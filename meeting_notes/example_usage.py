"""
Example usage script for the Meeting Notes Agent.

This demonstrates various ways to use the agent programmatically.
"""

from meeting_notes_agent import MeetingNotesAgent, list_all_todos
from pathlib import Path


def example_1_process_audio():
    """Example: Process a meeting audio file."""
    print("\n" + "=" * 60)
    print("Example 1: Process Meeting Audio")
    print("=" * 60)
    
    agent = MeetingNotesAgent()
    
    # Replace with actual audio file path
    audio_file = "path/to/your/meeting.mp3"
    
    if Path(audio_file).exists():
        response = agent.process_meeting_audio(
            audio_file_path=audio_file,
            meeting_name="Weekly Team Sync",
            date="2024-12-03"
        )
        print(f"\nAgent Response:\n{response}")
    else:
        print(f"\nNote: Audio file not found at {audio_file}")
        print("To use this example, provide a valid audio file path.")


def example_2_chat_interface():
    """Example: Use the chat interface to interact with the agent."""
    print("\n" + "=" * 60)
    print("Example 2: Chat Interface")
    print("=" * 60)
    
    agent = MeetingNotesAgent()
    
    # Ask the agent to list all to-dos
    response = agent.chat("Can you show me all pending to-do items?")
    print(f"\nAgent Response:\n{response}")


def example_3_direct_tool_usage():
    """Example: Directly use the tools without the agent."""
    print("\n" + "=" * 60)
    print("Example 3: Direct Tool Usage")
    print("=" * 60)
    
    # List all todos directly
    todos = list_all_todos()
    
    if todos:
        print("\nAll Pending To-Dos:")
        for todo in todos:
            print(f"  📋 [{todo['meeting']}] {todo['todo']}")
            print(f"     File: {todo['file']}")
    else:
        print("\nNo pending to-dos found.")


def example_4_custom_workflow():
    """Example: Custom workflow for processing multiple meetings."""
    print("\n" + "=" * 60)
    print("Example 4: Batch Processing")
    print("=" * 60)
    
    agent = MeetingNotesAgent()
    
    # List of meetings to process
    meetings = [
        {
            "audio": "meeting1.mp3",
            "name": "Product Planning",
            "date": "2024-12-01"
        },
        {
            "audio": "meeting2.mp3",
            "name": "Engineering Sync",
            "date": "2024-12-02"
        },
    ]
    
    for meeting in meetings:
        if Path(meeting["audio"]).exists():
            print(f"\nProcessing: {meeting['name']}")
            response = agent.process_meeting_audio(
                audio_file_path=meeting["audio"],
                meeting_name=meeting["name"],
                date=meeting["date"]
            )
            print(f"✓ Completed: {meeting['name']}")
        else:
            print(f"\n⚠ Skipping {meeting['name']}: Audio file not found")


def example_5_mark_complete():
    """Example: Mark a to-do item as complete."""
    print("\n" + "=" * 60)
    print("Example 5: Update To-Do Status")
    print("=" * 60)
    
    agent = MeetingNotesAgent()
    
    # First, check if there are any to-dos
    todos = list_all_todos()
    
    if todos:
        # Mark the first to-do as complete
        first_todo = todos[0]
        response = agent.chat(
            f"Please mark this to-do as complete: '{first_todo['todo']}' "
            f"from the file '{first_todo['file']}'"
        )
        print(f"\nAgent Response:\n{response}")
    else:
        print("\nNo to-dos available to mark as complete.")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print(" Meeting Notes Agent - Example Usage")
    print("=" * 70)
    
    examples = [
        ("Process Audio File", example_1_process_audio),
        ("Chat Interface", example_2_chat_interface),
        ("Direct Tool Usage", example_3_direct_tool_usage),
        ("Batch Processing", example_4_custom_workflow),
        ("Update To-Do Status", example_5_mark_complete),
    ]
    
    print("\nAvailable Examples:")
    for idx, (name, _) in enumerate(examples, 1):
        print(f"  {idx}. {name}")
    
    print("\nRunning all examples...\n")
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as error:
            print(f"\n⚠ Error in {name}: {error}")
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

