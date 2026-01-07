"""
Configuration management for the agent system.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AgentConfig:
    """Configuration for agent instances."""
    
    model: str = "gpt-4"
    default_timeout: int = 30
    max_iterations: int = 50
    working_directory: Optional[str] = None
    log_level: str = "INFO"
    enable_background_processes: bool = True
    api_key: Optional[str] = None
    log_file: Optional[str] = None
    verbose: bool = False
    save_conversation: bool = True
    conversation_file: Optional[str] = None
    
    def __post_init__(self):
        """Validate and set defaults after initialization."""
        # Set working directory from environment if not provided
        if self.working_directory is None:
            self.working_directory = os.getcwd()
        
        # Set API key from environment if not provided
        if self.api_key is None:
            self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Validate log level
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {self.log_level}. Must be one of {valid_levels}")
        
        # Validate timeout
        if self.default_timeout <= 0:
            raise ValueError("default_timeout must be positive")
        
        # Validate max_iterations
        if self.max_iterations <= 0:
            raise ValueError("max_iterations must be positive")
    
    @classmethod
    def from_env(cls) -> 'AgentConfig':
        """Create config from environment variables."""
        return cls(
            model=os.getenv("AGENT_MODEL", "gpt-4"),
            default_timeout=int(os.getenv("AGENT_TIMEOUT", "30")),
            max_iterations=int(os.getenv("AGENT_MAX_ITERATIONS", "50")),
            working_directory=os.getenv("AGENT_WORKING_DIRECTORY"),
            log_level=os.getenv("AGENT_LOG_LEVEL", "INFO"),
            enable_background_processes=os.getenv("AGENT_ENABLE_BACKGROUND", "true").lower() == "true",
            api_key=os.getenv("OPENAI_API_KEY"),
            log_file=os.getenv("AGENT_LOG_FILE"),
        )
