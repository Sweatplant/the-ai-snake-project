# The AI Snake Project

A Python-accessible Snake agent built in C++ using `nanobind`.

## Overview

This repository demonstrates building a native Python extension module named `my_ai` from `src/agent.cpp` and packaging it with `scikit-build-core`.

The package distribution name is `snake_ai`, while the imported module is `my_ai`.

## Requirements

- Python 3.8+
- Windows with Visual Studio Build Tools (or compatible C++ toolchain)
- `pip`
- `cmake` (installed automatically by the build backend)

## Install

From the repository root:

```powershell
python -m pip install .
```

If you need to reinstall after changes:

```powershell
python -m pip install --force-reinstall .
```

## Usage

Run the game script or import the extension directly:

```powershell
python game.py
```

Or use the module in Python:

```python
import my_ai
agent = my_ai.SnakeAI()
action = agent.get_action([5, 10, 5, 12, 1])
print(action)
```

## Project layout

- `CMakeLists.txt` - builds the `my_ai` extension module with `nanobind`
- `pyproject.toml` - Python packaging metadata for `snake_ai`
- `src/agent.cpp` - C++ implementation of the Snake AI module
- `game.py` - example Python usage

## Notes

- The compiled module is exposed as `my_ai`.
- The package name installed by `pip` is `snake_ai`.
- If `import my_ai` fails after installation, ensure the package build includes the extension module and reinstall.
