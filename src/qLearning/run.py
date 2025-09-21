import numpy as np
from pyboy import PyBoy
from constants import *
import database as db
import qLearning.qlearning as ql
import random

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

def run(load):
    """
    Run the Q Learning agent
    
    :param load: ID of the model to load
    """
    
    qlearning_collection = db.get_mongo_collection(DB_COLLECTION_QLEARNING)
    qtable_collection = db.get_mongo_collection(DB_COLLECTION_QTABLE)
    qtable_run_collection = db.get_mongo_collection(DB_COLLECTION_QL_RUN)
    mapping_collection = db.get_mongo_collection(DB_COLLECTION_QL_MAPPING)

    document = db.load(qlearning_collection, load)
    id = load
    epsilon = document["epsilon"]
    incr = document["incr"]
    ticks = document["ticks"]
    state_height = document["state_height"]
    state_width = document["state_width"]
    learning_rate = document["learning_rate"]
    gamma = document["gamma"]
        
    qlearning:ql.Qlearning = ql.QLearning(
            gamma=gamma, 
            learning_rate=learning_rate, 
            state_height=state_height,
            state_width=state_width,
            epsilon=epsilon
        ) 
    
    qtable = qlearning.initialize_qtable(id, qtable_collection)
    mapping = qlearning.initialize_mapping(id, mapping_collection)    
    
    for run_id in range(QL_RUNS):

        # Init epoch
        pyboy = PyBoy('sml.gb')
        pyboy.set_emulation_speed(QL_SPEED) # Default speed

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
                    
                    action = random.choice(INPUTS)
                    
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
                
                total_reward += reward
                reward = 0
                    

        finally:
            
            stats = {
                "qlearning_id": load,
                "run_id": str(run_id),
                "total_reward" : total_reward,
                "max_level_progress": max_level_progress,
                "lives_left": mario.lives_left + 1, # 3 lives = didn't die, 0 lives = dead
                "score": mario.score,
                "coins": mario.coins, 
                "level": f"{mario.world[0]}-{mario.world[1]}"
            }
            print(f"Run : {run_id}, Total reward : {total_reward}, Max level progress : {max_level_progress}, Epsilon: {epsilon}")
            
            db.save_ql_run(qtable_run_collection, stats)
            
            pyboy.stop()
            