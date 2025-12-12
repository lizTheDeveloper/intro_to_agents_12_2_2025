# Agent Security Features

## Overview

The Agent has been enhanced with security restrictions that prevent it from reading or writing files outside its configured working directory. This protects against:

- **Path traversal attacks** (e.g., `../../etc/passwd`)
- **Unauthorized file access** (absolute paths outside the allowed directory)
- **Symlink attacks** (symbolic links that point outside the directory)

## How It Works

### 1. Set Working Directory Once

When initializing the Agent, specify the working directory:

```python
from agentic_agent import Agent

# Restrict agent to a specific directory
agent = Agent(working_directory="/path/to/restricted/folder")

# Or use current directory (default)
agent = Agent(working_directory=os.getcwd())
```

### 2. All Operations Are Automatically Restricted

Once the working directory is set, **all file operations** are automatically validated:

- `_read_file(filepath)` - Read files
- `_write_file(filepath, content)` - Write files
- `_list_directory(path)` - List directories
- `_move_file(source, dest)` - Move/rename files
- `_make_directory(path)` - Create directories

No need to pass `allowed_directory` to each function - it's set once at the Agent level.

### 3. Security Validation

The `_validate_path()` method checks every file path:

1. **Resolves to absolute path** - Handles both relative and absolute paths
2. **Normalizes the path** - Removes `.`, `..`, and follows symlinks
3. **Verifies containment** - Ensures the path is within `working_directory`
4. **Blocks unauthorized access** - Returns an error if validation fails

## Examples

### ✅ Allowed Operations

```python
agent = Agent(working_directory="/home/user/workspace")

# Read file with relative path
content = agent._read_file("data.txt")

# Read file with absolute path (within workspace)
content = agent._read_file("/home/user/workspace/data.txt")

# Create subdirectory
agent._make_directory("subfolder")

# Write to subdirectory
agent._write_file("subfolder/output.txt", "content")
```

### ❌ Blocked Operations

```python
agent = Agent(working_directory="/home/user/workspace")

# Path traversal attack - BLOCKED
agent._read_file("../../../etc/passwd")
# Returns: "Access denied: Path is outside allowed directory"

# Absolute path outside workspace - BLOCKED
agent._read_file("/etc/passwd")
# Returns: "Access denied: Path is outside allowed directory"

# Symlink pointing outside - BLOCKED
# (Even if workspace/link -> /etc/passwd exists)
agent._read_file("link")
# Returns: "Access denied: Path is outside allowed directory"
```

## Testing

Run the security tests to verify the restrictions work:

```bash
cd long_horizon_tasks
python test_agent_security.py
```

Run the example demonstration:

```bash
python example_secure_agent.py
```

## Key Benefits

1. **Simple Configuration** - Set `working_directory` once during initialization
2. **Automatic Protection** - All file operations are automatically validated
3. **No Extra Parameters** - Methods access `self.working_directory` directly
4. **Comprehensive Coverage** - Blocks path traversal, absolute paths, and symlink attacks
5. **Clear Error Messages** - Users get informative error messages when access is denied

## Implementation Details

The security is implemented at the Agent class level:

- `__init__(working_directory)` - Sets and validates the working directory
- `_validate_path(filepath)` - Internal method that validates all file paths
- `_read_file()`, `_write_file()`, etc. - All call `_validate_path()` before accessing files

This ensures that **no file operation can bypass the security restrictions**.
