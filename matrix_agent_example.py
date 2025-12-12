"""
Example usage of the Agent with Matrix tools

This demonstrates how to use the agent to interact with Matrix
at matrix.themultiverse.school
"""

from agentic_agent_copy import Agent

# Initialize the agent
agent = Agent()

# Example 1: Post a message to a Matrix channel
print("=== Example 1: Posting a message ===")
agent.run("Post a message to the 'coordination' channel as agent 'file_organizer' saying 'Starting file organization task'")

# Example 2: Read messages from a channel
print("\n=== Example 2: Reading messages ===")
agent.run("Read the last 5 messages from the 'research' channel as agent 'reader'")

# Example 3: List all available Matrix rooms
print("\n=== Example 3: Listing rooms ===")
agent.run("List all available Matrix rooms")

# Example 4: Check if a user is a member of a channel
print("\n=== Example 4: Checking membership ===")
agent.run("Check if '@ann:matrix.themultiverse.school' is a member of the 'coordination' channel")

# Example 5: Invite a user to a channel
print("\n=== Example 5: Inviting a user ===")
agent.run("Invite '@newuser:matrix.themultiverse.school' to the 'research' channel as agent 'coordinator'")

# Example 6: Get notifications for an agent
print("\n=== Example 6: Getting notifications ===")
agent.run("Get the notification count for agent 'coordinator'")

# Example 7: Combined task - organize files and notify on Matrix
print("\n=== Example 7: Combined task ===")
agent.run("""
Organize the markdown files in this directory into a 'docs' folder,
then post a message to the 'coordination' channel as agent 'file_organizer'
summarizing what was organized.
""")

