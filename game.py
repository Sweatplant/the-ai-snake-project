#test 2

import my_ai

def main():
    print("Initializing C++ Agent...")
    agent = my_ai.SnakeAI()
    
    # Fake board state (snake coords, food coords, etc.)
    state = [5, 10, 5, 12, 1] 
    
    print(f"Sending state to C++: {state}")
    action = agent.get_action(state)
    
    print(f"Success! The C++ AI says to take action: {action}")

if __name__ == "__main__":
    main()