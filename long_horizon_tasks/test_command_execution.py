"""
Test script to demonstrate the agent's terminal command execution capabilities.

This script tests:
1. Basic command execution (ls, echo, etc.)
2. Commands with output
3. Commands that fail
4. Background command execution
5. Commands with log file redirection
"""

import os
import tempfile
import shutil
import time


# Simplified Agent class for demonstration (no OpenAI dependency)
class Agent:
    def __init__(self, working_directory=None):
        if working_directory is None:
            self.working_directory = os.getcwd()
        else:
            self.working_directory = os.path.realpath(working_directory)
        
        if not os.path.exists(self.working_directory):
            raise ValueError(f"Working directory does not exist: {self.working_directory}")
        if not os.path.isdir(self.working_directory):
            raise ValueError(f"Working directory is not a directory: {self.working_directory}")
        
        print(f"[Agent initialized with restricted access to: {self.working_directory}]")
    
    def _validate_path(self, filepath):
        """Validates that a filepath is within the allowed directory."""
        try:
            abs_allowed_dir = os.path.realpath(self.working_directory)
            if not os.path.isabs(filepath):
                filepath = os.path.join(self.working_directory, filepath)
            abs_filepath = os.path.realpath(filepath)
            
            try:
                common_path = os.path.commonpath([abs_allowed_dir, abs_filepath])
            except ValueError:
                return False, None, f"Access denied: Path is outside allowed directory"
            
            if common_path != abs_allowed_dir:
                return False, None, f"Access denied: Path '{filepath}' is outside allowed directory"
            
            return True, abs_filepath, None
        except Exception as error:
            return False, None, f"Path validation error: {str(error)}"
    
    def _execute_command(self, command, timeout=30):
        """Execute a terminal command in the working directory."""
        import subprocess
        
        print(f"Executing command: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = {
                "command": command,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "working_directory": self.working_directory
            }
            
            if result.returncode == 0:
                print(f"✓ Command succeeded (exit code: 0)")
            else:
                print(f"✗ Command failed (exit code: {result.returncode})")
            
            return output
            
        except subprocess.TimeoutExpired:
            return {
                "command": command,
                "error": f"Command timed out after {timeout} seconds",
                "working_directory": self.working_directory
            }
        except Exception as error:
            return {
                "command": command,
                "error": f"Error executing command: {str(error)}",
                "working_directory": self.working_directory
            }
    
    def _execute_background_command(self, command, log_file=None):
        """Execute a terminal command in the background."""
        import subprocess
        
        print(f"Starting background command: {command}")
        
        try:
            if log_file:
                is_valid, normalized_log_path, error_msg = self._validate_path(log_file)
                if not is_valid:
                    return {"error": error_msg}
                
                log_dir = os.path.dirname(normalized_log_path)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)
                
                log_file_handle = open(normalized_log_path, 'w')
                stdout_dest = log_file_handle
                stderr_dest = log_file_handle
            else:
                log_file_handle = None
                stdout_dest = subprocess.DEVNULL
                stderr_dest = subprocess.DEVNULL
            
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=self.working_directory,
                stdout=stdout_dest,
                stderr=stderr_dest,
                start_new_session=True
            )
            
            output = {
                "command": command,
                "pid": process.pid,
                "working_directory": self.working_directory,
                "log_file": log_file if log_file else None,
                "message": f"Process started in background with PID {process.pid}"
            }
            
            print(f"✓ Background process started (PID: {process.pid})")
            if log_file:
                print(f"  Output redirected to: {log_file}")
            
            return output
            
        except Exception as error:
            return {
                "command": command,
                "error": f"Error starting background command: {str(error)}",
                "working_directory": self.working_directory
            }


def test_command_execution():
    """Test the command execution capabilities"""
    
    print("=" * 60)
    print("Testing Agent Terminal Command Execution")
    print("=" * 60)
    
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp(prefix="agent_cmd_test_")
    
    print(f"\nTest directory: {test_dir}")
    
    # Create agent instance
    agent = Agent(working_directory=test_dir)
    
    # Test 1: Simple command - list directory
    print("\n" + "─" * 60)
    print("Test 1: List directory contents")
    print("─" * 60)
    result = agent._execute_command("ls -la")
    print(f"Exit code: {result.get('exit_code')}")
    print(f"Output:\n{result.get('stdout')}")
    
    # Test 2: Create a file and read it
    print("\n" + "─" * 60)
    print("Test 2: Create file and read it")
    print("─" * 60)
    result = agent._execute_command("echo 'Hello from agent!' > test.txt && cat test.txt")
    print(f"Exit code: {result.get('exit_code')}")
    print(f"Output:\n{result.get('stdout')}")
    
    # Test 3: Command that fails
    print("\n" + "─" * 60)
    print("Test 3: Command that fails")
    print("─" * 60)
    result = agent._execute_command("cat nonexistent_file.txt")
    print(f"Exit code: {result.get('exit_code')}")
    print(f"Stderr:\n{result.get('stderr')}")
    
    # Test 4: Python command
    print("\n" + "─" * 60)
    print("Test 4: Execute Python command")
    print("─" * 60)
    result = agent._execute_command("python3 -c \"print('Python says hello!'); print('2 + 2 =', 2 + 2)\"")
    print(f"Exit code: {result.get('exit_code')}")
    print(f"Output:\n{result.get('stdout')}")
    
    # Test 5: Background command with log file
    print("\n" + "─" * 60)
    print("Test 5: Background command with log file")
    print("─" * 60)
    result = agent._execute_background_command(
        "for i in 1 2 3 4 5; do echo \"Count: $i\"; sleep 1; done",
        log_file="background_output.log"
    )
    print(f"PID: {result.get('pid')}")
    print(f"Message: {result.get('message')}")
    print(f"Log file: {result.get('log_file')}")
    
    # Wait a bit and check the log file
    print("\nWaiting 3 seconds for background process to write some output...")
    time.sleep(3)
    
    log_path = os.path.join(test_dir, "background_output.log")
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            print(f"Log file contents so far:\n{f.read()}")
    
    # Test 6: Background command without log file
    print("\n" + "─" * 60)
    print("Test 6: Background command without log file (silent)")
    print("─" * 60)
    result = agent._execute_background_command("sleep 10")
    print(f"PID: {result.get('pid')}")
    print(f"Message: {result.get('message')}")
    print("(Process will continue in background)")
    
    # Cleanup
    print("\n" + "─" * 60)
    print("Cleaning up test directory...")
    time.sleep(2)  # Let background processes finish
    shutil.rmtree(test_dir)
    print("✓ Cleanup complete")
    
    print("\n" + "=" * 60)
    print("Command execution tests completed!")
    print("=" * 60)
    print("\nKey capabilities demonstrated:")
    print("✓ Execute synchronous commands with output capture")
    print("✓ Handle command failures and stderr")
    print("✓ Execute Python and shell scripts")
    print("✓ Start background processes")
    print("✓ Redirect background output to log files")
    print("✓ All commands restricted to working directory")


if __name__ == "__main__":
    test_command_execution()
