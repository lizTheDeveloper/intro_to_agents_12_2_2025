"""
Default tool definitions for the agent.
"""


def get_default_tool_definitions():
    """Get default tool definitions."""
    return [
        {
            "type": "function",
            "name": "read_file",
            "description": "Read the contents of a file at the specified filepath. Paths can be relative to the working directory or absolute (but must be within the allowed directory).",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path to the file to read (relative or absolute)",
                    },
                },
                "required": ["filepath"],
            },
        },
        {
            "type": "function",
            "name": "write_file",
            "description": "Write content to a file at the specified filepath. Paths can be relative to the working directory or absolute (but must be within the allowed directory).",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path to the file to write to (relative or absolute)",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file",
                    },
                },
                "required": ["filepath", "content"],
            },
        },
        {
            "type": "function",
            "name": "list_directory",
            "description": "List all files and directories in the specified path. Paths can be relative to the working directory or absolute (but must be within the allowed directory).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path to list contents from (relative or absolute)",
                    },
                },
                "required": ["path"],
            },
        },
        {
            "type": "function",
            "name": "move_file",
            "description": "Move or rename a file from source path to destination path. Both paths must be within the allowed directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {
                        "type": "string",
                        "description": "The current path of the file to move (relative or absolute)",
                    },
                    "destination_path": {
                        "type": "string",
                        "description": "The new path where the file should be moved to (relative or absolute)",
                    },
                },
                "required": ["source_path", "destination_path"],
            },
        },
        {
            "type": "function",
            "name": "contact_user",
            "description": "Contact the user to request information or clarification. Use this when you need user input to proceed with the task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message or question to present to the user",
                    },
                },
                "required": ["message"],
            },
        },
        {
            "type": "function",
            "name": "make_directory",
            "description": "Create a new directory at the specified path. Creates parent directories if they don't exist. Path must be within the allowed directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path where the directory should be created (relative or absolute)",
                    },
                },
                "required": ["path"],
            },
        },
        {
            "type": "function",
            "name": "execute_command",
            "description": "Execute a terminal command in the working directory. Returns stdout, stderr, and exit code. Use for commands that complete quickly (< 30 seconds).",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute (e.g., 'ls -la', 'python script.py', 'grep pattern file.txt')",
                    },
                    "timeout": {
                        "type": "number",
                        "description": "Maximum execution time in seconds (default: 30)",
                    },
                },
                "required": ["command"],
            },
        },
        {
            "type": "function",
            "name": "execute_background_command",
            "description": "Execute a terminal command in the background (non-blocking). Use for long-running processes like web servers, watchers, etc. Returns immediately with the process ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute in the background (e.g., 'python -m http.server 8000', 'npm run dev')",
                    },
                    "log_file": {
                        "type": "string",
                        "description": "Optional path to redirect stdout/stderr (relative to working directory)",
                    },
                },
                "required": ["command"],
            },
        },
    ]
