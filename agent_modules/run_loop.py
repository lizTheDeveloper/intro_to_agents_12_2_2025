"""
Run loop strategies for agent execution.
"""

from typing import Dict, Any, Optional
from .exceptions import MaxIterationsExceeded, ContextWindowError
from .memory_manager import MemoryManager
from .llm_client import LLMClient, ContextWindowError as LLMContextWindowError
from .tool_registry import ToolRegistry
from .logging_module import AgentLogger


class PlanningStrategy:
    """Strategy for creating plans to achieve goals."""
    
    def __init__(self, llm_client: LLMClient, memory_manager: MemoryManager, logger: AgentLogger):
        self.llm_client = llm_client
        self.memory_manager = memory_manager
        self.logger = logger
    
    def create_plan(self, goal: str, system_prompt: str) -> str:
        """
        Generate a plan to achieve the goal.
        
        Args:
            goal: The goal to achieve
            system_prompt: System prompt with context
            
        Returns:
            Plan text
        """
        prompt = f"{system_prompt}\n\nDetermine a plan to achieve the user's goal: {goal}"
        self.memory_manager.add_user_message(prompt)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                messages = self.memory_manager.get_messages()
                response = self.llm_client.create_response(messages)
                plan = self.llm_client.get_output_text(response)
                self.memory_manager.add_assistant_message(plan)
                self.logger.info("Plan created")
                return plan
            except (LLMContextWindowError, ContextWindowError) as error:
                self.logger.warning(f"Context window exceeded (attempt {attempt + 1}/{max_retries}), compressing memory...")
                # Force compression
                self.memory_manager._compress_memory()
                if attempt == max_retries - 1:
                    raise


class ExecutionStrategy:
    """Strategy for executing plans."""
    
    def __init__(
        self,
        llm_client: LLMClient,
        memory_manager: MemoryManager,
        tool_registry: ToolRegistry,
        tool_executor: Any,
        logger: AgentLogger
    ):
        self.llm_client = llm_client
        self.memory_manager = memory_manager
        self.tool_registry = tool_registry
        self.tool_executor = tool_executor
        self.logger = logger
    
    def execute_plan(self, plan: str, system_prompt: str) -> str:
        """
        Execute tool calls based on plan.
        
        Args:
            plan: The plan to execute
            system_prompt: System prompt with context
            
        Returns:
            Execution results text
        """
        prompt = f"{system_prompt}\n\nGenerate a sequence of tool calls to achieve the steps in the plan:\n{plan}"
        self.memory_manager.add_user_message(prompt)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                messages = self.memory_manager.get_messages()
                tools = self.tool_registry.get_tool_definitions()
                response = self.llm_client.create_response(messages, tools=tools)
                
                output_items = self.llm_client.get_output_items(response)
                self.memory_manager.add_raw_messages(output_items)
                
                # Process tool calls
                for item in output_items:
                    if hasattr(item, 'type'):
                        if item.type == "function_call":
                            result = self.tool_executor.execute_tool_call(item)
                            # Always add tool output, even if it failed
                            call_id = result.get("call_id", "")
                            if result.get("success"):
                                self.memory_manager.add_tool_output(call_id, result.get("result"))
                            else:
                                # Add error as tool output so LLM can see what went wrong
                                self.memory_manager.add_tool_output(call_id, {"error": result.get("error", "Unknown error")})
                        elif item.type == "text":
                            self.memory_manager.add_assistant_message(item.content)
                
                # Get final response
                messages = self.memory_manager.get_messages()
                final_response = self.llm_client.create_response(
                    messages,
                    tools=tools,
                    instructions="Respond with the results from the tool calls."
                )
                result_text = self.llm_client.get_output_text(final_response)
                self.memory_manager.add_assistant_message(result_text)
                
                self.logger.info("Plan executed")
                return result_text
            except (LLMContextWindowError, ContextWindowError) as error:
                self.logger.warning(f"Context window exceeded during execution (attempt {attempt + 1}/{max_retries}), compressing memory...")
                # Force compression
                self.memory_manager._compress_memory()
                if attempt == max_retries - 1:
                    raise


