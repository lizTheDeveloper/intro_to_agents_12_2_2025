# 🎯 START HERE

Welcome to the **Meeting Notes Agent**! This guide will get you started in 60 seconds.

## What This Does

Transforms meeting audio into organized notes with automatic to-do tracking:

```
Audio Recording  →  Transcription  →  Analysis  →  Markdown Notes + To-Dos
```

## Quick Start (60 seconds)

```bash
# 1. Activate environment
source env/bin/activate

# 2. Set your OpenAI API key
export OPENAI_API_KEY='your-key-here'

# 3. Try the demo
python demo.py
```

That's it! The demo creates example meeting notes you can review.

## What You Get

### Input: Meeting Audio
- MP3, WAV, M4A, FLAC files
- Up to 25MB

### Output: Markdown Notes
```markdown
# Product Planning Meeting

**Date:** 2024-12-03

## Attendees
- Alice
- Bob  
- Charlie

## Summary
Discussed Q1 roadmap...

## Action Items
- [ ] Alice: Review mockups by Tuesday
- [ ] Bob: Send meeting invite today
- [ ] Charlie: Update timeline by Friday

## Full Transcript
...
```

## Try It Now

### Interactive Mode
```bash
python meeting_notes_agent.py
```

Then type:
- `process meeting.mp3` - Transcribe a meeting
- `todos` - See all pending to-dos
- `quit` - Exit

### Demo Mode (No Audio Needed)
```bash
python demo.py
```

Simulates a meeting and creates example notes.

## Next Steps

1. ✅ You're here! Great start.
2. 📖 Read [QUICKSTART.md](QUICKSTART.md) for detailed setup
3. 🔍 See [SAMPLE_OUTPUT.md](SAMPLE_OUTPUT.md) for examples
4. 📚 Explore [INDEX.md](INDEX.md) for all documentation

## Quick Reference

| Want to... | Go to... |
|------------|----------|
| **Get started fast** | [QUICKSTART.md](QUICKSTART.md) |
| **See examples** | [SAMPLE_OUTPUT.md](SAMPLE_OUTPUT.md) |
| **Use in code** | [example_usage.py](example_usage.py) |
| **Understand how it works** | [HOW_IT_WORKS.md](HOW_IT_WORKS.md) |
| **Navigate everything** | [INDEX.md](INDEX.md) |

## Common Commands

```bash
# Run demo (no audio needed)
python demo.py

# Interactive agent
python meeting_notes_agent.py

# View examples
python example_usage.py
```

## Project Files

```
📁 intro_to_agents_12_2_2025/
├── 🚀 meeting_notes_agent.py    ← Main agent (run this!)
├── 🎮 demo.py                   ← Try this first!
├── 📖 QUICKSTART.md             ← 5-min guide
├── 📚 INDEX.md                  ← Navigate docs
├── 📋 README.md                 ← Full docs
└── 📁 meeting_notes/            ← Your notes go here
```

## Need Help?

**"How do I set up?"**
→ [QUICKSTART.md](QUICKSTART.md)

**"How does it work?"**
→ [HOW_IT_WORKS.md](HOW_IT_WORKS.md)

**"Show me examples"**
→ [SAMPLE_OUTPUT.md](SAMPLE_OUTPUT.md)

**"I want to code with it"**
→ [example_usage.py](example_usage.py)

## That's It!

You now have a fully functional meeting notes agent. Try the demo:

```bash
python demo.py
```

Then check `meeting_notes/` for the generated notes!

---

**Ready?** → [QUICKSTART.md](QUICKSTART.md) | **Questions?** → [INDEX.md](INDEX.md)

