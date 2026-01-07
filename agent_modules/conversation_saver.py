"""
Conversation history saving functionality.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from .logging_module import AgentLogger


class ConversationSaver:
    """Saves conversation history to files."""
    
    def __init__(self, logger: AgentLogger, save_dir: Optional[str] = None):
        """
        Initialize conversation saver.
        
        Args:
            logger: Logger instance
            save_dir: Directory to save conversations (default: ./conversations)
        """
        self.logger = logger
        self.save_dir = save_dir or "./conversations"
        os.makedirs(self.save_dir, exist_ok=True)
    
    def save_conversation(
        self,
        messages: List[Dict[str, Any]],
        goal: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save conversation to a file.
        
        Args:
            messages: List of conversation messages
            goal: The goal that was being pursued
            metadata: Optional metadata (iterations, time, etc.)
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
        filepath = os.path.join(self.save_dir, filename)
        
        conversation_data = {
            "goal": goal,
            "timestamp": timestamp,
            "metadata": metadata or {},
            "messages": messages
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Conversation saved to: {filepath}")
            return filepath
        except Exception as error:
            self.logger.error(f"Failed to save conversation: {error}")
            return ""
    
    def save_summary(self, summary: str, goal: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save a text summary of the conversation.
        
        Args:
            summary: Summary text
            goal: The goal that was being pursued
            metadata: Optional metadata
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{timestamp}.md"
        filepath = os.path.join(self.save_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Conversation Summary\n\n")
                f.write(f"**Goal:** {goal}\n\n")
                f.write(f"**Timestamp:** {timestamp}\n\n")
                if metadata:
                    f.write(f"**Metadata:**\n")
                    for key, value in metadata.items():
                        f.write(f"- {key}: {value}\n")
                    f.write(f"\n")
                f.write(f"## Summary\n\n{summary}\n")
            
            self.logger.info(f"Summary saved to: {filepath}")
            return filepath
        except Exception as error:
            self.logger.error(f"Failed to save summary: {error}")
            return ""
