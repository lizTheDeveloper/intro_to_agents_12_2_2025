# Quick Start Guide

Get up and running with the Meeting Notes Agent in under 5 minutes!

## Prerequisites

- Python 3.11 or higher
- An OpenAI API key (get one at https://platform.openai.com/api-keys)

## Step 1: Set Up Environment

```bash
# Navigate to the project directory
cd intro_to_agents_12_2_2025

# Activate the virtual environment
source env/bin/activate

# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
```

💡 **Tip**: Add the export command to your `~/.zshrc` or `~/.bashrc` to make it permanent:
```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## Step 2: Run the Demo

Try the demo first to see how it works:

```bash
python demo.py
```

This will:
- Process a simulated meeting transcript
- Extract action items with assignees
- Create a Markdown file with meeting notes
- Show all pending to-dos

## Step 3: Use the Interactive Agent

```bash
python meeting_notes_agent.py
```

Then try these commands:
- `todos` - List all pending to-do items
- `process path/to/audio.mp3` - Transcribe and process a meeting recording
- Type any message to chat with the agent
- `quit` - Exit

## Step 4: Process Your First Real Meeting

If you have a meeting recording:

```bash
python meeting_notes_agent.py
```

Then type:
```
process /path/to/your/meeting.mp3
```

The agent will:
1. Transcribe the audio using Whisper
2. Analyze the transcript
3. Extract attendees, summary, and action items
4. Save a Markdown file in `meeting_notes/`

## What's Next?

- Check the generated notes in `meeting_notes/`
- View all pending to-dos with the `todos` command
- Mark items complete by chatting with the agent
- See `README.md` for advanced usage
- See `example_usage.py` for programmatic examples

## Troubleshooting

### "OPENAI_API_KEY environment variable is not set"
Make sure you've exported your API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### "No module named 'openai'"
Make sure the virtual environment is activated:
```bash
source env/bin/activate
```

### Audio file not supported
Supported formats: mp3, wav, m4a, flac, and others supported by OpenAI Whisper.
Maximum file size: 25MB

## Example Workflow

```bash
# 1. Activate environment
source env/bin/activate

# 2. Set API key (if not already set)
export OPENAI_API_KEY='sk-...'

# 3. Run the agent
python meeting_notes_agent.py

# 4. Process a meeting
> process recording.mp3

# 5. View all to-dos
> todos

# 6. Mark something complete
> Mark the task "Update documentation" as complete

# 7. Exit
> quit
```

That's it! You're ready to start managing your meeting notes with AI. 🚀

