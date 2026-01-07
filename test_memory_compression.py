#!/usr/bin/env python3
"""
Test script to verify memory compression works correctly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agent_modules.memory_manager import MemoryManager


def test_memory_compression():
    """Test that memory compression works correctly."""
    print("Testing memory compression...")
    
    # Create memory manager with low threshold
    manager = MemoryManager(
        system_prompt="You are a helpful assistant.",
        max_messages=25,
        compress_threshold=15
    )
    
    # Add many messages to trigger compression
    for i in range(20):
        manager.add_user_message(f"User message {i}")
        manager.add_assistant_message(f"Assistant response {i}")
    
    print(f"Messages before compression check: {len(manager.messages)}")
    
    # Trigger compression check
    manager._check_and_compress()
    
    print(f"Messages after compression: {len(manager.messages)}")
    
    # Verify we kept system prompt
    assert manager.messages[0].get("role") == "system", "System prompt should be first"
    
    # Verify compression happened (should have system + summary + recent messages)
    assert len(manager.messages) < 20, "Messages should be compressed"
    
    # Verify recent messages are preserved
    recent_messages = manager.messages[-6:]
    assert any("User message" in str(msg.get("content", "")) for msg in recent_messages), "Recent messages should be preserved"
    
    print("✓ Memory compression test passed!")
    return True


if __name__ == "__main__":
    try:
        test_memory_compression()
        print("\nAll tests passed!")
    except Exception as error:
        print(f"\nTest failed: {error}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
