"""
Example demonstrating how to use the Agent with security restrictions.

The agent is configured with a working directory at initialization,
and all file operations are restricted to that directory only.

NOTE: This example uses a simplified mock Agent that doesn't require
the OpenAI module, to demonstrate the security concept.
"""

import os


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
    
    def _read_file(self, filepath):
        """Read the contents of a file at the specified filepath."""
        is_valid, normalized_path, error_msg = self._validate_path(filepath)
        if not is_valid:
            return error_msg
        try:
            with open(normalized_path, 'r') as file:
                content = file.read()
            return content
        except Exception as error:
            return f"Error reading file: {str(error)}"
    
    def _write_file(self, filepath, content):
        """Write content to a file at the specified filepath."""
        is_valid, normalized_path, error_msg = self._validate_path(filepath)
        if not is_valid:
            return error_msg
        try:
            parent_dir = os.path.dirname(normalized_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            with open(normalized_path, 'w') as file:
                file.write(content)
            return f"Successfully wrote to {filepath}"
        except Exception as error:
            return f"Error writing file: {str(error)}"


def example_basic_usage():
    """Basic example of creating an agent with restricted directory access."""
    
    # Create a test directory
    test_dir = "./test_workspace"
    os.makedirs(test_dir, exist_ok=True)
    
    # Initialize agent with restricted access to test_workspace
    print("=" * 60)
    print("Example: Agent with Restricted Directory Access")
    print("=" * 60)
    
    agent = Agent(working_directory=test_dir)
    
    print("\nThe agent is now restricted to:", agent.working_directory)
    print("\nAttempting to access files outside this directory will be blocked.")
    
    # Clean up
    os.rmdir(test_dir)


def example_security_demonstration():
    """Demonstrate that security restrictions work."""
    
    import tempfile
    import shutil
    
    # Create test directory
    test_dir = tempfile.mkdtemp(prefix="agent_demo_")
    
    # Create a file inside the allowed directory
    test_file = os.path.join(test_dir, "allowed.txt")
    with open(test_file, 'w') as f:
        f.write("This is an allowed file")
    
    print("\n" + "=" * 60)
    print("Security Demonstration")
    print("=" * 60)
    print(f"\nAllowed directory: {test_dir}")
    
    agent = Agent(working_directory=test_dir)
    
    # Test 1: Read an allowed file (should work)
    print("\n1. Reading allowed file...")
    result = agent._read_file("allowed.txt")
    print(f"   Result: {result}")
    
    # Test 2: Try to read a file outside the directory (should be blocked)
    print("\n2. Attempting to read /etc/passwd (should be blocked)...")
    result = agent._read_file("/etc/passwd")
    print(f"   Result: {result}")
    
    # Test 3: Try path traversal attack (should be blocked)
    print("\n3. Attempting path traversal with '../../../etc/passwd' (should be blocked)...")
    result = agent._read_file("../../../etc/passwd")
    print(f"   Result: {result}")
    
    # Clean up
    shutil.rmtree(test_dir)
    print("\n✓ Demo complete!")


if __name__ == "__main__":
    example_basic_usage()
    example_security_demonstration()
    
    print("\n" + "=" * 60)
    print("Key Points:")
    print("=" * 60)
    print("1. Set working_directory once when creating the Agent")
    print("2. All file operations are automatically restricted to that directory")
    print("3. No need to pass allowed_directory to each function call")
    print("4. Path traversal attacks and absolute paths are blocked")
    print("5. Both relative and absolute paths (within the directory) work fine")
    print("=" * 60)
