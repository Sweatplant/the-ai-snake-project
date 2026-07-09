"""
@file tabular_agent.py
@brief Tabular Q-Learning agent for the Snake game.
@author Sam Ro
@date 26/06/2026
@version 1.0
@details This agent uses a Dictionary (Hash Map) to store Q-values for 
all 2,048 possible combinations of the 11-value state vector. It utilizes
the Bellman equation to learn optimal moves over time via trial and error. (Description made by AI)
"""

import random
import pickle
import config
import my_ai
import os

class TabularAgent:
    def __init__(self, vision_type="basic"):
        self.model_path = "weights/tabular_q_table.pkl"
        self.vision_type = vision_type
        
        # C++ action enum values mapping
        self.UP = 0
        self.DOWN = 1
        self.LEFT = 2
        self.RIGHT = 3    

        # grid size
        self.width = config.GRID_WIDTH
        self.height = config.GRID_HEIGHT

        # Hyperparameters
        self.alpha = config.TABULAR_LR
        self.gamma = config.TABULAR_GAMMA
        self.epsilon = config.TABULAR_EPSILON
        self.epsilon_decay = config.TABULAR_EPSILON_DECAY
        self.epsilon_min = config.TABULAR_EPSILON_MIN

        # To Train or not to Train
        self.training_enabled = config.TRAINING_ENABLED
        if not config.TRAINING_ENABLED:
            self.epsilon = 0.0
            self.alpha = 0.0

        # Q-Table
        self.q_table = {}
        self.load_model()
        
    def get_state(self, engine):
        """
        Computes an (11 for basic or 16 for rayvision)-value binary state vector based on the current game state.
        The vector indicates immediate dangers (walls, self-collision) and food location.
        """
        # convert from list (due to nanobind) to tuple before returning
        if self.vision_type == "basic":
            return tuple(my_ai.get_basic_vision(engine))
        elif self.vision_type == "ray":
            return tuple(my_ai.get_ray_vision(engine, config.RAY_LENGTH))

    def get_q_values(self, state):
        """
        Helper function to get Q-values for a state, and if it does not exist it will initialize with zeros for all directions
        """
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0, 0.0]
        return self.q_table[state]

    def get_action(self, state):
        """
        Selects an action using epsilon-greedy policy
        """
        # exploration (pick random action)
        if random.random() < self.epsilon:
            return random.randint(0, 3) # it should learn that it dies so even dangerous actions are possible

        # exploitation (pick the best known action for this state)
        q_values = self.get_q_values(state)
        max_q = max(q_values)

        # if multiple actions have the same q-value, pick random one
        best_actions = []
        for i, q in enumerate(q_values):
            if q == max_q:
                best_actions.append(i)
        return random.choice(best_actions)

    def update(self, state, action, reward, next_state, game_over):
        """
        Update the Q-table using Bellman Equation
        """
        if not self.training_enabled:
            return
        
        q_values = self.get_q_values(state)
        next_q_values = self.get_q_values(next_state)

        # if game is over / snake is dead, next q values are zero
        if game_over:
            max_next_q = 0.0
        else:
            max_next_q = max(next_q_values)
        
        # Q learning algorithm:
        q_values[action] = q_values[action] + self.alpha*(reward + self.gamma * max_next_q - q_values[action])
        
    def decay_epsilon(self):
        """
        Reduces exploration over time
        """
        if self.training_enabled:
            self.epsilon *= self.epsilon_decay
            self.epsilon = max(self.epsilon_min, self.epsilon)

    def save_model(self):
        """
        Save the trained model
        TODO add versioning
        """
        if not self.training_enabled:
            return
        
        # write to table
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(self.q_table, f)
        
    def load_model(self):
        """
        Load the previously trained model
        """
        if os.path.exists(self.model_path):
            with open(self.model_path, "rb") as f:
                self.q_table = pickle.load(f)
            print(f"Loaded Q-table with {len(self.q_table)} states.")
        else:
            print("No existing Q-table found. making new one.")
