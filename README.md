# Meeting Notes Agent

An AI-powered agent that transcribes meeting audio, extracts action items, and maintains organized meeting notes in Markdown format.

> 🚀 **New here?** Start with [START_HERE.md](START_HERE.md) for a 60-second overview, or jump to [QUICKSTART.md](QUICKSTART.md) for the 5-minute setup guide!

## Features

- 🎙️ **Audio Transcription**: Automatically transcribe meeting recordings using OpenAI Whisper
- ✅ **To-Do Tracking**: Extract and track action items with GitHub-style checkboxes
- 📝 **Markdown Notes**: Generate well-structured meeting notes with summaries and full transcripts
- 📋 **Cross-Meeting Tracking**: View all pending to-dos across all meetings
- ✓ **Status Updates**: Mark to-do items as complete

## Setup

1. Activate the virtual environment:
```bash
source env/bin/activate
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

3. Run the agent:
```bash
python meeting_notes_agent.py
```

## Usage

### Interactive Mode

Run the agent and interact via the command line:

```bash
python meeting_notes_agent.py
```

Available commands:
- `process <audio_file_path>` - Transcribe and process a meeting audio file
- `todos` - List all pending to-dos across all meetings
- Type any message to chat with the agent
- `quit` - Exit

### Programmatic Usage

```python
from meeting_notes_agent import MeetingNotesAgent

agent = MeetingNotesAgent()

# Process a meeting audio file
response = agent.process_meeting_audio(
    audio_file_path="path/to/meeting.mp3",
    meeting_name="Team Sync",
    date="2024-12-03"
)

# List all pending to-dos
response = agent.chat("Show me all pending to-dos")

# Mark a to-do as complete
response = agent.chat("Mark the task 'Update documentation' as complete in the team sync meeting")
```

## Meeting Notes Format

Meeting notes are saved in the `meeting_notes/` directory with the format:
`YYYY-MM-DD_meeting_name.md`

Each note includes:
- Meeting name and date
- List of attendees
- Summary of key points
- Action items with GitHub checkboxes
- Full transcript

Example:
```markdown
# Team Sync

**Date:** 2024-12-03
**Time:** 14:30

## Attendees
- Alice
- Bob
- Charlie

## Summary
Discussed Q4 goals and project timelines...

## Action Items
- [ ] Alice: Update the documentation by Friday
- [ ] Bob: Review pull request #123
- [ ] Charlie: Schedule follow-up meeting

## Full Transcript
...
```

## Supported Audio Formats

- MP3
- WAV
- M4A
- FLAC
- And other formats supported by OpenAI Whisper

## Documentation

- 📖 **[Quick Start Guide](QUICKSTART.md)** - Get running in 5 minutes
- 🔧 **[How It Works](HOW_IT_WORKS.md)** - Architecture and design explained
- 📋 **[Sample Output](SAMPLE_OUTPUT.md)** - See what generated notes look like
- 🔄 **[What Changed](CHANGES.md)** - Technical comparison with original code
- 📊 **[Project Summary](PROJECT_SUMMARY.md)** - Complete overview

## Requirements

- Python 3.11+
- OpenAI API key
- See `requirements.txt` for Python dependencies

## Project Structure

```
intro_to_agents_12_2_2025/
├── meeting_notes_agent.py    # Main agent implementation
├── meeting_notes/             # Generated meeting notes (Markdown)
├── plans/                     # Project plans and requirements
├── env/                       # Python virtual environment
└── README.md                  # This file
```