class GoalChecker:
    """Strategy for checking if goals are achieved."""
    
    def __init__(self, llm_client: LLMClient, memory_manager: MemoryManager, logger: AgentLogger):
        self.llm_client = llm_client
        self.memory_manager = memory_manager
        self.logger = logger
    
    def is_achieved(self, goal: str, system_prompt: str) -> bool:
        """
        Check if goal is achieved.
        
        Args:
            goal: The goal to check
            system_prompt: System prompt with context
            
        Returns:
            True if goal is achieved, False otherwise
        """
        prompt = f"{system_prompt}\n\nIs the goal achieved? Respond with 'Yes' or 'No'. Goal: {goal}"
        self.memory_manager.add_user_message(prompt)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                messages = self.memory_manager.get_messages()
                response = self.llm_client.create_response(messages)
                response_text = self.llm_client.get_output_text(response)
                
                self.memory_manager.add_assistant_message(response_text)
                
                is_achieved = "yes" in response_text.lower()
                self.logger.info(f"Goal check: {'Achieved' if is_achieved else 'Not achieved'}")
                return is_achieved
            except (LLMContextWindowError, ContextWindowError) as error:
                self.logger.warning(f"Context window exceeded during goal check (attempt {attempt + 1}/{max_retries}), compressing memory...")
                # Force compression
                self.memory_manager._compress_memory()
                if attempt == max_retries - 1:
                    raise


class AgentRunLoop:
    """Main run loop orchestrator."""
    
    def __init__(
        self,
        planner: PlanningStrategy,
        executor: ExecutionStrategy,
        checker: GoalChecker,
        memory_manager: MemoryManager,
        logger: AgentLogger,
        max_iterations: int = 50
    ):
        self.planner = planner
        self.executor = executor
        self.checker = checker
        self.memory_manager = memory_manager
        self.logger = logger
        self.max_iterations = max_iterations
    
    def run(self, goal: str, system_prompt: str) -> str:
        """
        Main run loop.
        
        Args:
            goal: The goal to achieve
            system_prompt: System prompt with context
            
        Returns:
            Final summary of results
            
        Raises:
            MaxIterationsExceeded: If max iterations exceeded
        """
        self.memory_manager.add_user_message(goal)
        
        for iteration in range(self.max_iterations):
            self.logger.info(f"Iteration {iteration + 1}/{self.max_iterations}")
            
            # Plan
            plan = self.planner.create_plan(goal, system_prompt)
            
            # Execute
            execution_results = self.executor.execute_plan(plan, system_prompt)
            
            # Check if goal achieved
            if self.checker.is_achieved(goal, system_prompt):
                # Generate summary
                summary_prompt = f"{system_prompt}\n\nSummarize the results of the tool calls and the goal achievement."
                self.memory_manager.add_user_message(summary_prompt)
                messages = self.memory_manager.get_messages()
                response = self.planner.llm_client.create_response(messages)
                summary = self.planner.llm_client.get_output_text(response)
                self.memory_manager.add_assistant_message(summary)
                
                self.logger.info("Goal achieved!")
                return summary
            
            # Reflect and continue
            reflection_prompt = f"{system_prompt}\n\nReflect on the actions taken and the results achieved. What is the next step to achieve the goal?"
            self.memory_manager.add_user_message(reflection_prompt)
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    messages = self.memory_manager.get_messages()
                    response = self.planner.llm_client.create_response(messages)
                    reflection = self.planner.llm_client.get_output_text(response)
                    self.memory_manager.add_assistant_message(reflection)
                    break
                except (LLMContextWindowError, ContextWindowError) as error:
                    self.logger.warning(f"Context window exceeded during reflection (attempt {attempt + 1}/{max_retries}), compressing memory...")
                    # Force compression
                    self.memory_manager._compress_memory()
                    if attempt == max_retries - 1:
                        raise
        
        raise MaxIterationsExceeded(f"Maximum iterations ({self.max_iterations}) exceeded")
