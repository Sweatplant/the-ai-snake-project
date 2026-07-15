"""
@file config.py
@brief Centralized Configuration and hyperparameters for the Snake AI Project.
@author Sam Ro
@date 26/06/2026
"""

# --- Simulation & Grid Settings ---
GRID_WIDTH = 20
GRID_HEIGHT = 20
CELL_SIZE = 30
FPS = 0                         # Simulation speed (set 0 for max speed)
RENDERER_ENABLED = False        # Enable or Disable game rendering
TRAINING_ENABLED = True         # Enable or Disable training (for RL agents)
SAVE_FREQUENCY = 200            # Save frequency (save every # games, for RL agents)

# --- Agent Selection ---       (Stats are for 20x20 grid)
# AGENT_TYPE = "human"          # Play manually with arrowkeys
# AGENT_TYPE = "heuristic"      # Rule-based AI agent (Mean score: ~28, Max score: ~87)
# AGENT_TYPE = "tabular"          # Tabular AI agent (Basic: Mean score: ~23, Max score: ~71)
AGENT_TYPE = "dqn"
# AGENT_TYPE = "pgm"

# Other Agents:
# AGENT_TYPE = "heuristic_ai"   # Funny AI made agent
# AGENT_TYPE = "tabular_mb"     # Tabular Model-Based AI agent


# --- Plotting Settings ---
VISUALISATION_ENABLED = False           # Enable or disable real-time plotting of scores
PLOT_PERFORMANCE_HISTORY = False         # Plot 1: Scores over time + Running Average
PLOT_FREQUENCY_DISTRIBUTION = False      # Plot 2: Frequency distribution histogram of scores
STATISTICS_LOG_INTERVAL = 50             # Print detailed console statistics every N games

# --- Rewards ---
REWARD_EATING = 50              # Reward for eating food
REWARD_DYING = -200             # Penalty for dying
REWARD_NOTHING = -0.01           # Reward/penalty for just doing nothing
REWARD_CLOSER = 0.25             # Reward for going closer to the food
REWARD_FURTHER = -0.3           # Reward for going further from the food

# --- Vision Type ---               (Delete weights in case of changing vision type)
# VISION_TYPE = "basic"
# VISION_TYPE = "ray"                
# RAY_LENGTH = 10                    # For ray, change how far the rays can see (in grid units)
VISION_TYPE = "grid"
GRID_CHANNELS = ["head", "body", "food"]  # For grid, change what channels to include in the grid vision (["head", "body", "food", "walls", "enemy_head","enemy_body"])


# --- Tabular Q-Learning Hyperparameters ---
TABULAR_LR = 0.1                # Learning rate
TABULAR_GAMMA = 0.95            # Discount factor
TABULAR_EPSILON = 1.0           # Initial exploration rate
TABULAR_EPSILON_DECAY = 0.9995   # Exploration rate decay
TABULAR_EPSILON_MIN = 0.01      # Residual exploration rate

# --- Deep Q-Network (DQN) Hyperparameters ---
DQN_LR = 0.00025                 # Learning rate
DQN_GAMMA = 0.99                # Discount factor
DQN_EPSILON = 1.0               # Initial exploration rate
DQN_EPSILON_DECAY = 0.995       # Exploration rate decay
DQN_EPSILON_MIN = 0.005          # Residual exploration rate
DQN_BATCH_SIZE = 128             # Batch size for training
DQN_BUFFER_CAPACITY = 500000     # Replay buffer capacity
DQN_TARGET_UPDATE_FREQ = 1000   # Frequency to update target network

import train
if __name__ == "__main__":
    train.main()