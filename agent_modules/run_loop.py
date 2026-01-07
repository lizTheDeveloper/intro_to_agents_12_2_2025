"""
Run loop strategies for agent execution.
"""

from typing import Dict, Any, Optional
from .exceptions import MaxIterationsExceeded, ContextWindowError
from .memory_manager import MemoryManager
from .llm_client import LLMClient, ContextWindowError as LLMContextWindowError
from .tool_registry import ToolRegistry
from .logging_module import AgentLogger
from .progress_tracker import ProgressTracker


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
        self.logger.reasoning(f"Creating plan to achieve goal: {goal[:100]}...")
        prompt = f"{system_prompt}\n\nDetermine a plan to achieve the user's goal: {goal}"
        self.memory_manager.add_user_message(prompt)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                messages = self.memory_manager.get_messages()
                self.logger.debug(f"Requesting plan from LLM (attempt {attempt + 1})...")
                response = self.llm_client.create_response(messages)
                plan = self.llm_client.get_output_text(response)
                self.memory_manager.add_assistant_message(plan)
                self.logger.plan(plan)
                self.logger.step("Plan created successfully")
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
                tool_call_count = 0
                for item in output_items:
                    if hasattr(item, 'type'):
                        if item.type == "function_call":
                            tool_call_count += 1
                            tool_name = getattr(item, 'name', 'unknown')
                            try:
                                import json
                                args = json.loads(getattr(item, 'arguments', '{}'))
                            except:
                                args = {}
                            
                            self.logger.tool_call(tool_name, args)
                            result = self.tool_executor.execute_tool_call(item)
                            
                            # Always add tool output, even if it failed
                            call_id = result.get("call_id", "")
                            success = result.get("success", False)
                            result_data = result.get("result") if success else result.get("error", "Unknown error")
                            
                            self.logger.tool_result(tool_name, success, result_data)
                            
                            if success:
                                self.memory_manager.add_tool_output(call_id, result_data)
                            else:
                                # Add error as tool output so LLM can see what went wrong
                                self.memory_manager.add_tool_output(call_id, {"error": result_data})
                        elif item.type == "text":
                            content = getattr(item, 'content', '')
                            if content:
                                self.logger.debug(f"LLM text response: {content[:200]}...")
                            self.memory_manager.add_assistant_message(content)
                
                if tool_call_count > 0:
                    self.logger.step(f"Executed {tool_call_count} tool call(s)")
                
                # Get final response
                messages = self.memory_manager.get_messages()
                final_response = self.llm_client.create_response(
                    messages,
                    tools=tools,
                    instructions="Respond with the results from the tool calls."
                )
                result_text = self.llm_client.get_output_text(final_response)
                self.memory_manager.add_assistant_message(result_text)
                
                self.logger.step(f"Plan execution completed")
                self.logger.debug(f"Execution result: {result_text[:200]}...")
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
                status = "✓ ACHIEVED" if is_achieved else "✗ NOT ACHIEVED"
                self.logger.status(f"Goal check: {status}")
                self.logger.debug(f"Goal check response: {response_text}")
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
        max_iterations: int = 50,
        progress_tracker: Optional[ProgressTracker] = None
    ):
        self.planner = planner
        self.executor = executor
        self.checker = checker
        self.memory_manager = memory_manager
        self.logger = logger
        self.max_iterations = max_iterations
        self.progress_tracker = progress_tracker or ProgressTracker(max_iterations)
    
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
        self.logger.status(f"Starting agent run loop (max {self.max_iterations} iterations)")
        self.logger.reasoning(f"Goal: {goal[:150]}...")
        
        for iteration in range(self.max_iterations):
            self.progress_tracker.start_iteration(iteration + 1)
            status = self.progress_tracker.get_status()
            self.logger.status(status)
            self.logger.info("=" * 80)
            self.logger.info(f"ITERATION {iteration + 1}/{self.max_iterations}")
            self.logger.info("=" * 80)
            
            # Plan
            self.progress_tracker.start_step("Planning")
            self.logger.step("Phase 1: Planning")
            plan = self.planner.create_plan(goal, system_prompt)
            self.progress_tracker.end_step()
            
            # Execute
            self.progress_tracker.start_step("Execution")
            self.logger.step("Phase 2: Execution")
            execution_results = self.executor.execute_plan(plan, system_prompt)
            self.progress_tracker.end_step()
            
            # Check if goal achieved
            self.progress_tracker.start_step("Goal Check")
            self.logger.step("Phase 3: Goal Check")
            if self.checker.is_achieved(goal, system_prompt):
                self.progress_tracker.end_step()
                # Generate summary
                self.logger.reasoning("Goal achieved! Generating summary...")
                summary_prompt = f"{system_prompt}\n\nSummarize the results of the tool calls and the goal achievement."
                self.memory_manager.add_user_message(summary_prompt)
                messages = self.memory_manager.get_messages()
                response = self.planner.llm_client.create_response(messages)
                summary = self.planner.llm_client.get_output_text(response)
                self.memory_manager.add_assistant_message(summary)
                
                elapsed = self.progress_tracker.get_elapsed_str()
                self.logger.status(f"✓ Goal achieved in {iteration + 1} iterations ({elapsed})!")
                return summary
            
            self.progress_tracker.end_step()
            
            # Reflect and continue
            self.progress_tracker.start_step("Reflection")
            self.logger.step("Phase 4: Reflection")
            reflection_prompt = f"{system_prompt}\n\nReflect on the actions taken and the results achieved. What is the next step to achieve the goal?"
            self.memory_manager.add_user_message(reflection_prompt)
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    messages = self.memory_manager.get_messages()
                    response = self.planner.llm_client.create_response(messages)
                    reflection = self.planner.llm_client.get_output_text(response)
                    self.memory_manager.add_assistant_message(reflection)
                    self.logger.reflection(reflection)
                    break
                except (LLMContextWindowError, ContextWindowError) as error:
                    self.logger.warning(f"Context window exceeded during reflection (attempt {attempt + 1}/{max_retries}), compressing memory...")
                    # Force compression
                    self.memory_manager._compress_memory()
                    if attempt == max_retries - 1:
                        raise
            
            self.progress_tracker.end_step()
            self.logger.info("")  # Blank line between iterations
        
        raise MaxIterationsExceeded(f"Maximum iterations ({self.max_iterations}) exceeded")
