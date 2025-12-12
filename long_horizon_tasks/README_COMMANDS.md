# Agent Terminal Command Execution

## Overview

The Agent now has the ability to execute terminal commands within its restricted working directory. This enables the agent to:

- Run scripts and programs
- Interact with the file system using shell commands
- Execute build tools, package managers, and development servers
- Start long-running background processes

All commands execute within the agent's configured `working_directory` for security.

## Available Tools

### 1. execute_command

Execute a terminal command synchronously and capture its output.

**Use for:**
- Quick commands that complete in < 30 seconds
- Commands where you need to capture the output
- File operations (ls, grep, find, cat, etc.)
- Running scripts (python script.py, node app.js, etc.)

**Parameters:**
- `command` (string, required): The command to execute
- `timeout` (number, optional): Maximum execution time in seconds (default: 30)

**Returns:**
```python
{
    "command": "ls -la",
    "exit_code": 0,
    "stdout": "... output ...",
    "stderr": "... errors ...",
    "working_directory": "/path/to/workdir"
}
```

**Example usage:**
```python
agent = Agent(working_directory="/my/project")

# List files
result = agent._execute_command("ls -la")
print(result["stdout"])

# Run a Python script
result = agent._execute_command("python process_data.py")
if result["exit_code"] == 0:
    print("Success!")
else:
    print(f"Error: {result['stderr']}")

# Search for patterns
result = agent._execute_command("grep -r 'TODO' .")
```

### 2. execute_background_command

Execute a terminal command in the background (non-blocking).

**Use for:**
- Web servers (python -m http.server, npm run dev)
- Development servers (flask run, rails server)
- File watchers (npm run watch)
- Any long-running process that doesn't need to block

**Parameters:**
- `command` (string, required): The command to execute
- `log_file` (string, optional): Path to redirect stdout/stderr (relative to working directory)

**Returns:**
```python
{
    "command": "python -m http.server 8000",
    "pid": 12345,
    "working_directory": "/path/to/workdir",
    "log_file": "server.log",
    "message": "Process started in background with PID 12345"
}
```

**Example usage:**
```python
agent = Agent(working_directory="/my/project")

# Start a web server
result = agent._execute_background_command(
    "python -m http.server 8000",
    log_file="server.log"
)
print(f"Server running on PID: {result['pid']}")

# Start a development build watcher
result = agent._execute_background_command(
    "npm run watch",
    log_file="build.log"
)

# Silent background process (no log file)
result = agent._execute_background_command("celery worker")
```

## Security Features

### Working Directory Restriction

All commands execute in the agent's `working_directory`:

```python
agent = Agent(working_directory="/safe/workspace")

# This runs in /safe/workspace
agent._execute_command("ls")

# This also runs in /safe/workspace
agent._execute_command("pwd")  # Output: /safe/workspace
```

### Log File Path Validation

When using `log_file` with background commands, the path is validated to ensure it's within the working directory:

```python
# ✅ Valid - relative path
agent._execute_background_command("npm start", log_file="logs/server.log")

# ✅ Valid - absolute path within working directory
agent._execute_background_command("npm start", 
    log_file="/safe/workspace/logs/server.log")

# ❌ Blocked - path traversal
agent._execute_background_command("npm start", 
    log_file="../../../etc/passwd")
# Returns: {"error": "Access denied: Path is outside allowed directory"}
```

## Practical Examples

### Example 1: Setup and Build Project

```python
agent = Agent(working_directory="/my/project")

# Install dependencies
result = agent._execute_command("npm install")
if result["exit_code"] != 0:
    print(f"Install failed: {result['stderr']}")
    return

# Run tests
result = agent._execute_command("npm test")
print(result["stdout"])

# Build for production
result = agent._execute_command("npm run build")
```

### Example 2: Start Development Environment

```python
agent = Agent(working_directory="/my/webapp")

# Start backend server in background
backend = agent._execute_background_command(
    "python manage.py runserver",
    log_file="logs/backend.log"
)

# Start frontend dev server in background
frontend = agent._execute_background_command(
    "npm run dev",
    log_file="logs/frontend.log"
)

print(f"Backend PID: {backend['pid']}")
print(f"Frontend PID: {frontend['pid']}")
```

### Example 3: File Processing

```python
agent = Agent(working_directory="/data/processing")

# Find all CSV files
result = agent._execute_command("find . -name '*.csv'")
csv_files = result["stdout"].strip().split("\n")

# Process each file
for csv_file in csv_files:
    result = agent._execute_command(f"python process.py {csv_file}")
    if result["exit_code"] == 0:
        print(f"✓ Processed {csv_file}")
    else:
        print(f"✗ Failed {csv_file}: {result['stderr']}")
```

### Example 4: Git Operations

```python
agent = Agent(working_directory="/my/repo")

# Check git status
result = agent._execute_command("git status --short")
print(result["stdout"])

# Add and commit files
agent._execute_command("git add .")
result = agent._execute_command('git commit -m "Auto commit by agent"')

# Push changes
result = agent._execute_command("git push origin main")
if result["exit_code"] == 0:
    print("✓ Changes pushed successfully")
```

### Example 5: Database Operations

```python
agent = Agent(working_directory="/my/project")

# Run database migrations
result = agent._execute_command("python manage.py migrate")
if result["exit_code"] != 0:
    print(f"Migration failed: {result['stderr']}")
    return

# Load initial data
result = agent._execute_command("python manage.py loaddata initial.json")

# Start database shell in background for monitoring
agent._execute_background_command(
    "python manage.py dbshell",
    log_file="db_queries.log"
)
```

## Best Practices

### 1. Choose the Right Tool

- Use `execute_command` for quick operations where you need the output
- Use `execute_background_command` for servers and long-running processes

### 2. Handle Errors Gracefully

Always check the exit code:

```python
result = agent._execute_command("some-command")
if result.get("exit_code") != 0:
    # Handle the error
    print(f"Command failed: {result.get('stderr')}")
else:
    # Process the output
    print(result.get("stdout"))
```

### 3. Use Timeouts

For potentially slow commands, specify a timeout:

```python
# Default 30 second timeout
result = agent._execute_command("slow-command")

# Custom 60 second timeout
result = agent._execute_command("very-slow-command", timeout=60)
```

### 4. Log Background Processes

Always use log files for background commands so you can debug issues:

```python
# Good - can debug later
agent._execute_background_command(
    "npm run dev",
    log_file="dev-server.log"
)

# Less ideal - no way to see what happened
agent._execute_background_command("npm run dev")
```

### 5. Command Composition

Use shell features for complex operations:

```python
# Multiple commands with &&
result = agent._execute_command("cd subdir && python script.py && cd ..")

# Piping
result = agent._execute_command("cat data.txt | grep 'pattern' | wc -l")

# Redirection
result = agent._execute_command("python script.py > output.txt 2>&1")
```

## Testing

Run the test suite to verify command execution:

```bash
cd long_horizon_tasks
python test_command_execution.py
```

The tests demonstrate:
- ✅ Successful command execution
- ✅ Error handling
- ✅ Background process management
- ✅ Log file redirection
- ✅ Working directory restriction
