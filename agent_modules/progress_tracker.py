"""
Progress tracking for agent execution.
"""

import time
from datetime import datetime, timedelta
from typing import Optional


class ProgressTracker:
    """Tracks progress of agent execution."""
    
    def __init__(self, total_iterations: int = 50):
        """
        Initialize progress tracker.
        
        Args:
            total_iterations: Total number of iterations expected
        """
        self.start_time = time.time()
        self.total_iterations = total_iterations
        self.current_iteration = 0
        self.step_times = []
        self.current_step = None
        self.step_start_time = None
    
    def start_iteration(self, iteration: int):
        """Mark start of an iteration."""
        self.current_iteration = iteration
        self.step_times.append(time.time())
    
    def start_step(self, step_name: str):
        """Mark start of a step."""
        if self.step_start_time:
            # Record previous step duration
            duration = time.time() - self.step_start_time
            self.step_times.append(duration)
        self.current_step = step_name
        self.step_start_time = time.time()
    
    def end_step(self):
        """Mark end of current step."""
        if self.step_start_time:
            duration = time.time() - self.step_start_time
            self.step_times.append(duration)
            self.step_start_time = None
    
    def get_elapsed_time(self) -> float:
        """Get total elapsed time in seconds."""
        return time.time() - self.start_time
    
    def get_elapsed_str(self) -> str:
        """Get formatted elapsed time string."""
        elapsed = self.get_elapsed_time()
        return str(timedelta(seconds=int(elapsed)))
    
    def get_progress_percent(self) -> float:
        """Get progress percentage."""
        if self.total_iterations == 0:
            return 0.0
        return min(100.0, (self.current_iteration / self.total_iterations) * 100)
    
    def get_avg_step_time(self) -> float:
        """Get average step time."""
        if not self.step_times:
            return 0.0
        return sum(self.step_times) / len(self.step_times)
    
    def get_estimated_remaining(self) -> Optional[str]:
        """Get estimated remaining time."""
        if self.current_iteration == 0:
            return None
        avg_time = self.get_avg_step_time()
        if avg_time == 0:
            return None
        remaining_iterations = self.total_iterations - self.current_iteration
        estimated_seconds = avg_time * remaining_iterations
        return str(timedelta(seconds=int(estimated_seconds)))
    
    def get_status(self) -> str:
        """Get current status string."""
        elapsed = self.get_elapsed_str()
        progress = self.get_progress_percent()
        status = f"Iteration {self.current_iteration}/{self.total_iterations} ({progress:.1f}%) | Elapsed: {elapsed}"
        
        if self.current_step:
            status += f" | Current: {self.current_step}"
        
        remaining = self.get_estimated_remaining()
        if remaining:
            status += f" | Est. remaining: {remaining}"
        
        return status
