#!/usr/bin/env python3
"""
Wrapper script to run the agent with better error handling.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from improved_agentic_agent import Agent
from agent_modules import AgentConfig

def main():
    """Run the agent with the specified goal."""
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found.")
        print("Please add it to a .env file in the project root:")
        print("  OPENAI_API_KEY=your-key-here")
        print("\nOr set it as an environment variable:")
        print("  export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Configuration
    config = AgentConfig(
        model="gpt-4",
        max_iterations=100,  # Increased for complex tasks
        log_level="INFO"
    )
    
    # Initialize agent
    workdir = "/Users/annhoward/intro_to_agents_12_2_2025/team_formation_agent/workdir2"
    agent = Agent(working_directory=workdir, config=config)
    
    # Goal
    goal = """https://mtgjson.com/getting-started/ - using this api, we want to solve the team formation problem with a mtg deck creator. Create a software system that can produce decks that are playable, competitive, and fun. Select strategies that work together, and write an evolutionary testing algorithm to test the decks. Your role is as chief data scientist and you will be responsible for the design, implementation, and testing of the software system and the evolutionary testing algorithm. First write an openspec spec and implement the software system and the evolutionary testing algorithm."""
    
    try:
        print("=" * 80)
        print("Starting agent execution...")
        print("=" * 80)
        result = agent.run(goal)
        print("=" * 80)
        print("Agent completed successfully!")
        print("=" * 80)
        print("\nFinal Result:")
        print(result)
        return 0
    except KeyboardInterrupt:
        print("\n\nAgent execution interrupted by user.")
        agent.cleanup()
        return 130
    except Exception as error:
        print(f"\n\nAgent execution failed: {error}")
        import traceback
        traceback.print_exc()
        agent.cleanup()
        return 1

if __name__ == "__main__":
    sys.exit(main())
