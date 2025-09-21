import random
from constants import *

class QLearning:
    def __init__(self, state_height, state_width, learning_rate, gamma, epsilon):
        """
        Initialize the Q-learning agent with parameters.

        :param state_height: Height of the state representation.
        :param state_width: Width of the state representation.
        :param learning_rate: Learning rate for Q-learning.
        :param gamma: Discount factor for future rewards.
        :param epsilon: Initial epsilon value for exploration.
        """
        self.state_height = state_height
        self.state_width = state_width
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon

    def initialize_qtable(self, id:str, collection) -> list:
        """Initializes a Q-table as a list of dictionaries with keys from INPUTS and values set to zero."""
        res = []
        records = list(collection.find({"qlearning_id": id})) # Check if records exist for the given id

        if records:  # If records, load
            for entry in records:
                res.append({
                    "state_id": entry["state_id"],
                    "qlearning_id": entry["qlearning_id"],
                    "actions": entry["actions"]
                })
        else:  # otherwise, default values
            res.append({
                "state_id": 0,
                "qlearning_id": id,
                "actions": {key: 0 for key in INPUTS}
            })
        return res
    
    def initialize_mapping(self, id:str, collection) -> list:
        """Initializes a Q-table as a list of dictionaries with keys from INPUTS and values set to zero."""
        res = []
        records = list(collection.find({"qlearning_id": id}).sort("state_id", 1)) # Check if records exist for the given id

        if records:  # If records, load
            for entry in records:
                res.append(entry["mapping"])
        return res

    def create_row(self, state_id: int, qlearning_id: str) -> dict:
        """creates a new row as a dictionary entry."""
        return {
                "state_id": state_id,
                "qlearning_id": qlearning_id,
                "actions": {key: 0 for key in INPUTS}
            }
        
    def create_mapping_row(self, state_id: int, qlearning_id: str) -> dict:
        """creates a new row as a dictionary entry."""
        return {
                "state_id": state_id,
                "qlearning_id": qlearning_id,
                "mapping": []
            }

    def update(self, qtable: dict, state_id: int, action: str, reward: int) -> dict:
        """Updates a Q-value based on the Q-learning equation."""

        # Find the dictionary where state_id matches
        state_entry = next((entry for entry in qtable if entry["state_id"] == state_id), None)

        # Get current Q-value
        current_value = state_entry["actions"][action]

        # Q-learning update rule
        state_entry["actions"][action] = (
            current_value + self.learning_rate * (reward + self.gamma * self.get_max_value(qtable) - current_value)
        )
        
        return qtable


    def get_max_value(self, qtable: list) -> float:
        """Returns the maximum value from a qtable (list of dictionaries)."""
        if not isinstance(qtable, list):
            raise ValueError("Input must be a list.")

        max_value = float('-inf')
        for row in qtable:
            if not isinstance(row, dict):
                raise ValueError("Each element of the qtable must be a dictionary.")
            if row:  # Ensure dictionary is not empty
                max_value = max(max_value, max(row["actions"].values()))

        return max_value

    def pick_action(self, qtable: list, state_id: int) -> str:
        """Pick an action based on epsilon-greedy policy."""
        state_entry = next(entry for entry in qtable if entry["state_id"] == state_id)
        if self.epsilon > random.random():
            return random.choice(INPUTS)
        else:
            max_action = max(state_entry["actions"], key=state_entry["actions"].get)
            return max_action


    def find_mario_position(self, game_map: list) -> tuple:
        """Finds Mario's most bottom 1 position in the game map."""
        rows = len(game_map)
        cols = len(game_map[0]) if rows > 0 else 0
        bottom_most = None

        for row in range(rows):
            for col in range(cols):
                if game_map[row][col] == 1:
                    bottom_most = (row, col)  # Always update to the most bottom one
        
        return bottom_most


    def get_state(self, game_map: list) -> list:
        """Extracts a sub-qtable of size state_height x state_width around Mario's position."""
        mario_position = self.find_mario_position(game_map)
        if not mario_position:
            raise ValueError("Mario's position could not be found in the map." + str(game_map))

        game_map = [[int(value) for value in row] for row in game_map.tolist()]
        mario_row, mario_col = mario_position

        rows = len(game_map)
        cols = len(game_map[0]) if rows > 0 else 0

        # Initialize the result qtable with -1
        subqtable = [[-1 for _ in range(self.state_width)] for _ in range(self.state_height)]

        # Fill the subqtable with values from the game map
        for i in range(self.state_height):
            for j in range(self.state_width):
                map_row = mario_row + i - self.state_height // 2
                map_col = mario_col + j - self.state_width // 2

                if 0 <= map_row < rows and 0 <= map_col < cols:
                    subqtable[i][j] = game_map[map_row][map_col]

        return subqtable

