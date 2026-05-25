//Test

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