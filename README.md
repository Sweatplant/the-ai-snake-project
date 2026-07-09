# The AI Snake Project

A high-performance C++ Snake engine wrapped in Python using `nanobind`.

## What it is

This project includes:

- a C++ game engine in [src](src)
- a Python module built with nanobind
- a playable version in [play_human.py](play_human.py)
- a training script in [train.py](train.py)
- several AI agent implementations in [agents](agents)

## Requirements

Make sure you have:

- Python 3.8 or newer
- Windows PowerShell
- CMake
- Visual Studio Build Tools with the Desktop development with C++ workload

## Setup

Open a terminal in the folder where you cloned or downloaded this repository.

If needed, change into the project folder:

```powershell
cd path\to\the-ai-snake-project
```

Create and activate a virtual environment:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

Install the required packages:

```powershell
python -m pip install pygame
pip install . --force-reinstall --no-cache-dir --config-settings=cmake.args="-A x64"
```

The second command builds the native extension.

## Run the game

Start the game with:

```powershell
python play_human.py
```

Use the arrow keys to move the snake. If you hit a wall or your own tail, the round resets.

## Project files

- [play_human.py](play_human.py): runs the human-playable version
- [train.py](train.py): training and execution loop for the AI agents
- [config.py](config.py): project configuration and settings
- [weights/](weights/): saved model weights and training checkpoints
- [agents/heuristic_agent.py](agents/heuristic_agent.py): heuristic-based agent
- [agents/heuristic_agent_ai.py](agents/heuristic_agent_ai.py): funny heuristic-based agent
- [agents/tabular_agent.py](agents/tabular_agent.py): tabular agent module, yet to be implemented
- [agents/dqn_agent.py](agents/dqn_agent.py): DQN agent module, yet to be implemented
- [agents/pgm_agent.py](agents/pgm_agent.py): probabilistic graphical model agent module, yet to be implemented
- [src/main.cpp](src/main.cpp): Python/C++ binding entry point
- [src/snake_engine.cpp](src/snake_engine.cpp): game logic
- [src/snake_engine.hpp](src/snake_engine.hpp): engine declarations
- [src/vision_engine.cpp](src/vision_engine.cpp): vision processing implementation
- [src/vision_engine.hpp](src/vision_engine.hpp): vision engine declarations
- [snake_ui/renderer.py](snake_ui/renderer.py): rendering code
- [CMakeLists.txt](CMakeLists.txt) & [pyproject.toml](pyproject.toml): The backend build configuration files.

## Troubleshooting

If the build fails, make sure Visual Studio Build Tools are installed and that the C++ workload is enabled.

If Python cannot import the compiled module, run:

```powershell
pip install . --force-reinstall --no-cache-dir --config-settings=cmake.args="-A x64"
```

If activation is blocked by PowerShell, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Quick start

If you want the short version, run:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pygame
pip install . --force-reinstall --no-cache-dir --config-settings=cmake.args="-A x64"
python [play_human or train].py
```