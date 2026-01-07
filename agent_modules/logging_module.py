"""
Centralized logging module for the agent system.
"""

import logging
import sys
from typing import Optional


class AgentLogger:
    """Centralized logger for agent operations."""
    
    def __init__(self, name: str = "Agent", level: str = "INFO", log_file: Optional[str] = None):
        """
        Initialize the logger.
        
        Args:
            name: Logger name
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path to write logs to
        """
        self.logger = logging.getLogger(name)
        
        # Clear existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Set log level
        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter('[%(name)s] %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter(
                '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)
    
    def reasoning(self, message: str):
        """Log reasoning/thinking process (always shown)."""
        # Use info level but with special formatting
        self.logger.info(f"🧠 REASONING: {message}")
    
    def step(self, message: str):
        """Log step/progress information."""
        self.logger.info(f"📋 STEP: {message}")
    
    def tool_call(self, tool_name: str, args: dict):
        """Log tool call with arguments."""
        args_str = str(args)[:200] + "..." if len(str(args)) > 200 else str(args)
        self.logger.info(f"🔧 TOOL: {tool_name}({args_str})")
    
    def tool_result(self, tool_name: str, success: bool, result: any = None):
        """Log tool execution result."""
        status = "✓" if success else "✗"
        result_preview = str(result)[:150] + "..." if result and len(str(result)) > 150 else str(result)
        self.logger.info(f"{status} TOOL RESULT [{tool_name}]: {result_preview}")
    
    def plan(self, plan_text: str):
        """Log the plan."""
        # Show first 500 chars of plan
        preview = plan_text[:500] + "..." if len(plan_text) > 500 else plan_text
        self.logger.info(f"📝 PLAN:\n{preview}")
    
    def reflection(self, reflection_text: str):
        """Log reflection/reasoning."""
        preview = reflection_text[:300] + "..." if len(reflection_text) > 300 else reflection_text
        self.logger.info(f"💭 REFLECTION:\n{preview}")
    
    def status(self, message: str):
        """Log status update."""
        self.logger.info(f"📊 STATUS: {message}")
