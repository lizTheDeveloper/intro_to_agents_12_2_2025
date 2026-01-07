# Matrix Integration for Agent

This document describes the Matrix integration added to the Agent framework, enabling communication with Matrix rooms at `matrix.themultiverse.school`.

## Overview

The agent now has six Matrix-related tools that allow it to:
- Post messages to channels
- Read messages from rooms
- List available rooms
- Invite users to rooms
- Check user membership
- Monitor notifications

## Matrix Tools

### 1. matrix_post_message

Post a message to a Matrix room.

**Parameters:**
- `channel` (required): Channel name (e.g., 'coordination', 'research')
- `agent` (required): Agent username posting the message
- `message` (required): Message content to post
- `status` (optional): Status tag for the message

**Example:**
```python
agent.run("Post a message to the 'coordination' channel as agent 'organizer' saying 'Task completed'")
```

### 2. matrix_read_messages

Read recent messages from a Matrix room.

**Parameters:**
- `channel` (required): Channel name to read from
- `agent` (required): Agent username for authentication
- `limit` (optional): Number of messages to retrieve (default: 10)

**Example:**
```python
agent.run("Read the last 20 messages from the 'research' channel as agent 'reader'")
```

### 3. matrix_list_rooms

List all configured Matrix rooms and their mappings.

**Parameters:**
- `agent` (optional): Agent username for authentication (default: 'orchestrator')

**Example:**
```python
agent.run("List all available Matrix rooms")
```

### 4. matrix_invite_user

Invite a user to a Matrix room.

**Parameters:**
- `channel` (required): Channel name where to invite the user
- `agent` (required): Agent username performing the invitation (must have invite permissions)
- `user_id` (required): Matrix user ID to invite (e.g., '@user:matrix.themultiverse.school')

**Example:**
```python
agent.run("Invite '@newuser:matrix.themultiverse.school' to the 'coordination' channel as agent 'admin'")
```

### 5. matrix_check_membership

Check if a user is a member of a Matrix room.

**Parameters:**
- `channel` (required): Channel name to check
- `user_id` (required): Matrix user ID to check
- `agent` (optional): Agent username for authentication (default: 'orchestrator')

**Example:**
```python
agent.run("Check if '@ann:matrix.themultiverse.school' is a member of the 'research' channel")
```

### 6. matrix_get_notifications

Get unread notification count for an agent across Matrix rooms.

**Parameters:**
- `agent` (required): Agent username to check notifications for
- `channels` (optional): List of channel names to check (default: all configured channels)

**Example:**
```python
agent.run("Get the notification count for agent 'coordinator'")
```

## Combined Use Cases

The agent can now combine file system operations with Matrix notifications:

```python
agent.run("""
1. Organize all markdown files in the current directory into a 'docs' folder
2. Post a summary message to the 'coordination' channel as agent 'file_organizer'
   listing what was organized
""")
```

## Implementation Details

The Matrix functions are currently set up as stubs that will integrate with your Matrix MCP server. The server URL is configured as:

```python
MATRIX_SERVER = "https://matrix.themultiverse.school"
```

Each function returns structured data that includes:
- Success status
- Relevant identifiers (channel, agent, user_id)
- Result data (messages, rooms, membership status, etc.)

## Setup

Make sure you have the required dependencies:

```bash
pip install -r requirements.txt
```

The `requests` library is now included in requirements.txt for HTTP communication with the Matrix server.

## Next Steps

To fully integrate with your Matrix MCP server:

1. Configure authentication credentials for your Matrix agents
2. Map channel names to actual Matrix room IDs
3. Implement the actual HTTP calls to the Matrix API
4. Add error handling for network issues and authentication failures
5. Consider adding rate limiting for API calls

## Security Considerations

- Store Matrix access tokens securely (use environment variables)
- Validate user permissions before allowing room creation/invitations
- Implement proper authentication for each agent
- Consider implementing message encryption for sensitive channels

