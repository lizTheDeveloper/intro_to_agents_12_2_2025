from openai import OpenAI
client = OpenAI()
import json 
import os
import requests
from typing import Optional, List

def read_file(filepath):
    print(f"Reading file: {filepath}")
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return content
    except Exception as error:
        return f"Error reading file: {str(error)}"

def write_file(filepath, content):
    print(f"Writing to file: {filepath}")
    try:
        with open(filepath, 'w') as file:
            file.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as error:
        return f"Error writing file: {str(error)}"

def list_directory(path):
    print(f"Listing directory: {path}")
    try:
        entries = os.listdir(path)
        return {"entries": entries, "count": len(entries)}
    except Exception as error:
        return f"Error listing directory: {str(error)}"

def move_file(source_path, destination_path):
    print(f"Moving file from {source_path} to {destination_path}")
    try:
        os.rename(source_path, destination_path)
        return f"Successfully moved {source_path} to {destination_path}"
    except Exception as error:
        return f"Error moving file: {str(error)}"

def contact_user(message):
    print(f"\n[Agent contacting user]: {message}")
    user_response = input("Your response: ")
    return user_response

def make_directory(path):
    print(f"Creating directory: {path}")
    try:
        os.makedirs(path, exist_ok=True)
        return f"Successfully created directory {path}"
    except Exception as error:
        return f"Error creating directory: {str(error)}"

# Matrix integration functions
MATRIX_SERVER = "https://matrix.themultiverse.school"

def matrix_post_message(channel, agent, message, status=None):
    """Post a message to a Matrix room."""
    print(f"Posting Matrix message to {channel} as {agent}: {message}")
    try:
        # This would integrate with your Matrix MCP server
        # For now, returning a simulated response
        return {
            "success": True,
            "channel": channel,
            "agent": agent,
            "message": message,
            "status": status
        }
    except Exception as error:
        return f"Error posting Matrix message: {str(error)}"

def matrix_read_messages(channel, agent, limit=10):
    """Read recent messages from a Matrix room."""
    print(f"Reading messages from {channel} as {agent}, limit: {limit}")
    try:
        return {
            "success": True,
            "channel": channel,
            "limit": limit,
            "messages": []  # Would be populated by actual Matrix API
        }
    except Exception as error:
        return f"Error reading Matrix messages: {str(error)}"

def matrix_list_rooms(agent="orchestrator"):
    """List all configured Matrix rooms."""
    print(f"Listing Matrix rooms for {agent}")
    try:
        return {
            "success": True,
            "rooms": []  # Would be populated by actual Matrix API
        }
    except Exception as error:
        return f"Error listing Matrix rooms: {str(error)}"

def matrix_invite_user(channel, agent, user_id):
    """Invite a user to a Matrix room."""
    print(f"Inviting {user_id} to {channel} by {agent}")
    try:
        return {
            "success": True,
            "channel": channel,
            "user_id": user_id,
            "invited_by": agent
        }
    except Exception as error:
        return f"Error inviting user to Matrix room: {str(error)}"

def matrix_check_membership(channel, user_id, agent="orchestrator"):
    """Check if a user is a member of a Matrix room."""
    print(f"Checking membership of {user_id} in {channel}")
    try:
        return {
            "success": True,
            "channel": channel,
            "user_id": user_id,
            "is_member": False  # Would be populated by actual Matrix API
        }
    except Exception as error:
        return f"Error checking Matrix membership: {str(error)}"

def matrix_get_notifications(agent, channels=None):
    """Get unread notification count for an agent."""
    print(f"Getting notifications for {agent}")
    try:
        return {
            "success": True,
            "agent": agent,
            "channels": channels or [],
            "unread_count": 0  # Would be populated by actual Matrix API
        }
    except Exception as error:
        return f"Error getting Matrix notifications: {str(error)}"


