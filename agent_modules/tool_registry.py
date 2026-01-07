"""
Tool registry for managing agent tools and their handlers.
"""

from typing import Dict, Callable, List, Any


class ToolRegistry:
    """Registry for managing tools and their execution handlers."""
    
    def __init__(self):
        """Initialize empty tool registry."""
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._handlers: Dict[str, Callable] = {}
    
    def register(self, tool_def: Dict[str, Any], handler_func: Callable):
        """
        Register a tool with its handler.
        
        Args:
            tool_def: Tool definition dictionary (must have "name" key)
            handler_func: Function to call when tool is executed
        """
        tool_name = tool_def.get("name")
        if not tool_name:
            raise ValueError("Tool definition must have a 'name' field")
        
        self._tools[tool_name] = tool_def
        self._handlers[tool_name] = handler_func
    
    def register_multiple(self, tools: List[Tuple[Dict[str, Any], Callable]]):
        """
        Register multiple tools at once.
        
        Args:
            tools: List of (tool_def, handler_func) tuples
        """
        for tool_def, handler_func in tools:
            self.register(tool_def, handler_func)
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get list of all tool definitions."""
        return list(self._tools.values())
    
    def get_tool(self, tool_name: str) -> Dict[str, Any]:
        """Get tool definition by name."""
        if tool_name not in self._tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        return self._tools[tool_name]
    
    def execute(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """
        Execute a tool by name with given arguments.
        
        Args:
            tool_name: Name of the tool to execute
            args: Arguments to pass to the tool handler
            
        Returns:
            Result from tool execution
        """
        if tool_name not in self._handlers:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        handler = self._handlers[tool_name]
        return handler(**args)
    
    def has_tool(self, tool_name: str) -> bool:
        """Check if a tool is registered."""
        return tool_name in self._tools
    
    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
