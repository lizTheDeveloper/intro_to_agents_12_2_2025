from openai import OpenAI
client = OpenAI()
import json 
import os

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
            }
        ] # tools to use
        self.name = "Agent"
        self.system_prompt = f"""
        You are a helpful file system assistant.
        Don't ask the user clarifying questions as they do not have an interactive terminal.
        Always check the current state of the file system before taking any action.
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