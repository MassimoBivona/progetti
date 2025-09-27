import argparse
import sys
import os

# Add the project root to the Python path for absolute imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# The AutonomousCore will be the central brain of the agent
# from core.reasoner import AutonomousCore

def main():
    """
    The main entry point for the Autonomous Creative Agent.
    This script initializes the agent's core and starts the execution
    of a user-provided idea.
    """
    parser = argparse.ArgumentParser(
        description="An autonomous creative agent that can reason, plan, and execute complex tasks."
    )

    parser.add_argument(
        "idea",
        type=str,
        help="The high-level idea or goal for the agent to execute. (e.g., 'Create a short video about the history of space exploration')"
    )

    # In the future, we could add arguments for configuration, like verbosity or model selection
    # parser.add_argument("--config", type=str, default="default_config.json")

    args = parser.parse_args()

    print(f"--- Autonomous Agent Initialized ---")
    print(f"Received Idea: '{args.idea}'")
    print("------------------------------------")

    # Instantiate and run the agent's brain
    core = AutonomousCore()
    result = core.execute_idea(args.idea)

    print("\n--- Agent Execution Complete ---")
    print(f"Final Output: {result}")


if __name__ == "__main__":
    from core.reasoner import AutonomousCore
    main()