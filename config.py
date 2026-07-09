"""
@file config.py
@brief Centralized Configuration and hyperparameters for the Snake AI Project.
@author Sam Ro
@date 26/06/2026
"""

# --- Simulation & Grid Settings ---
GRID_WIDTH = 10
GRID_HEIGHT = 10
CELL_SIZE = 30
FPS = 0                         # Simulation speed (set 0 for max speed)
RENDERER_ENABLED = False        # Enable or Disable game rendering
TRAINING_ENABLED = True         # Enable or Disable training (for RL agents)
SAVE_FREQUENCY = 1000            # Save frequency (save every # games, for RL agents)

# --- Agent Selection ---       (Stats are for 20x20 grid)
# AGENT_TYPE = "human"          # Play manually with arrowkeys
# AGENT_TYPE = "heuristic"      # Rule-based AI agent (Mean score: ~28, Max score: ~87)
AGENT_TYPE = "tabular"          # Tabular AI agent (Basic: Mean score: ~23, Max score: ~71)
# AGENT_TYPE = "dqn"
# AGENT_TYPE = "pgm"

# Other Agents:
# AGENT_TYPE = "heuristic_ai"   # Funny AI made agent


# --- Plotting Settings ---
VISUALISATION_ENABLED = False           # Enable or disable real-time plotting of scores
PLOT_PERFORMANCE_HISTORY = True         # Plot 1: Scores over time + Running Average
PLOT_FREQUENCY_DISTRIBUTION = True      # Plot 2: Frequency distribution histogram of scores
STATISTICS_LOG_INTERVAL = 5             # Print detailed console statistics every N games

# --- Rewards ---
REWARD_EATING = 25          # Reward for eating food
REWARD_DYING = -200          # Penalty for dying
REWARD_NOTHING = -0.05          # Reward/penalty for just doing nothing

# --- Vision Type ---               (Delete weights in case of changing vision type)
# VISION_TYPE = "basic"
VISION_TYPE = "ray"                
RAY_LENGTH = 2                    # For ray, change how far the rays can see (in grid units)
# VISION_TYPE = "grid"


# --- Tabular Q-Learning Hyperparameters ---
TABULAR_LR = 0.1            # Alpha: learning rate
TABULAR_GAMMA = 0.95         # Discount factor
TABULAR_EPSILON = 1.0       # Initial exploration rate
TABULAR_EPSILON_DECAY = 0.995
TABULAR_EPSILON_MIN = 0.01

# --- Deep Q-Network (DQN) Hyperparameters ---
DQN_LR = 0.001
DQN_GAMMA = 0.9
DQN_HIDDEN_SIZE = 256

import train
if __name__ == "__main__":
    train.main()