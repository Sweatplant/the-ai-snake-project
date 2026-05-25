cmake_minimum_required(VERSION 3.15...3.27)
project(snake_ai LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# Find nanobind
find_package(nanobind CONFIG REQUIRED)

# Compiler settings
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Create the Python module named 'my_ai' using your C++ file
nanobind_add_module(my_ai src/agent.cpp)

# Install the compiled extension into the Python package root
install(TARGETS my_ai
    RUNTIME DESTINATION .
    LIBRARY DESTINATION .
    ARCHIVE DESTINATION .
)