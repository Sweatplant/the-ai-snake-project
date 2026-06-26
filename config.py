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
FPS = 0                 # Simulation speed (set 0 for max speed)
RENDERER_ENABLED = False 
TRAINING_ENABLED = True          

# --- Agent Selection ---
# AGENT_TYPE = "human"        # Play manually with arrowkeys
# AGENT_TYPE = "heuristic"    # Rule-based AI agent (Mean score: ~28, Max score: ~87)
AGENT_TYPE = "tabular"
# AGENT_TYPE = "dqn"
# AGENT_TYPE = "pgm"

# Other Agents:
# AGENT_TYPE = "heuristic_ai" # Funny AI made agent


# --- Plotting Settings ---
VISUALISATION_ENABLED = False  # Enable or disable real-time plotting of scores
PLOT_PERFORMANCE_HISTORY = True         # Plot 1: Scores over time + Running Average
PLOT_FREQUENCY_DISTRIBUTION = True       # Plot 2: Frequency distribution histogram of scores
STATISTICS_LOG_INTERVAL = 5             # Print detailed console statistics every N games


# --- Tabular Q-Learning Hyperparameters ---
TABULAR_LR = 0.1            # Alpha: learning rate
TABULAR_GAMMA = 0.9         # Discount factor
TABULAR_EPSILON = 1.0       # Initial exploration rate
TABULAR_EPSILON_DECAY = 0.995
TABULAR_EPSILON_MIN = 0.01

# --- Deep Q-Network (DQN) Hyperparameters ---
DQN_LR = 0.001
DQN_GAMMA = 0.9
DQN_HIDDEN_SIZE = 256