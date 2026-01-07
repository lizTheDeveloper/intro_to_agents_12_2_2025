"""
Memory management for agent conversation history.
"""

import json
from typing import List, Dict, Any, Optional


class MemoryManager:
    """Manages conversation memory and message history."""
    
    def __init__(self, system_prompt: str, max_messages: int = 50, compress_threshold: int = 40):
        """
        Initialize memory manager.
        
        Args:
            system_prompt: The system prompt to use
            max_messages: Maximum number of messages to keep before compression
            compress_threshold: Number of messages before compressing old ones
        """
        self.messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt}
        ]
        self.max_messages = max_messages
        self.compress_threshold = compress_threshold
        self.summary_messages: List[Dict[str, Any]] = []
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough estimate of token count (4 chars per token average)."""
        return len(text) // 4
    
    def _get_messages_size(self, messages: List[Dict[str, Any]]) -> int:
        """Estimate total size of messages."""
        total = 0
        for msg in messages:
            if isinstance(msg, dict):
                content = msg.get("content", "")
                if isinstance(content, str):
                    total += self._estimate_tokens(content)
                output = msg.get("output", "")
                if isinstance(output, str):
                    total += self._estimate_tokens(output)
        return total
    
    def add_user_message(self, content: str):
        """Add a user message to memory."""
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content: str):
        """Add an assistant message to memory."""
        self.messages.append({"role": "assistant", "content": content})
    
    def add_tool_output(self, call_id: str, output: Any):
        """
        Add tool call output to memory.
        
        Args:
            call_id: The call ID from the function call
            output: The output from the tool execution
        """
        self.messages.append({
            "type": "function_call_output",
            "call_id": call_id,
            "output": json.dumps({"result": output})
        })
    
    def add_raw_messages(self, messages: List[Any]):
        """Add raw messages (for handling LLM output)."""
        # Convert Pydantic objects to dicts if needed
        converted_messages = []
        for msg in messages:
            if hasattr(msg, 'model_dump'):
                # Pydantic v2
                converted_messages.append(msg.model_dump())
            elif hasattr(msg, 'dict'):
                # Pydantic v1
                converted_messages.append(msg.dict())
            elif isinstance(msg, dict):
                converted_messages.append(msg)
            else:
                # Try to convert to dict manually
                try:
                    converted_messages.append({
                        'type': getattr(msg, 'type', None),
                        'content': getattr(msg, 'content', None),
                        'role': getattr(msg, 'role', None),
                    })
                except:
                    # If all else fails, convert to string
                    converted_messages.append({'content': str(msg)})
        
        self.messages.extend(converted_messages)
        self._check_and_compress()
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """Get a copy of all messages, with compression if needed."""
        self._check_and_compress()
        return self.messages.copy()
    
    def _check_and_compress(self):
        """Check if compression is needed and compress old messages."""
        # Count non-system messages (handle both dict and object access)
        non_system_count = 0
        for m in self.messages:
            role = m.get("role") if isinstance(m, dict) else getattr(m, "role", None)
            if role != "system":
                non_system_count += 1
        
        if non_system_count > self.compress_threshold:
            self._compress_memory()
    
    def _compress_memory(self):
        """Compress old messages by summarizing them."""
        if len(self.messages) <= 2:  # Only system prompt or system + 1 message
            return
        
        # Keep system prompt and last few messages (more aggressive)
        system_msg = self.messages[0]
        keep_recent = 6  # Keep last 6 messages (reduced from 10)
        
        if len(self.messages) <= keep_recent + 1:
            return
        
        # Messages to compress (everything except system and recent)
        to_compress = self.messages[1:-keep_recent]
        recent_messages = self.messages[-keep_recent:]
        
        # Create concise summary of compressed messages
        summary_parts = []
        for msg in to_compress:
            # Handle both dict and object access
            if isinstance(msg, dict):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                msg_type = msg.get("type")
            else:
                role = getattr(msg, "role", "unknown")
                content = getattr(msg, "content", "")
                msg_type = getattr(msg, "type", None)
            
            if isinstance(content, str) and len(content) > 0:
                # Truncate to 150 chars for summary
                summary_parts.append(f"{role}: {content[:150]}")
            elif msg_type == "function_call_output":
                if isinstance(msg, dict):
                    output = msg.get("output", "")
                else:
                    output = getattr(msg, "output", "")
                if isinstance(output, str):
                    try:
                        parsed = json.loads(output)
                        if isinstance(parsed, dict) and "result" in parsed:
                            result_str = str(parsed["result"])[:150]
                            summary_parts.append(f"tool: {result_str}")
                    except:
                        summary_parts.append(f"tool_output: {output[:150]}")
        
        # Create compact summary
        summary_content = "Previous conversation summary:\n" + "\n".join(summary_parts[:20])  # Limit to 20 items
        if len(summary_parts) > 20:
            summary_content += f"\n... and {len(summary_parts) - 20} more messages"
        summary_content += "\n[Note: Previous conversation history has been summarized to manage context length.]"
        
        # Replace compressed messages with summary
        summary_msg = {
            "role": "system",
            "content": summary_content
        }
        
        self.messages = [system_msg, summary_msg] + recent_messages
        self.summary_messages.extend(to_compress)
    
    def clear(self, keep_system: bool = True):
        """
        Clear memory, optionally keeping system prompt.
        
        Args:
            keep_system: If True, keep the system prompt
        """
        if keep_system and self.messages:
            self.messages = [self.messages[0]]
        else:
            self.messages = []
    
    def get_system_prompt(self) -> str:
        """Get the system prompt."""
        if self.messages and self.messages[0].get("role") == "system":
            return self.messages[0].get("content", "")
        return ""
    
    def set_system_prompt(self, prompt: str):
        """Update the system prompt."""
        if self.messages and self.messages[0].get("role") == "system":
            self.messages[0]["content"] = prompt
        else:
            self.messages.insert(0, {"role": "system", "content": prompt})
