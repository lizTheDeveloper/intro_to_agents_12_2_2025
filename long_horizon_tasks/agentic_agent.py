from openai import OpenAI
client = OpenAI()
import json 
import os
import subprocess
import shlex


class Agent:
    def __init__(self, working_directory=None):
        # Set the working directory - if None, use current directory
        if working_directory is None:
            self.working_directory = os.getcwd()
        else:
            self.working_directory = os.path.realpath(working_directory)
            
        # Validate that the working directory exists
        if not os.path.exists(self.working_directory):
            raise ValueError(f"Working directory does not exist: {self.working_directory}")
        if not os.path.isdir(self.working_directory):
            raise ValueError(f"Working directory is not a directory: {self.working_directory}")
        
        print(f"[Agent initialized with restricted access to: {self.working_directory}]")
        
        self.tools = [
            {
                "type": "function",
                "name": "read_file",
                "description": "Read the contents of a file at the specified filepath. Paths can be relative to the working directory or absolute (but must be within the allowed directory).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "The path to the file to read (relative or absolute)",
                        },
                    },
                    "required": ["filepath"],
                },
            },
            {
                "type": "function",
                "name": "write_file",
                "description": "Write content to a file at the specified filepath. Paths can be relative to the working directory or absolute (but must be within the allowed directory).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "The path to the file to write to (relative or absolute)",
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
                "description": "List all files and directories in the specified path. Paths can be relative to the working directory or absolute (but must be within the allowed directory).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The directory path to list contents from (relative or absolute)",
                        },
                    },
                    "required": ["path"],
                },
            },
            {
                "type": "function",
                "name": "move_file",
                "description": "Move or rename a file from source path to destination path. Both paths must be within the allowed directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source_path": {
                            "type": "string",
                            "description": "The current path of the file to move (relative or absolute)",
                        },
                        "destination_path": {
                            "type": "string",
                            "description": "The new path where the file should be moved to (relative or absolute)",
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
                "description": "Create a new directory at the specified path. Creates parent directories if they don't exist. Path must be within the allowed directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path where the directory should be created (relative or absolute)",
                        },
                    },
                    "required": ["path"],
                },
            },
            {
                "type": "function",
                "name": "execute_command",
                "description": "Execute a terminal command in the working directory. Returns stdout, stderr, and exit code. Use for commands that complete quickly (< 30 seconds).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The command to execute (e.g., 'ls -la', 'python script.py', 'grep pattern file.txt')",
                        },
                        "timeout": {
                            "type": "number",
                            "description": "Maximum execution time in seconds (default: 30)",
                        },
                    },
                    "required": ["command"],
                },
            },
            {
                "type": "function",
                "name": "execute_background_command",
                "description": "Execute a terminal command in the background (non-blocking). Use for long-running processes like web servers, watchers, etc. Returns immediately with the process ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The command to execute in the background (e.g., 'python -m http.server 8000', 'npm run dev')",
                        },
                        "log_file": {
                            "type": "string",
                            "description": "Optional path to redirect stdout/stderr (relative to working directory)",
                        },
                    },
                    "required": ["command"],
                },
            }
        ] # tools to use
        self.name = "Agent"
        self.system_prompt = f"""
        You are an agent with restricted access to: {self.working_directory}
        <!-- OPENSPEC:START -->
        # OpenSpec Instructions

        These instructions are for AI assistants working in this project.

        Always open `@/openspec/AGENTS.md` when the request:
        - Mentions planning or proposals (words like proposal, spec, change, plan)
        - Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
        - Sounds ambiguous and you need the authoritative spec before coding

        Use `@/openspec/AGENTS.md` to learn:
        - How to create and apply change proposals
        - Spec format and conventions
        - Project structure and guidelines

        Keep this managed block so 'openspec update' can refresh the instructions.

        <!-- OPENSPEC:END -->
        
        
        IMPORTANT SECURITY RESTRICTIONS:
        - You can ONLY access files and directories within your working directory
        - All file paths (relative or absolute) must resolve to locations within this directory
        - Attempts to access paths outside this directory will be blocked
        - All terminal commands execute in the working directory context
        
        AVAILABLE CAPABILITIES:
        - File operations: read, write, move, list directories, create directories
        - Terminal commands: execute commands synchronously or in the background
        - User interaction: contact user for clarification
        
        Always check the current state of the file system before taking any action.
        If you need clarification or additional information from the user, use the contact_user tool.
        
        For commands that take a long time (web servers, dev servers, watchers), use execute_background_command.
        For quick commands (ls, grep, python script.py), use execute_command.
        
        You can use the following tools:
        {self.tools}
        """
        self.memory = [
            {"role": "system", "content": self.system_prompt}
            
        ] # memory to use
    
    def _validate_path(self, filepath):
        """
        Validates that a filepath is within the allowed directory.
        Prevents path traversal attacks and unauthorized file access.
        
        Args:
            filepath: The path to validate (can be relative or absolute)
            
        Returns:
            tuple: (is_valid: bool, normalized_path: str or None, error_message: str or None)
        """
        try:
            # Resolve to absolute paths and normalize (removes .., symlinks, etc.)
            abs_allowed_dir = os.path.realpath(self.working_directory)
            
            # If filepath is relative, join it with working_directory first
            if not os.path.isabs(filepath):
                filepath = os.path.join(self.working_directory, filepath)
            
            abs_filepath = os.path.realpath(filepath)
            
            # Check if the filepath is within the allowed directory
            # os.path.commonpath returns the longest common sub-path
            try:
                common_path = os.path.commonpath([abs_allowed_dir, abs_filepath])
            except ValueError:
                # Different drives on Windows
                return False, None, f"Access denied: Path is outside allowed directory"
            
            if common_path != abs_allowed_dir:
                return False, None, f"Access denied: Path '{filepath}' is outside allowed directory '{self.working_directory}'"
            
            return True, abs_filepath, None
            
        except Exception as error:
            return False, None, f"Path validation error: {str(error)}"
    
    def _read_file(self, filepath):
        """Read the contents of a file at the specified filepath."""
        print(f"Reading file: {filepath}")
        
        is_valid, normalized_path, error_msg = self._validate_path(filepath)
        if not is_valid:
            return error_msg
        
        try:
            with open(normalized_path, 'r') as file:
                content = file.read()
            return content
        except Exception as error:
            return f"Error reading file: {str(error)}"
    
    def _write_file(self, filepath, content):
        """Write content to a file at the specified filepath."""
        print(f"Writing to file: {filepath}")
        
        is_valid, normalized_path, error_msg = self._validate_path(filepath)
        if not is_valid:
            return error_msg
        
        try:
            # Create parent directory if it doesn't exist
            parent_dir = os.path.dirname(normalized_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
                
            with open(normalized_path, 'w') as file:
                file.write(content)
            return f"Successfully wrote to {filepath}"
        except Exception as error:
            return f"Error writing file: {str(error)}"
    
    def _list_directory(self, path):
        """List all files and directories in the specified path."""
        print(f"Listing directory: {path}")
        
        is_valid, normalized_path, error_msg = self._validate_path(path)
        if not is_valid:
            return error_msg
        
        try:
            entries = os.listdir(normalized_path)
            return {"entries": entries, "count": len(entries)}
        except Exception as error:
            return f"Error listing directory: {str(error)}"
    
    def _move_file(self, source_path, destination_path):
        """Move or rename a file from source path to destination path."""
        print(f"Moving file from {source_path} to {destination_path}")
        
        # Validate both source and destination paths
        is_valid_source, normalized_source, error_msg_source = self._validate_path(source_path)
        if not is_valid_source:
            return error_msg_source
        
        is_valid_dest, normalized_dest, error_msg_dest = self._validate_path(destination_path)
        if not is_valid_dest:
            return error_msg_dest
        
        try:
            # Create parent directory for destination if it doesn't exist
            dest_parent = os.path.dirname(normalized_dest)
            if dest_parent and not os.path.exists(dest_parent):
                os.makedirs(dest_parent, exist_ok=True)
                
            os.rename(normalized_source, normalized_dest)
            return f"Successfully moved {source_path} to {destination_path}"
        except Exception as error:
            return f"Error moving file: {str(error)}"
    
    def _contact_user(self, message):
        """Contact the user to request information or clarification."""
        print(f"\n[Agent contacting user]: {message}")
        user_response = input("Your response: ")
        return user_response
    
    def _make_directory(self, path):
        """Create a new directory at the specified path."""
        print(f"Creating directory: {path}")
        
        is_valid, normalized_path, error_msg = self._validate_path(path)
        if not is_valid:
            return error_msg
        
        try:
            os.makedirs(normalized_path, exist_ok=True)
            return f"Successfully created directory {path}"
        except Exception as error:
            return f"Error creating directory: {str(error)}"
    
    def _execute_command(self, command, timeout=30):
        """Execute a terminal command in the working directory."""
        print(f"Executing command: {command}")
        
        try:
            # Execute the command in the working directory with a timeout
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = {
                "command": command,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "working_directory": self.working_directory
            }
            
            if result.returncode == 0:
                print(f"✓ Command succeeded (exit code: 0)")
            else:
                print(f"✗ Command failed (exit code: {result.returncode})")
            
            return output
            
        except subprocess.TimeoutExpired:
            return {
                "command": command,
                "error": f"Command timed out after {timeout} seconds",
                "working_directory": self.working_directory
            }
        except Exception as error:
            return {
                "command": command,
                "error": f"Error executing command: {str(error)}",
                "working_directory": self.working_directory
            }
    
    def _execute_background_command(self, command, log_file=None):
        """Execute a terminal command in the background."""
        print(f"Starting background command: {command}")
        
        try:
            # Validate log file path if provided
            if log_file:
                is_valid, normalized_log_path, error_msg = self._validate_path(log_file)
                if not is_valid:
                    return {"error": error_msg}
                
                # Create parent directory for log file if needed
                log_dir = os.path.dirname(normalized_log_path)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)
                
                # Open log file for writing
                log_file_handle = open(normalized_log_path, 'w')
                stdout_dest = log_file_handle
                stderr_dest = log_file_handle
            else:
                log_file_handle = None
                stdout_dest = subprocess.DEVNULL
                stderr_dest = subprocess.DEVNULL
            
            # Start the process in the background
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=self.working_directory,
                stdout=stdout_dest,
                stderr=stderr_dest,
                start_new_session=True  # Detach from parent process
            )
            
            output = {
                "command": command,
                "pid": process.pid,
                "working_directory": self.working_directory,
                "log_file": log_file if log_file else None,
                "message": f"Process started in background with PID {process.pid}"
            }
            
            print(f"✓ Background process started (PID: {process.pid})")
            if log_file:
                print(f"  Output redirected to: {log_file}")
            
            return output
            
        except Exception as error:
            return {
                "command": command,
                "error": f"Error starting background command: {str(error)}",
                "working_directory": self.working_directory
            }
        
        
    def prompt(self, prompt):
        self.memory.append({"role": "user", "content": prompt})
        response = client.responses.create(
            model="gpt-5.2",
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
                    result = self._read_file(args.get("filepath"))
                    
                elif item.name == "write_file":
                    result = self._write_file(args.get("filepath"), args.get("content"))
                    
                elif item.name == "list_directory":
                    result = self._list_directory(args.get("path"))
                
                elif item.name == "move_file":
                    result = self._move_file(args.get("source_path"), args.get("destination_path"))
                
                elif item.name == "contact_user":
                    result = self._contact_user(args.get("message"))
                
                elif item.name == "make_directory":
                    result = self._make_directory(args.get("path"))
                
                elif item.name == "execute_command":
                    result = self._execute_command(
                        args.get("command"),
                        args.get("timeout", 30)
                    )
                
                elif item.name == "execute_background_command":
                    result = self._execute_background_command(
                        args.get("command"),
                        args.get("log_file")
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
            model="gpt-5.2",
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
                reflection = self.prompt(self.system_prompt + "\n Reflect on the actions taken and the results achieved. What is the next step to achieve the goal?")
                self.memory.append({"role": "assistant", "content": reflection})
                
       
        

# Example usage with restricted directory access
if __name__ == "__main__":
    # Initialize agent with restricted access to current directory
    # You can specify a different directory by passing it as an argument:
    # agent = Agent(working_directory="/path/to/restricted/folder")
    
    agent = Agent(working_directory="/Users/annhoward/intro_to_agents_12_2_2025/long_horizon_tasks/workdir")
    agent.run("Implement all specs and write tests for everything that we build and test that it works.")

