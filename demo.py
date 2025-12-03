"""
Demo script for Meeting Notes Agent.

This demonstrates the agent's capabilities without requiring an actual audio file.
It simulates a meeting transcript and shows how the agent processes it.
"""

from meeting_notes_agent import MeetingNotesAgent, list_all_todos
from datetime import datetime


def demo_with_simulated_transcript():
    """Demo the agent using a simulated meeting transcript."""
    
    print("\n" + "=" * 70)
    print(" Meeting Notes Agent Demo")
    print("=" * 70)
    print()
    
    # Simulated meeting transcript
    simulated_transcript = """
    [Meeting Start]
    
    Alice: Good morning everyone! Thanks for joining today's product planning meeting.
    Let's go over our Q1 roadmap.
    
    Bob: Hi Alice, hi everyone. I think we should prioritize the mobile app redesign.
    Our user feedback has been pretty clear on that.
    
    Alice: Good point. Charlie, can you take the lead on gathering all the user 
    feedback and creating a summary document by end of this week?
    
    Charlie: Sure, I can do that. I'll have it ready by Friday.
    
    Bob: I'll also need someone to review the current design mockups. Alice, could 
    you handle that?
    
    Alice: Yes, I'll review them by next Tuesday and provide feedback.
    
    Charlie: One more thing - we need to schedule a follow-up meeting to discuss 
    the technical implementation. Bob, can you send out a calendar invite for 
    next week?
    
    Bob: Will do. I'll send that out today.
    
    Alice: Great! Let's also make sure we update the project timeline in Notion.
    Charlie, can you handle that as well?
    
    Charlie: Yep, I'll update it along with the feedback summary.
    
    Alice: Perfect. Anything else before we wrap up?
    
    Bob: I think that covers it. Thanks everyone!
    
    Alice: Thanks all! Have a great day.
    
    [Meeting End]
    """
    
    # Initialize the agent
    agent = MeetingNotesAgent()
    
    print("📝 Simulating meeting transcript processing...")
    print()
    
    # Use the agent to process the transcript and create notes
    prompt = f"""I have a transcript from a product planning meeting held today. 
Here is the full transcript:

{simulated_transcript}

Please analyze this transcript and:
1. Identify all attendees (Alice, Bob, Charlie)
2. Create a summary of the meeting
3. Extract all action items with assignees and due dates
4. Save the meeting notes using the save_meeting_notes function

The meeting name is "Product Planning - Q1 Roadmap" and the date is {datetime.now().strftime("%Y-%m-%d")}.
"""
    
    response = agent.chat(prompt)
    
    print("\n" + "=" * 70)
    print(" Agent Response")
    print("=" * 70)
    print(response)
    print()
    
    # Show all pending to-dos
    print("\n" + "=" * 70)
    print(" All Pending To-Dos")
    print("=" * 70)
    print()
    
    todos = list_all_todos()
    if todos:
        for idx, todo in enumerate(todos, 1):
            print(f"{idx}. [{todo['meeting']}]")
            print(f"   ✓ {todo['todo']}")
            print(f"   📄 File: {todo['file']}")
            print()
    else:
        print("No pending to-dos found.")
    
    print("\n" + "=" * 70)
    print(" Demo Complete!")
    print("=" * 70)
    print()
    print("✓ Meeting notes have been saved to the 'meeting_notes/' directory")
    print("✓ You can now run the agent interactively with: python meeting_notes_agent.py")
    print()


def interactive_demo():
    """Run an interactive demo."""
    
    print("\n" + "=" * 70)
    print(" Interactive Demo Mode")
    print("=" * 70)
    print()
    print("This demo will show you how to:")
    print("  1. Process a meeting transcript")
    print("  2. View all to-dos")
    print("  3. Mark a to-do as complete")
    print()
    
    agent = MeetingNotesAgent()
    
    # Step 1: Show all current to-dos
    print("\n📋 Step 1: Checking existing to-dos...")
    todos = list_all_todos()
    
    if todos:
        print(f"\nFound {len(todos)} pending to-do(s):")
        for idx, todo in enumerate(todos, 1):
            print(f"  {idx}. {todo['todo']} ({todo['meeting']})")
        
        # Step 2: Mark one as complete
        print("\n✓ Step 2: Marking the first to-do as complete...")
        first_todo = todos[0]
        response = agent.chat(
            f"Please mark this to-do as complete: '{first_todo['todo']}' "
            f"in the file '{first_todo['file']}'"
        )
        print(f"\nAgent: {response}")
        
        # Step 3: Show updated to-dos
        print("\n📋 Step 3: Checking updated to-dos...")
        updated_todos = list_all_todos()
        print(f"\nNow {len(updated_todos)} pending to-do(s) remaining.")
    else:
        print("\nNo existing to-dos found. Run the simulated transcript demo first!")
    
    print("\n" + "=" * 70)
    print(" Interactive Demo Complete!")
    print("=" * 70)


def main():
    """Run the demo."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_demo()
    else:
        demo_with_simulated_transcript()
        
        print("\n💡 Tip: Run with '--interactive' flag to see the to-do management features:")
        print("   python demo.py --interactive")


if __name__ == "__main__":
    main()

