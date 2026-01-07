"""
Background process management for tracking and controlling long-running processes.
"""

import subprocess
import os
from datetime import datetime
from typing import Dict, Optional, List, Any
from .exceptions import PathValidationError
from .path_validator import PathValidator
from .logging_module import AgentLogger


class ProcessManager:
    """Manages background processes and their lifecycle."""
    
    def __init__(self, working_directory: str, path_validator: PathValidator, logger: AgentLogger):
        """
        Initialize process manager.
        
        Args:
            working_directory: Directory to execute processes in
            path_validator: Path validator for log file paths
            logger: Logger instance
        """
        self.working_directory = working_directory
        self.path_validator = path_validator
        self.logger = logger
        self.processes: Dict[int, Dict] = {}
    
    def start_background(
        self,
        command: str,
        log_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Start a background process and track it.
        
        Args:
            command: Command to execute
            log_file: Optional path to redirect stdout/stderr
            
        Returns:
            Dictionary with process information
        """
        self.logger.info(f"Starting background command: {command}")
        
        try:
            log_file_handle = None
            
            # Validate and setup log file if provided
            if log_file:
                normalized_log_path = self.path_validator.validate_and_raise(log_file)
                
                # Create parent directory for log file if needed
                log_dir = os.path.dirname(normalized_log_path)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)
                
                # Open log file for writing
                log_file_handle = open(normalized_log_path, 'w')
                stdout_dest = log_file_handle
                stderr_dest = log_file_handle
            else:
                stdout_dest = subprocess.DEVNULL
                stderr_dest = subprocess.DEVNULL
            
            # Start the process in the background
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=self.working_directory,
                stdout=stdout_dest,
                stderr=stderr_dest,
                start_new_session=True  # Detach from parent process
            )
            
            process_info = {
                "process": process,
                "command": command,
                "log_file": log_file,
                "started_at": datetime.now(),
                "log_file_handle": log_file_handle
            }
            
            self.processes[process.pid] = process_info
            
            self.logger.info(f"Background process started (PID: {process.pid})")
            if log_file:
                self.logger.info(f"  Output redirected to: {log_file}")
            
            return {
                "command": command,
                "pid": process.pid,
                "working_directory": self.working_directory,
                "log_file": log_file if log_file else None,
                "message": f"Process started in background with PID {process.pid}"
            }
            
        except PathValidationError as error:
            error_msg = f"Invalid log file path: {error}"
            self.logger.error(error_msg)
            return {"error": error_msg}
        except Exception as error:
            error_msg = f"Error starting background command: {error}"
            self.logger.error(error_msg)
            return {"error": error_msg}
    
    def stop_process(self, pid: int) -> bool:
        """
        Stop a tracked process.
        
        Args:
            pid: Process ID to stop
            
        Returns:
            True if process was stopped, False if not found
        """
        if pid not in self.processes:
            self.logger.warning(f"Process {pid} not found")
            return False
        
        process_info = self.processes[pid]
        process = process_info["process"]
        
        try:
            process.terminate()
            
            # Close log file handle if open
            if process_info.get("log_file_handle"):
                process_info["log_file_handle"].close()
            
            del self.processes[pid]
            self.logger.info(f"Process {pid} terminated")
            return True
        except Exception as error:
            self.logger.error(f"Error terminating process {pid}: {error}")
            return False
    
    def list_processes(self) -> Dict[int, Dict]:
        """List all tracked processes."""
        return self.processes.copy()
    
    def get_process_info(self, pid: int) -> Optional[Dict]:
        """Get information about a specific process."""
        return self.processes.get(pid)
    
    def cleanup(self):
        """Stop all tracked processes."""
        self.logger.info("Cleaning up all background processes")
        pids = list(self.processes.keys())
        for pid in pids:
            self.stop_process(pid)
    
    def __del__(self):
        """Cleanup on deletion."""
        self.cleanup()
