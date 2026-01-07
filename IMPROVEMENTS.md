# 10 Concrete Improvements for Agent Modularity and Robustness

## 1. **Extract Tool Registry Pattern**
**Problem**: Tool definitions (lines 25-162) are hardcoded in `__init__`, and tool execution uses a long if/elif chain (lines 462-490), creating tight coupling.

**Solution**: Create a `ToolRegistry` class that maps tool names to handler functions:
```python
class ToolRegistry:
    def __init__(self):
        self._tools = {}
        self._handlers = {}
    
    def register(self, tool_def, handler_func):
        self._tools[tool_def["name"]] = tool_def
        self._handlers[tool_def["name"]] = handler_func
    
    def get_tool_definitions(self):
        return list(self._tools.values())
    
    def execute(self, tool_name, args):
        if tool_name not in self._handlers:
            raise ValueError(f"Unknown tool: {tool_name}")
        return self._handlers[tool_name](**args)
```

**Benefits**: Easy to add/remove tools, test handlers independently, and swap implementations.

---

## 2. **Separate Logging Module**
**Problem**: Uses `print()` statements throughout (lines 23, 250, 265, etc.), making it impossible to control log levels, redirect output, or disable logging.

**Solution**: Create a centralized logging module:
```python
import logging

class AgentLogger:
    def __init__(self, name="Agent", level=logging.INFO):
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(name)s] %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(level)
    
    def info(self, msg): self.logger.info(msg)
    def debug(self, msg): self.logger.debug(msg)
    def error(self, msg): self.logger.error(msg)
    def warning(self, msg): self.logger.warning(msg)
```

**Benefits**: Configurable log levels, file output, structured logging, easier debugging.

---

## 3. **Extract Path Validator to Utility Class**
**Problem**: `_validate_path()` (lines 211-246) is tightly coupled to the Agent class but could be reused elsewhere.

**Solution**: Create a standalone `PathValidator` class:
```python
class PathValidator:
    def __init__(self, allowed_directory):
        self.allowed_directory = os.path.realpath(allowed_directory)
    
    def validate(self, filepath):
        """Returns (is_valid, normalized_path, error_message)"""
        # Move validation logic here
        pass
```

**Benefits**: Reusable across modules, testable independently, can be swapped for different validation strategies.

---

## 4. **Separate Memory Management**
**Problem**: Memory handling is mixed with agent logic (lines 206-209, 442, 454, etc.), making it hard to persist, clear, or swap memory backends.

**Solution**: Create a `MemoryManager` class:
```python
class MemoryManager:
    def __init__(self, system_prompt):
        self.messages = [{"role": "system", "content": system_prompt}]
    
    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})
    
    def add_tool_output(self, call_id, output):
        self.messages.append({
            "type": "function_call_output",
            "call_id": call_id,
            "output": json.dumps({"result": output})
        })
    
    def get_messages(self):
        return self.messages.copy()
    
    def clear(self):
        self.messages = self.messages[:1]  # Keep system prompt
```

**Benefits**: Can swap for database-backed memory, implement memory limits, add conversation history management.

---

## 5. **Extract LLM Client Interface**
**Problem**: OpenAI client is global (line 2) and hardcoded model name "gpt-5.2" (lines 444, 505), making it impossible to swap providers or configure per-instance.

**Solution**: Create an `LLMClient` interface:
```python
class LLMClient:
    def __init__(self, model="gpt-4", api_key=None):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def create_response(self, messages, tools=None, instructions=None):
        kwargs = {
            "model": self.model,
            "input": messages
        }
        if tools:
            kwargs["tools"] = tools
        if instructions:
            kwargs["instructions"] = instructions
        return self.client.responses.create(**kwargs)
```

**Benefits**: Easy to swap providers (Anthropic, local models), configure per-agent, mock for testing.

---

## 6. **Extract Configuration Management**
**Problem**: Hardcoded values scattered throughout (timeout=30, model name, etc.), making it hard to configure without code changes.

**Solution**: Create a `Config` dataclass or use a config file:
```python
from dataclasses import dataclass

@dataclass
class AgentConfig:
    model: str = "gpt-4"
    default_timeout: int = 30
    max_iterations: int = 50
    working_directory: str = None
    log_level: str = "INFO"
    enable_background_processes: bool = True
```

**Benefits**: Centralized configuration, environment variable support, per-instance customization.

---

## 7. **Separate Tool Execution from Agent Logic**
**Problem**: Tool execution logic (lines 452-513) is embedded in the agent, making it hard to add retries, rate limiting, or async execution.

