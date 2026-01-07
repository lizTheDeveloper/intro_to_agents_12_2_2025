"""
Custom exception hierarchy for agent errors.
"""


class AgentError(Exception):
    """Base exception for all agent-related errors."""
    pass


class PathValidationError(AgentError):
    """Raised when path validation fails."""
    pass


class ToolExecutionError(AgentError):
    """Raised when tool execution fails."""
    pass


class MaxIterationsExceeded(AgentError):
    """Raised when run loop exceeds maximum iterations."""
    pass


class ConfigurationError(AgentError):
    """Raised when configuration is invalid."""
    pass


class ContextWindowError(AgentError):
    """Raised when context window is exceeded."""
    pass
