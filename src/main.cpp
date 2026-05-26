/**
 * @file main.cpp
 * @brief Nanobind glue layer exporting the C++ SnakeEngine to Python.
 * @author Sam Ro
 * @date 26/05/2026
 * @details This file uses the nanobind library to expose the C++ SnakeEngine 
 * class and its methods directly to the Python ecosystem, allowing the engine 
 * to be imported as a native Python module ('my_ai'). (Description made by AI)
 */
#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h> // Crucial for auto-converting Python lists to C++ vectors
#include <vector>

namespace nb = nanobind;

class SnakeAI {
public:
    SnakeAI() {}
    
    // A dummy function that accepts a game state and returns an action
    int get_action(const std::vector<int>& state) {
        // ... Eventually, your neural network math will go here ...
        
        // For now, just return 3 (e.g., "Move Right")
        return 3; 
    }
};

// Expose the class and its methods to Python
NB_MODULE(my_ai, m) {
    nb::class_<SnakeAI>(m, "SnakeAI")
        .def(nb::init<>())
        .def("get_action", &SnakeAI::get_action);
} 