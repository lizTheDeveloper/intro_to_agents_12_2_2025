"""
Improved modular agentic agent with separated concerns.
"""

import os
import subprocess
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agent_modules import (
    AgentError,
    PathValidationError,
    ToolExecutionError,
    MaxIterationsExceeded,
    AgentLogger,
    AgentConfig,
    PathValidator,
    MemoryManager,
    LLMClient,
    ToolRegistry,
    ToolExecutor,
    ProcessManager,
    PlanningStrategy,
    ExecutionStrategy,
    GoalChecker,
    AgentRunLoop,
)
from agent_modules.default_tools import get_default_tool_definitions


class Agent:
    """Modular agentic agent with separated concerns."""
    
    def __init__(self, working_directory: Optional[str] = None, config: Optional[AgentConfig] = None):
        """
        Initialize agent with modular components.
        
        Args:
            working_directory: Working directory for agent operations
            config: Optional configuration (uses defaults if not provided)
        """
        # Initialize configuration
        if config is None:
            config = AgentConfig()
            if working_directory:
                config.working_directory = working_directory
        
        if config.working_directory is None:
            config.working_directory = os.getcwd()
        
        self.config = config
        self.working_directory = os.path.realpath(config.working_directory)
        
        # Validate working directory
        if not os.path.exists(self.working_directory):
            raise ValueError(f"Working directory does not exist: {self.working_directory}")
        if not os.path.isdir(self.working_directory):
            raise ValueError(f"Working directory is not a directory: {self.working_directory}")
        
        # Initialize logger
        self.logger = AgentLogger(
            name="Agent",
            level=config.log_level,
            log_file=config.log_file
        )
        self.logger.info(f"Agent initialized with restricted access to: {self.working_directory}")
        
        # Initialize path validator
        self.path_validator = PathValidator(self.working_directory)
        
        # Initialize process manager
        self.process_manager = ProcessManager(
            self.working_directory,
            self.path_validator,
            self.logger
        )
        
        # Initialize LLM client
        self.llm_client = LLMClient(
            model=config.model,
            api_key=config.api_key
        )
        
        # Initialize tool registry and register default tools (before building system prompt)
        self.tool_registry = ToolRegistry()
        self._register_default_tools()
        
        # Build system prompt (after tools are registered)
        self.system_prompt = self._build_system_prompt()
        
        # Initialize memory manager with compression settings
        self.memory_manager = MemoryManager(
            self.system_prompt,
            max_messages=25,  # Lower threshold to prevent context overflow
            compress_threshold=15  # Compress when we have 15+ messages (more aggressive)
        )
        
        # Initialize tool executor
        self.tool_executor = ToolExecutor(
            self.tool_registry,
            self.logger
        )
        
        # Initialize run loop strategies
        self.planner = PlanningStrategy(
            self.llm_client,
            self.memory_manager,
            self.logger
        )
        
        self.executor = ExecutionStrategy(
            self.llm_client,
            self.memory_manager,
            self.tool_registry,
            self.tool_executor,
            self.logger
        )
        
        self.goal_checker = GoalChecker(
            self.llm_client,
            self.memory_manager,
            self.logger
        )
        
        self.run_loop = AgentRunLoop(
            self.planner,
            self.executor,
            self.goal_checker,
            self.memory_manager,
            self.logger,
            max_iterations=config.max_iterations
        )
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt with context."""
        tools_list = self.tool_registry.get_tool_definitions() if hasattr(self, 'tool_registry') else []
        
        return f"""
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
        """
    
    def _register_default_tools(self):
        """Register default tools with their handlers."""
        tool_defs = get_default_tool_definitions()
        
        # Define tool handlers
        handlers = {
            "read_file": self._read_file,
            "write_file": self._write_file,
            "list_directory": self._list_directory,
            "move_file": self._move_file,
            "contact_user": self._contact_user,
            "make_directory": self._make_directory,
            "execute_command": self._execute_command,
            "execute_background_command": self._execute_background_command,
        }
        
        # Register each tool
        for tool_def in tool_defs:
            tool_name = tool_def["name"]
            if tool_name in handlers:
                self.tool_registry.register(tool_def, handlers[tool_name])
    
    def _read_file(self, filepath: str) -> str:
        """Read the contents of a file."""
        self.logger.info(f"Reading file: {filepath}")
        
        try:
            normalized_path = self.path_validator.validate_and_raise(filepath)
            with open(normalized_path, 'r') as file:
                content = file.read()
            return content
        except PathValidationError as error:
            raise ToolExecutionError(f"Path validation failed: {error}") from error
        except Exception as error:
            raise ToolExecutionError(f"Error reading file: {error}") from error
    
    def _write_file(self, filepath: str, content: str) -> str:
        """Write content to a file."""
        self.logger.info(f"Writing to file: {filepath}")
        
        try:
            normalized_path = self.path_validator.validate_and_raise(filepath)
            
            # Create parent directory if it doesn't exist
            parent_dir = os.path.dirname(normalized_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            
            with open(normalized_path, 'w') as file:
                file.write(content)
            return f"Successfully wrote to {filepath}"
        except PathValidationError as error:
            raise ToolExecutionError(f"Path validation failed: {error}") from error
        except Exception as error:
            raise ToolExecutionError(f"Error writing file: {error}") from error
    
    def _list_directory(self, path: str) -> dict:
        """List all files and directories in the specified path."""
        self.logger.info(f"Listing directory: {path}")
        
        try:
            normalized_path = self.path_validator.validate_and_raise(path)
            entries = os.listdir(normalized_path)
            return {"entries": entries, "count": len(entries)}
        except PathValidationError as error:
            raise ToolExecutionError(f"Path validation failed: {error}") from error
        except Exception as error:
            raise ToolExecutionError(f"Error listing directory: {error}") from error
    
    def _move_file(self, source_path: str, destination_path: str) -> str:
        """Move or rename a file."""
        self.logger.info(f"Moving file from {source_path} to {destination_path}")
        
        try:
            normalized_source = self.path_validator.validate_and_raise(source_path)
            normalized_dest = self.path_validator.validate_and_raise(destination_path)
            
            # Create parent directory for destination if it doesn't exist
            dest_parent = os.path.dirname(normalized_dest)
            if dest_parent and not os.path.exists(dest_parent):
                os.makedirs(dest_parent, exist_ok=True)
            
            os.rename(normalized_source, normalized_dest)
            return f"Successfully moved {source_path} to {destination_path}"
        except PathValidationError as error:
            raise ToolExecutionError(f"Path validation failed: {error}") from error
        except Exception as error:
            raise ToolExecutionError(f"Error moving file: {error}") from error
    
    def _contact_user(self, message: str) -> str:
        """Contact the user to request information or clarification."""
        self.logger.info(f"\n[Agent contacting user]: {message}")
        user_response = input("Your response: ")
        return user_response
    
    def _make_directory(self, path: str) -> str:
        """Create a new directory."""
        self.logger.info(f"Creating directory: {path}")
        
        try:
            normalized_path = self.path_validator.validate_and_raise(path)
            os.makedirs(normalized_path, exist_ok=True)
            return f"Successfully created directory {path}"
        except PathValidationError as error:
            raise ToolExecutionError(f"Path validation failed: {error}") from error
        except Exception as error:
            raise ToolExecutionError(f"Error creating directory: {error}") from error
    
    def _execute_command(self, command: str, timeout: Optional[int] = None) -> dict:
        """Execute a terminal command."""
        if timeout is None:
            timeout = self.config.default_timeout
        
        self.logger.info(f"Executing command: {command}")
        
        try:
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
                self.logger.info(f"✓ Command succeeded (exit code: 0)")
            else:
                self.logger.warning(f"✗ Command failed (exit code: {result.returncode})")
            
            return output
            
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out after {timeout} seconds"
            self.logger.error(error_msg)
            return {
                "command": command,
                "error": error_msg,
                "working_directory": self.working_directory
            }
        except Exception as error:
            error_msg = f"Error executing command: {error}"
            self.logger.error(error_msg)
            return {
                "command": command,
                "error": error_msg,
                "working_directory": self.working_directory
            }
    
    def _execute_background_command(self, command: str, log_file: Optional[str] = None) -> dict:
        """Execute a terminal command in the background."""
        if not self.config.enable_background_processes:
            raise ToolExecutionError("Background processes are disabled")
        
        return self.process_manager.start_background(command, log_file)
    
    def run(self, user_input: str) -> str:
        """
        Run the agent with a user goal.
        
        Args:
            user_input: The goal or task for the agent
            
        Returns:
            Summary of results
            
        Raises:
            MaxIterationsExceeded: If max iterations exceeded
        """
        try:
            return self.run_loop.run(user_input, self.system_prompt)
        except MaxIterationsExceeded as error:
            self.logger.error(str(error))
            raise
        finally:
            # Cleanup background processes
            if self.config.enable_background_processes:
                self.process_manager.cleanup()
    
    def cleanup(self):
        """Cleanup resources."""
        if self.config.enable_background_processes:
            self.process_manager.cleanup()


# Example usage with restricted directory access
if __name__ == "__main__":
    # Initialize agent with restricted access to current directory
    # You can specify a different directory by passing it as an argument:
    # agent = Agent(working_directory="/path/to/restricted/folder")
    
    agent = Agent(working_directory="/Users/annhoward/intro_to_agents_12_2_2025/team_formation_agent/workdir2")
    agent.run("https://mtgjson.com/getting-started/ - using this api, we want to solve the team formation problem with a mtg deck creator. Create a software system that can produce decks that are playable, competitive, and fun. Select strategies that work together, and write an evolutionary testing algorithm to test the decks. Your role is as chief data scientist and you will be responsible for the design, implementation, and testing of the software system and the evolutionary testing algorithm. First write an openspec spec and implement the software system and the evolutionary testing algorithm.")
