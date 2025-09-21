import numpy as np
from pyboy import PyBoy
from constants import *
import database as db
import qLearning.qlearning as ql


def find_state_id(mapping: dict, state: list) -> int:
    """
    Finds the index of the state
    
    Args:
        mapping (dict): The dictionary to search.
        state: The value to search for.
        
    Returns:
        int: the row of the state in the qtable
    """
    for i in range(len(mapping)):
        if mapping[i] == state:
            return i
    return None

def train_agent(epochs, ticks, epsilon, load, state_height, state_width, learning_rate, gamma):
    """
    Trains the Q-learning agent with the given parameters.

    :param epochs: Number of training epochs
    :param ticks: Number of ticks per epoch
    :param epsilon: Initial epsilon value for exploration
    :param load: ID of the model to load (-1 if training from scratch)
    :param state_height: Height of the state representation
    :param state_width: Width of the state representation
    :param learning_rate: Learning rate for Q-learning
    :param gamma: Discount factor for future rewards
    """
        
    qlearning_collection = db.get_mongo_collection(DB_COLLECTION_QLEARNING)
    qtable_collection = db.get_mongo_collection(DB_COLLECTION_QTABLE)
    mapping_collection = db.get_mongo_collection(DB_COLLECTION_QL_MAPPING)
        
    # init global stuff (in case no load)
    qtable = dict({})
    incr = 0
    mapping = list({})
    id = db.get_next_id(qlearning_collection)
    epoch_start = 1
    stats = dict({})
    
    epsilon = epsilon if epsilon else QL_EPSILON
    ticks = ticks if ticks else QL_TICKS
    state_height = state_height if state_height else QL_STATE_HEIGHT
    state_width = state_width if state_width else QL_STATE_WIDTH
    learning_rate = learning_rate if learning_rate else QL_LEARNING_RATE
    gamma = gamma if gamma else QL_GAMMA
    speed = QL_SPEED
    
    # Load from the database
    if (load != "-1"):
        document = db.load(qlearning_collection, load)
        id = load
        epsilon = document["epsilon"]
        incr = document["incr"]
        epoch_start = document["epoch"] + 1
        stats = document["stats"]
        ticks = document["ticks"]
        state_height = document["state_height"]
        state_width = document["state_width"]
        learning_rate = document["learning_rate"]
        gamma = document["gamma"]
    else:
        # Store the hyper params in the database
        to_save = {
            "_id": id,
            "epsilon": epsilon,
            "incr": incr,
            "epoch": epoch_start,
            "stats": stats,
            "ticks": ticks,
            "state_height": state_height,
            "state_width": state_width,
            "learning_rate": learning_rate,
            "gamma": gamma,
        }
        db.save(qlearning_collection, to_save)
        
    qlearning:ql.Qlearning = ql.QLearning(
            gamma=gamma, 
            learning_rate=learning_rate, 
            state_height=state_height,
            state_width=state_width,
            epsilon=epsilon
        ) 
    
    qtable = qlearning.initialize_qtable(id, qtable_collection)
    mapping = qlearning.initialize_mapping(id, mapping_collection)

    for epoch in range(epoch_start, QL_EPOCHS, 1):

        # Init epoch
        pyboy = PyBoy('sml.gb')
        pyboy.set_emulation_speed(speed) # Default speed

        mario = pyboy.game_wrapper
        mario.game_area_mapping(mario.mapping_compressed, 0)
        mario.start_game()
        
        max_level_progress = mario.level_progress
        last_level_progress = mario.level_progress
        
        max_lives = mario.lives_left + 1 #Consider current life as third life (so 0 life left = game over)
        reward = 0
        state = None
        action = None
        total_reward = 0
        
        try:
            for tick in range(ticks):
                try:
                    state = qlearning.get_state(mario.game_area())
                except ValueError as e:
                    #print(f"Error occurred: {e}")
                    pyboy.tick()
                    continue
                
                state_id = incr
                if state not in mapping:
                    
                    #mapping
                    new_mapping_row = qlearning.create_mapping_row(state_id, id)
                    new_mapping_row["mapping"] = state
                    db.save_ql_mapping(mapping_collection, new_mapping_row)
                    mapping.append(state)
                    
                    #qtable
                    new_row = qlearning.create_row(state_id, id)
                    db.save_qtable(qtable_collection, new_row)
                    qtable.append(new_row)
                    incr += 1
                    
                else:
                    state_id = find_state_id(mapping, state)

                action = qlearning.pick_action(qtable, state_id)
                
                if (action == 'longjump'):
                    pyboy.button('a', 10) # jump for 10 frames
                    for _ in range(10):
                        pyboy.tick()
                        
                else:
                    pyboy.button(action, 1)
                    pyboy.tick()  # Advance one frame
                    
                if (mario.level_progress > max_level_progress):
                    reward += mario.level_progress - max_level_progress
                    max_level_progress = mario.level_progress # only if he went forward 

                if (mario.lives_left < max_lives):
                    reward += - 10
                    max_lives = mario.lives_left
                    
                    if (max_lives == 0):
                        pyboy.stop()
                        break
                    
                # q learning
                qtable = qlearning.update(qtable, state_id, action, reward)
                
                # results
                #print(f"Tick : {tick}, reward : {reward}, level progress : {mario.level_progress}, action : {action}")
                # reset & update variables 
                total_reward += reward
                reward = 0
                last_level_progress = mario.level_progress

                state_entry = next((entry for entry in qtable if entry["state_id"] == state_id), None)
                db.save_qtable(qtable_collection, state_entry)

        finally:
            #print(mario)
            stats[str(epoch)] = {
                "total_reward" : total_reward,
                "max_level_progress": max_level_progress,
                "lives_left": mario.lives_left + 1, # 3 lives = didn't die, 0 lives = dead
                "score": mario.score,
                "coins": mario.coins, 
                "level": f"{mario.world[0]}-{mario.world[1]}"
            }
            print(f"Epoch : {epoch}, Total reward : {total_reward}, Max level progress : {max_level_progress}, Epsilon: {epsilon}")
            #print("qtable : ")
            #print(qtable)
            #print("mapping")
            #print(mapping)
            to_save = {
                "_id": id,
                "epsilon": epsilon,
                "incr": incr,
                "epoch": epoch,
                "stats": stats
            }

            db.save(qlearning_collection, to_save)
            
            if (QL_DECREASE_EPSILON):
                epsilon -= ql.EPSILON_DECAY
            pyboy.stop()
            