**Solution**: Create a `ToolExecutor` class:
```python
class ToolExecutor:
    def __init__(self, tool_registry, path_validator, logger):
        self.tool_registry = tool_registry
        self.path_validator = path_validator
        self.logger = logger
    
    def execute_tool_call(self, function_call_item):
        """Execute a single tool call with error handling"""
        try:
            args = json.loads(function_call_item.arguments)
            result = self.tool_registry.execute(function_call_item.name, args)
            return {"success": True, "result": result}
        except Exception as error:
            self.logger.error(f"Tool execution failed: {error}")
            return {"success": False, "error": str(error)}
    
    def process_tool_calls(self, output_items):
        """Process multiple tool calls and return results"""
        results = []
        for item in output_items:
            if item.type == "function_call":
                results.append(self.execute_tool_call(item))
        return results
```

**Benefits**: Can add retry logic, rate limiting, async execution, better error handling.

---

## 8. **Extract Run Loop Logic**
**Problem**: The `run()` method (lines 515-535) has complex control flow mixing planning, execution, and goal checking.

**Solution**: Create separate strategy classes:
```python
class PlanningStrategy:
    def create_plan(self, goal, context):
        """Generate a plan to achieve the goal"""
        pass

class ExecutionStrategy:
    def execute_plan(self, plan, context):
        """Execute tool calls based on plan"""
        pass

class GoalChecker:
    def is_achieved(self, goal, context):
        """Check if goal is achieved"""
        pass

class AgentRunLoop:
    def __init__(self, planner, executor, checker):
        self.planner = planner
        self.executor = executor
        self.checker = checker
    
    def run(self, goal, max_iterations=50):
        """Main run loop with strategy pattern"""
        for iteration in range(max_iterations):
            plan = self.planner.create_plan(goal, context)
            results = self.executor.execute_plan(plan, context)
            if self.checker.is_achieved(goal, context):
                return results
        raise MaxIterationsExceeded()
```

**Benefits**: Swappable strategies, easier testing, clearer separation of concerns.

---

## 9. **Create Custom Exception Hierarchy**
**Problem**: Returns error strings instead of raising exceptions (lines 254, 261, etc.), making error handling inconsistent and hard to debug.

**Solution**: Define custom exceptions:
```python
class AgentError(Exception):
    """Base exception for agent errors"""
    pass

class PathValidationError(AgentError):
    """Raised when path validation fails"""
    pass

class ToolExecutionError(AgentError):
    """Raised when tool execution fails"""
    pass

class MaxIterationsExceeded(AgentError):
    """Raised when run loop exceeds max iterations"""
    pass
```

**Benefits**: Better error handling, stack traces, easier debugging, consistent error propagation.

---

## 10. **Separate Background Process Manager**
**Problem**: Background process handling (lines 384-438) is embedded in the agent, making it hard to track, kill, or monitor processes.

**Solution**: Create a `ProcessManager` class:
```python
class ProcessManager:
    def __init__(self, working_directory, logger):
        self.working_directory = working_directory
        self.logger = logger
        self.processes = {}  # pid -> process_info
    
    def start_background(self, command, log_file=None):
        """Start background process and track it"""
        process = subprocess.Popen(...)
        self.processes[process.pid] = {
            "process": process,
            "command": command,
            "log_file": log_file,
            "started_at": datetime.now()
        }
        return process.pid
    
    def stop_process(self, pid):
        """Stop a tracked process"""
        if pid in self.processes:
            self.processes[pid]["process"].terminate()
            del self.processes[pid]
    
    def list_processes(self):
        """List all tracked processes"""
        return self.processes.copy()
    
    def cleanup(self):
        """Stop all tracked processes"""
        for pid in list(self.processes.keys()):
            self.stop_process(pid)
```

**Benefits**: Process lifecycle management, resource cleanup, monitoring capabilities, prevents zombie processes.

---

## Implementation Priority

1. **High Priority** (Core robustness):
   - #9 Custom Exceptions
   - #2 Logging Module
   - #6 Configuration Management

2. **Medium Priority** (Modularity):
   - #1 Tool Registry
   - #4 Memory Management
   - #5 LLM Client Interface

3. **Lower Priority** (Advanced features):
   - #3 Path Validator
   - #7 Tool Executor
   - #8 Run Loop Strategy
   - #10 Process Manager

## Additional Benefits

- **Testability**: Each component can be unit tested independently
- **Extensibility**: Easy to add new tools, strategies, or backends
- **Maintainability**: Clear separation of concerns
- **Reusability**: Components can be used in other agents
- **Debugging**: Better error messages and logging
- **Configuration**: Easy to customize without code changes
