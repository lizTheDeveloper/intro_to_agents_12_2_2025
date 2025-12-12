"""
Test script to verify that the agent's file access security restrictions work correctly.

This script tests:
1. Access to files within the allowed directory (should work)
2. Access to files outside the allowed directory (should be blocked)
3. Path traversal attacks using .. (should be blocked)
4. Absolute paths outside the directory (should be blocked)
"""

import os
import tempfile
import shutil
from pathlib import Path

# Import the Agent class
import sys
sys.path.insert(0, os.path.dirname(__file__))


def test_path_validation():
    """Test the path validation function with various scenarios"""
    
    print("=" * 60)
    print("Testing Agent File Access Security")
    print("=" * 60)
    
    # Create a temporary directory structure for testing
    test_root = tempfile.mkdtemp(prefix="agent_test_")
    allowed_dir = os.path.join(test_root, "allowed_workspace")
    restricted_dir = os.path.join(test_root, "restricted_area")
    
    os.makedirs(allowed_dir, exist_ok=True)
    os.makedirs(restricted_dir, exist_ok=True)
    
    # Create test files
    allowed_file = os.path.join(allowed_dir, "allowed.txt")
    restricted_file = os.path.join(restricted_dir, "restricted.txt")
    
    with open(allowed_file, 'w') as f:
        f.write("This file is in the allowed directory")
    with open(restricted_file, 'w') as f:
        f.write("This file is OUTSIDE the allowed directory")
    
    print(f"\nTest setup:")
    print(f"  Allowed directory: {allowed_dir}")
    print(f"  Restricted directory: {restricted_dir}")
    
    # Create a mock Agent class for testing (without OpenAI dependency)
    class MockAgent:
        def __init__(self, working_directory):
            self.working_directory = os.path.realpath(working_directory)
        
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
    
    # Create agent instance
    agent = MockAgent(allowed_dir)
    
    # Test 1: Access file within allowed directory (should work)
    print("\n" + "─" * 60)
    print("Test 1: Access file within allowed directory")
    print("─" * 60)
    is_valid, path, error = agent._validate_path("allowed.txt")
    print(f"Path: 'allowed.txt'")
    print(f"Valid: {is_valid}")
    print(f"Result: {'✓ PASS - Access allowed' if is_valid else '✗ FAIL - Should be allowed'}")
    
    # Test 2: Access absolute path within allowed directory (should work)
    print("\n" + "─" * 60)
    print("Test 2: Access absolute path within allowed directory")
    print("─" * 60)
    is_valid, path, error = agent._validate_path(allowed_file)
    print(f"Path: '{allowed_file}'")
    print(f"Valid: {is_valid}")
    print(f"Result: {'✓ PASS - Access allowed' if is_valid else '✗ FAIL - Should be allowed'}")
    
    # Test 3: Path traversal attack using .. (should be blocked)
    print("\n" + "─" * 60)
    print("Test 3: Path traversal attack using '..'")
    print("─" * 60)
    is_valid, path, error = agent._validate_path("../restricted_area/restricted.txt")
    print(f"Path: '../restricted_area/restricted.txt'")
    print(f"Valid: {is_valid}")
    print(f"Error: {error if error else 'None'}")
    print(f"Result: {'✓ PASS - Access blocked' if not is_valid else '✗ FAIL - Should be blocked'}")
    
    # Test 4: Absolute path outside allowed directory (should be blocked)
    print("\n" + "─" * 60)
    print("Test 4: Absolute path outside allowed directory")
    print("─" * 60)
    is_valid, path, error = agent._validate_path(restricted_file)
    print(f"Path: '{restricted_file}'")
    print(f"Valid: {is_valid}")
    print(f"Error: {error if error else 'None'}")
    print(f"Result: {'✓ PASS - Access blocked' if not is_valid else '✗ FAIL - Should be blocked'}")
    
    # Test 5: Complex path traversal (should be blocked)
    print("\n" + "─" * 60)
    print("Test 5: Complex path traversal attack")
    print("─" * 60)
    is_valid, path, error = agent._validate_path("subdir/../../restricted_area/restricted.txt")
    print(f"Path: 'subdir/../../restricted_area/restricted.txt'")
    print(f"Valid: {is_valid}")
    print(f"Error: {error if error else 'None'}")
    print(f"Result: {'✓ PASS - Access blocked' if not is_valid else '✗ FAIL - Should be blocked'}")
    
    # Test 6: Access /etc/passwd (should be blocked)
    print("\n" + "─" * 60)
    print("Test 6: Attempt to access system file (/etc/passwd)")
    print("─" * 60)
    is_valid, path, error = agent._validate_path("/etc/passwd")
    print(f"Path: '/etc/passwd'")
    print(f"Valid: {is_valid}")
    print(f"Error: {error if error else 'None'}")
    print(f"Result: {'✓ PASS - Access blocked' if not is_valid else '✗ FAIL - Should be blocked'}")
    
    # Test 7: Test with actual read_file function
    print("\n" + "─" * 60)
    print("Test 7: Actual read_file function with valid path")
    print("─" * 60)
    result = agent._read_file("allowed.txt")
    success = "This file is in the allowed directory" in result
    print(f"Result: {'✓ PASS - File read successfully' if success else '✗ FAIL - Could not read file'}")
    print(f"Content preview: {result[:50]}...")
    
    # Test 8: Test with actual read_file function and invalid path
    print("\n" + "─" * 60)
    print("Test 8: Actual read_file function with invalid path")
    print("─" * 60)
    result = agent._read_file("../restricted_area/restricted.txt")
    success = "Access denied" in result
    print(f"Result: {'✓ PASS - Access blocked' if success else '✗ FAIL - Should be blocked'}")
    print(f"Error message: {result}")
    
    # Cleanup
    print("\n" + "─" * 60)
    print("Cleaning up test files...")
    shutil.rmtree(test_root)
    print("✓ Cleanup complete")
    
    print("\n" + "=" * 60)
    print("Security tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    test_path_validation()
