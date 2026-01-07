"""
Tool execution engine with error handling and retry logic.
"""

import json
from typing import List, Dict, Any, Optional
from .exceptions import ToolExecutionError
from .tool_registry import ToolRegistry
from .logging_module import AgentLogger


class ToolExecutor:
    """Executes tool calls with error handling."""
    
    def __init__(
        self,
        tool_registry: ToolRegistry,
        logger: AgentLogger,
        max_retries: int = 0
    ):
        """
        Initialize tool executor.
        
        Args:
            tool_registry: Registry containing tools and handlers
            logger: Logger instance
            max_retries: Maximum number of retries for failed executions
        """
        self.tool_registry = tool_registry
        self.logger = logger
        self.max_retries = max_retries
    
    def execute_tool_call(self, function_call_item: Any) -> Dict[str, Any]:
        """
        Execute a single tool call with error handling.
        
        Args:
            function_call_item: Function call item from LLM response
            
        Returns:
            Dictionary with success status and result or error
        """
        try:
            args = json.loads(function_call_item.arguments)
            tool_name = function_call_item.name
            
            self.logger.debug(f"Executing tool: {tool_name} with args: {args}")
            
            # Retry logic
            last_error = None
            for attempt in range(self.max_retries + 1):
                try:
                    result = self.tool_registry.execute(tool_name, args)
                    self.logger.debug(f"Tool {tool_name} executed successfully")
                    return {
                        "success": True,
                        "result": result,
                        "call_id": getattr(function_call_item, 'call_id', None)
                    }
                except Exception as error:
                    last_error = error
                    if attempt < self.max_retries:
                        self.logger.warning(
                            f"Tool {tool_name} failed (attempt {attempt + 1}/{self.max_retries + 1}): {error}"
                        )
                    else:
                        self.logger.error(f"Tool {tool_name} failed after {self.max_retries + 1} attempts: {error}")
            
            # Return error instead of raising
            error_msg = f"Tool execution failed: {last_error}"
            return {
                "success": False,
                "error": error_msg,
                "call_id": getattr(function_call_item, 'call_id', None)
            }
            
        except json.JSONDecodeError as error:
            error_msg = f"Failed to parse tool arguments: {error}"
            self.logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "call_id": getattr(function_call_item, 'call_id', None)
            }
        except ValueError as error:
            error_msg = f"Unknown tool or invalid arguments: {error}"
            self.logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "call_id": getattr(function_call_item, 'call_id', None)
            }
        except Exception as error:
            error_msg = f"Unexpected error executing tool: {error}"
            self.logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "call_id": getattr(function_call_item, 'call_id', None)
            }
    
    def process_tool_calls(self, output_items: List[Any]) -> List[Dict[str, Any]]:
        """
        Process multiple tool calls and return results.
        
        Args:
            output_items: List of output items from LLM response
            
        Returns:
            List of execution results
        """
        results = []
        for item in output_items:
            if hasattr(item, 'type') and item.type == "function_call":
                result = self.execute_tool_call(item)
                results.append(result)
        return results