class Agent:
    def __init__(self):
        self.tools = [
            {
                "type": "function",
                "name": "read_file",
                "description": "Read the contents of a file at the specified filepath.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "The path to the file to read",
                        },
                    },
                    "required": ["filepath"],
                },
            },
            {
                "type": "function",
                "name": "write_file",
                "description": "Write content to a file at the specified filepath.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "The path to the file to write to",
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write to the file",
                        },
                    },
                    "required": ["filepath", "content"],
                },
            },
            {
                "type": "function",
                "name": "list_directory",
                "description": "List all files and directories in the specified path.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The directory path to list contents from",
                        },
                    },
                    "required": ["path"],
                },
            },
            {
                "type": "function",
                "name": "move_file",
                "description": "Move or rename a file from source path to destination path.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source_path": {
                            "type": "string",
                            "description": "The current path of the file to move",
                        },
                        "destination_path": {
                            "type": "string",
                            "description": "The new path where the file should be moved to",
                        },
                    },
                    "required": ["source_path", "destination_path"],
                },
            },
            {
                "type": "function",
                "name": "contact_user",
                "description": "Contact the user to request information or clarification. Use this when you need user input to proceed with the task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message or question to present to the user",
                        },
                    },
                    "required": ["message"],
                },
            },
            {
                "type": "function",
                "name": "make_directory",
                "description": "Create a new directory at the specified path. Creates parent directories if they don't exist.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path where the directory should be created",
                        },
                    },
                    "required": ["path"],
                },
            },
            {
                "type": "function",
                "name": "matrix_post_message",
                "description": "Post a message to a Matrix room at matrix.themultiverse.school",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel name (e.g., 'coordination', 'research')",
                        },
                        "agent": {
                            "type": "string",
                            "description": "Agent username posting the message",
                        },
                        "message": {
                            "type": "string",
                            "description": "Message content to post",
                        },
                        "status": {
                            "type": "string",
                            "description": "Optional status tag for the message",
                        },
                    },
                    "required": ["channel", "agent", "message"],
                },
            },
            {
                "type": "function",
                "name": "matrix_read_messages",
                "description": "Read recent messages from a Matrix room",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel name to read from",
                        },
                        "agent": {
                            "type": "string",
                            "description": "Agent username to use for authentication",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of recent messages to retrieve (default: 10)",
                        },
                    },
                    "required": ["channel", "agent"],
                },
            },
            {
                "type": "function",
                "name": "matrix_list_rooms",
                "description": "List all configured Matrix rooms and their mappings",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent": {
                            "type": "string",
                            "description": "Agent username to use for authentication (default: orchestrator)",
                        },
                    },
                    "required": [],
                },
            },
            {
                "type": "function",
                "name": "matrix_invite_user",
                "description": "Invite a user to a Matrix room",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel name where to invite the user",
                        },
                        "agent": {
                            "type": "string",
                            "description": "Agent username performing the invitation (must have invite permissions)",
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Matrix user ID to invite (e.g., '@user:domain.com')",
                        },
                    },
                    "required": ["channel", "agent", "user_id"],
                },
            },
            {
                "type": "function",
                "name": "matrix_check_membership",
                "description": "Check if a user is a member of a Matrix room",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel name to check",
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Matrix user ID to check",
                        },
                        "agent": {
                            "type": "string",
                            "description": "Agent username to use for authentication (default: orchestrator)",
                        },
                    },
                    "required": ["channel", "user_id"],
                },
            },
            {
                "type": "function",
                "name": "matrix_get_notifications",
                "description": "Get unread notification count for an agent across Matrix rooms",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent": {
                            "type": "string",
                            "description": "Agent username to check notifications for",
                        },
                        "channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional list of channel names to check (default: all configured channels)",
                        },
                    },
                    "required": ["agent"],
                },
            }
        ] # tools to use
        self.name = "Agent"
        self.system_prompt = f"""
        You are a helpful file system assistant with Matrix collaboration capabilities.
        Always check the current state of the file system before taking any action.
        If you need clarification or additional information from the user, use the contact_user tool.
        
        You can communicate via Matrix at matrix.themultiverse.school to:
        - Post messages to channels
        - Read messages from rooms
        - List available rooms
        - Invite users to rooms
        - Check room membership
        - Get notification counts
        
        You can use the following tools:
        {self.tools}
        """
        self.memory = [
            {"role": "system", "content": self.system_prompt}
            
        ] # memory to use
        
        
    def prompt(self, prompt):
        self.memory.append({"role": "user", "content": prompt})
        response = client.responses.create(
            model="gpt-5.1",
            tools=self.tools,
            input=self.memory
        )
        
        output = self.handle_tool_call(response.output)
        return response.output_text
        
    def handle_tool_call(self, output):
        
        self.memory += output
        
        for item in output:
            print(item)
            if item.type == "function_call":
                args = json.loads(item.arguments)
                result = None
                
                if item.name == "read_file":
                    # Execute the function logic for read_file
                    result = read_file(args.get("filepath"))
                    
                elif item.name == "write_file":
                    # Execute the function logic for write_file
                    result = write_file(args.get("filepath"), args.get("content"))
                    
                elif item.name == "list_directory":
                    # Execute the function logic for list_directory
                    result = list_directory(args.get("path"))
                
                elif item.name == "move_file":
                    # Execute the function logic for move_file
                    result = move_file(args.get("source_path"), args.get("destination_path"))
                
                elif item.name == "contact_user":
                    # Execute the function logic for contact_user
                    result = contact_user(args.get("message"))
                
                elif item.name == "make_directory":
                    # Execute the function logic for make_directory
                    result = make_directory(args.get("path"))
                
                elif item.name == "matrix_post_message":
                    # Execute the function logic for matrix_post_message
                    result = matrix_post_message(
                        args.get("channel"),
                        args.get("agent"),
                        args.get("message"),
                        args.get("status")
                    )
                
                elif item.name == "matrix_read_messages":
                    # Execute the function logic for matrix_read_messages
                    result = matrix_read_messages(
                        args.get("channel"),
                        args.get("agent"),
                        args.get("limit", 10)
                    )
                
                elif item.name == "matrix_list_rooms":
                    # Execute the function logic for matrix_list_rooms
                    result = matrix_list_rooms(args.get("agent", "orchestrator"))
                
                elif item.name == "matrix_invite_user":
                    # Execute the function logic for matrix_invite_user
                    result = matrix_invite_user(
                        args.get("channel"),
                        args.get("agent"),
                        args.get("user_id")
                    )
                
                elif item.name == "matrix_check_membership":
                    # Execute the function logic for matrix_check_membership
                    result = matrix_check_membership(
                        args.get("channel"),
                        args.get("user_id"),
                        args.get("agent", "orchestrator")
                    )
                
                elif item.name == "matrix_get_notifications":
                    # Execute the function logic for matrix_get_notifications
                    result = matrix_get_notifications(
                        args.get("agent"),
                        args.get("channels")
                    )
                
                # Provide function call results to the model
                if result is not None:
                    self.memory.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps({"result": result})
                    })
                    
            elif item.type == "text":
                self.memory.append({"role": "assistant", "content": item.content})
                

        response = client.responses.create(
            model="gpt-5.1",
            instructions="Respond with the results from the tool calls.",
            tools=self.tools,
            input=self.memory,
        )
        
        self.memory.append({"role": "assistant", "content": response.output_text})
        print(response.output_text)
        return response.output_text
    
    def run(self, user_input):
        keep_going = True
        self.goal = user_input
        self.memory.append({"role": "user", "content": user_input})
        while keep_going:
            ## interpret the user's request as the goal of the agent // orient
            ## prompt the agent to come up with a plan to achieve the goal (to think) // decide
            plan = self.prompt(self.system_prompt + "\n Determine a plan to achieve the user's goal. " + self.goal)
            
            ## generate a sequence of tool calls to achieve the goal // act
            tool_calls = self.prompt(self.system_prompt + "\n Generate a sequence of tool calls to achieve the steps in the plan:\n" + plan)
            ## is the goal achieved? if not, repeat the process
            is_goal_achieved = self.prompt(self.system_prompt + "\n Is the goal achieved? Respond with 'Yes' or 'No'. " + self.goal)
            if "yes" in is_goal_achieved.lower():
                keep_going = False
                summary = self.prompt(self.system_prompt + "\n Summarize the results of the tool calls and the goal achievement.")
                return summary
            if "no" in is_goal_achieved.lower():
                self.memory.append({"role": "user", "content": "What is the next step to achieve the goal?"})
       
        

agent = Agent()
agent.run("there are a lot of markdown files and other files in this. Can you organize this folder so that everything is organized into logical folders based on the content of the file other than the README")