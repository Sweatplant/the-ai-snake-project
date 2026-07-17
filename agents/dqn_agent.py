"""
@file dqn_agent.py
@brief Deep Q-Network (DQN) agent for the Snake game.
@author Sam Ro
@date 12/07/2026
@version 1.1
@details This agent uses a Deep Neural Network to approximate Q-values, 
allowing it to scale efficiently to complex integer-based or high-dimensional 
state vectors like Ray Vision and Grid vision (Description partially made by AI)
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
import os
from collections import deque
import config
import my_ai



class QNetwork(nn.Module):
    """
    Define the Neural Network architecture per vision type
    """
    def __init__(self, vision_type, input_shape, output_dim):
        super(QNetwork, self).__init__()
        self.vision_type = vision_type
        grid_height = config.GRID_HEIGHT
        grid_width = config.GRID_WIDTH

        # Define the neural network architecture based on the vision type
        # Basic vision & Ray vision: 11 or 16 input features, 4 output actions
        if vision_type in ["basic", "ray"]:
            self.network = nn.Sequential(
                nn.Linear(input_shape[0], 128),
                nn.ReLU(),
                nn.Linear(128, 128),
                nn.ReLU(),
                nn.Linear(128, 128),
                nn.ReLU(),
                nn.Linear(128, output_dim)
            )
        
        elif vision_type == "grid":
            num_channels = len(config.GRID_CHANNELS)
            
            # convolutional layers
            self.features = nn.Sequential(
                nn.Conv2d(num_channels, 32, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.Conv2d(32, 64, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.Conv2d(64, 128, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.Conv2d(128, 128, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.Flatten()
            )
            # calculate the size of the flattened feature map after conv layers
            with torch.no_grad():
                dummy_input = torch.zeros(1, num_channels, grid_height, grid_width)
                self.flattened_size = self.features(dummy_input).shape[1]

            # fully connected layers
            self.classifier = nn.Sequential(
                nn.Linear(self.flattened_size, 256),
                nn.ReLU(),
                nn.Linear(256, 128),
                nn.ReLU(),
                nn.Linear(128, 64),
                nn.ReLU(),
                nn.Linear(64, output_dim)
            )
            
    def forward(self, x): 
        if self.vision_type in ["basic", "ray"]:
            return self.network(x)
        elif self.vision_type == "grid":
            x = self.features(x)
            x = self.classifier(x)
            return x

class ReplayBuffer:

    """
    Define an experience replay buffer to store past experiences for training the DQN.
    """
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        state, action, reward, next_state, done = zip(*random.sample(self.buffer, batch_size))
        return (np.array(state, dtype=np.float32),
                np.array(action, dtype=np.int64),
                np.array(reward, dtype=np.float32),
                np.array(next_state, dtype=np.float32),
                np.array(done, dtype=np.uint8))
    
    def __len__(self):
        return len(self.buffer)
    

class DQNAgent:
    """
    DQN Agent for the Snake game. Uses a Deep Neural Network to approximate Q-values.
    """
    def __init__(self, vision_type="basic"):
        self.vision_type = vision_type
        self.model_path = f"weights/dqn_{vision_type}_model.pth"
        
        self.output_dim = 4  # Up, Down, Left, Right

        if self.vision_type == "basic":
            self.input_shape = (11,)  # Basic vision has 11 features
        elif self.vision_type == "ray":
            self.input_shape = (16,)  # Ray vision has 16 features
        elif self.vision_type == "grid":
            self.num_channels = len(config.GRID_CHANNELS)
            self.grid_height = config.GRID_HEIGHT
            self.grid_width = config.GRID_WIDTH
            self.input_shape = (self.num_channels, self.grid_height, self.grid_width)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"DQN Agent initialized using device: {self.device}")

        # Pass the new arguments to the network
        self.policy_net = QNetwork(self.vision_type, self.input_shape, self.output_dim).to(self.device)
        self.target_net = QNetwork(self.vision_type, self.input_shape, self.output_dim).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()  # Target net is only used for evaluation mode

        # Hyperparameters
        self.lr = config.DQN_LR
        self.gamma = config.DQN_GAMMA
        self.epsilon = config.DQN_EPSILON
        self.epsilon_decay = config.DQN_EPSILON_DECAY
        self.epsilon_min = config.DQN_EPSILON_MIN
        self.batch_size = config.DQN_BATCH_SIZE

        # Optimizer and Loss Function
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

        # Memory buffer
        self.buffer_capacity = config.DQN_BUFFER_CAPACITY
        self.memory = ReplayBuffer(self.buffer_capacity)

        # Target network update frequency
        self.target_update_freq = config.DQN_TARGET_UPDATE_FREQ
        self.update_counter = 0

        self.training_enabled = config.TRAINING_ENABLED
        if not self.training_enabled:
            self.epsilon = 0.0  # No exploration if not training
        
        self.load_model()
    
    def get_state(self, engine):
        """
        Computes an (11 for basic or 16 for rayvision, or more for grid)-value binary state vector based on the current game state.
        The vector indicates immediate dangers (walls, self-collision) and food location. Also formats it for PyTorch
        """
        # convert from list (due to nanobind) to tuple before returning
        if self.vision_type == "basic":
            return np.array(my_ai.get_basic_vision(engine), dtype=np.float32)
        elif self.vision_type == "ray":
            return np.array(my_ai.get_ray_vision(engine, config.RAY_LENGTH), dtype=np.float32)
        elif self.vision_type == "grid":
            # fetch grid and convert to numpy array
            grid_data = my_ai.get_grid_vision(engine, config.GRID_CHANNELS)
            state = np.array(grid_data, dtype=np.float32)
            return state.reshape(self.num_channels, self.grid_height, self.grid_width)
        
    def get_action(self, state):
        """
        selects an action using epsilon-greedy policy
        """
        # exploration (pick random action)
        if self.training_enabled and random.random() < self.epsilon:
            return random.randint(0, self.output_dim - 1)  # Explore: random action
        
        # exploitation (pick best action)
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)  # Add batch dimension
            q_values = self.policy_net(state_tensor)
            return q_values.argmax().item()  # Return the index of the max Q-value as the action
        
    def update(self, state, action, reward, next_state, done):
        """
        Stores experience tuple and performs gradient descent step
        """
        if not self.training_enabled:
            return
        
        # save experience to memory buffer
        self.memory.push(state, action, reward, next_state, done)

        # skip training if buffer doesnt have neough samples
        if len(self.memory) < self.batch_size:
            return
        
        # sample
        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)

        # convert array to tensors
        states_tensor = torch.FloatTensor(states).to(self.device)
        actions_tensor = torch.LongTensor(actions).unsqueeze(1).to(self.device)  # Add dimension for gather
        rewards_tensor = torch.FloatTensor(rewards).unsqueeze(1).to(self.device)
        next_states_tensor = torch.FloatTensor(next_states).to(self.device)
        dones_tensor = torch.FloatTensor(dones).unsqueeze(1).to(self.device)

        # current Q predictions
        current_q_values = self.policy_net(states_tensor).gather(1, actions_tensor)

        # max future Q estimated
        with torch.no_grad():
            max_next_q = self.target_net(next_states_tensor).max(1, keepdim=True)[0]
            # Bellman targets: target = R if dead else R + gamma * max(Q_next)
            target_q_values = rewards_tensor + (self.gamma * max_next_q * (1 - dones_tensor))
        
        # compute loss
        loss = self.criterion(current_q_values, target_q_values)

        # backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # update target network periodically
        self.update_counter += 1
        if self.update_counter % self.target_update_freq == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

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
        torch.save(self.policy_net.state_dict(), self.model_path)
        print(f"-> DQN weights saved successfully to {self.model_path}")

        
    def load_model(self):
        """
        Load the previously trained model
        """
        if os.path.exists(self.model_path):
            try:
                self.policy_net.load_state_dict(torch.load(self.model_path, map_location=self.device))
                self.target_net.load_state_dict(self.policy_net.state_dict())
                print(f"-> DQN weights loaded successfully from {self.model_path}")
            except Exception as e:
                print(f"Error loading DQN weights: {e}")

        



