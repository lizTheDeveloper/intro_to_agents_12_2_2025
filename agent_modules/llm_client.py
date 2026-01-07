"""
LLM client interface for abstracting different providers.
"""

from openai import OpenAI
from typing import List, Dict, Any, Optional
from .exceptions import AgentError


class ContextWindowError(AgentError):
    """Raised when context window is exceeded."""
    pass


class LLMClient:
    """Interface for LLM providers."""
    
    def __init__(self, model: str = "gpt-4", api_key: Optional[str] = None):
        """
        Initialize LLM client.
        
        Args:
            model: Model name to use
            api_key: Optional API key (uses default OpenAI client if not provided)
        """
        self.model = model
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
    
    def create_response(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        instructions: Optional[str] = None
    ) -> Any:
        """
        Create a response from the LLM.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            instructions: Optional instruction string
            
        Returns:
            Response object from the LLM
            
        Raises:
            ContextWindowError: If context window is exceeded
        """
        kwargs = {
            "model": self.model,
            "input": messages
        }
        
        if tools:
            kwargs["tools"] = tools
        
        if instructions:
            kwargs["instructions"] = instructions
        
        try:
            return self.client.responses.create(**kwargs)
        except Exception as error:
            error_str = str(error)
            if "context_length_exceeded" in error_str or "context window" in error_str.lower():
                raise ContextWindowError(f"Context window exceeded: {error}") from error
            raise
    
    def get_output_text(self, response: Any) -> str:
        """Extract output text from response."""
        return response.output_text
    
    def get_output_items(self, response: Any) -> List[Any]:
        """Extract output items from response."""
        return response.output
