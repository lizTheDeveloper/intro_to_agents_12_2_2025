# How It Works: Meeting Notes Agent

A visual guide to understanding the agent's architecture and flow.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Meeting Notes Agent                       │
│                                                              │
│  ┌────────────┐      ┌──────────────┐      ┌────────────┐  │
│  │   User     │─────▶│    Agent     │◀─────│  OpenAI    │  │
│  │  Input     │      │   (GPT-4o)   │      │    API     │  │
│  └────────────┘      └──────┬───────┘      └────────────┘  │
│                             │                               │
│                             ▼                               │
│                    ┌─────────────────┐                      │
│                    │  Tool Executor  │                      │
│                    └────────┬────────┘                      │
│                             │                               │
│         ┌───────────────────┼───────────────────┐           │
│         ▼                   ▼                   ▼           │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────┐     │
│  │ Transcribe  │   │     Save     │   │   Manage    │     │
│  │   Audio     │   │    Notes     │   │   To-Dos    │     │
│  └─────────────┘   └──────────────┘   └─────────────┘     │
│         │                   │                   │           │
│         ▼                   ▼                   ▼           │
│  ┌──────────────────────────────────────────────────┐      │
│  │            Local File System                     │      │
│  │        meeting_notes/*.md files                  │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Processing Flow

### 1. Audio to Transcript

```
Audio File (MP3/WAV/M4A)
        │
        ▼
┌──────────────────┐
│  transcribe_     │
│  audio()         │
│                  │
│  OpenAI Whisper  │
└────────┬─────────┘
         │
         ▼
   Text Transcript
```

### 2. Analysis & Extraction

```
Text Transcript
        │
        ▼
┌──────────────────────┐
│      GPT-4o          │
│  (Agent Analysis)    │
│                      │
│  Extracts:           │
│  • Attendees         │
│  • Summary           │
│  • Action Items      │
│  • Due Dates         │
│  • Assignees         │
└────────┬─────────────┘
         │
         ▼
  Structured Data
```

### 3. Note Generation

```
Structured Data
        │
        ▼
┌──────────────────────┐
│  save_meeting_       │
│  notes()             │
│                      │
│  Formats:            │
│  • Markdown header   │
│  • Attendee list     │
│  • Summary section   │
│  • To-do checkboxes  │
│  • Full transcript   │
└────────┬─────────────┘
         │
         ▼
meeting_notes/
YYYY-MM-DD_name.md
```

## Agent Conversation Loop

```
Start
  │
  ▼
User sends message
  │
  ▼
Add to conversation history
  │
  ▼
Call OpenAI API
  │
  ├──────────┐
  │          ▼
  │    Tool calls needed?
  │          │
  │         Yes ──▶ Execute each tool
  │          │           │
  │          │           ▼
  │          │     Add results to history
  │          │           │
  │          └───────────┘
  │          │
  │         No
  │          │
  ▼          ▼
Return response to user
  │
  ▼
Ready for next message
```

## Tool Execution Flow

```
┌─────────────────────────────────────────────────┐
│  Agent decides to use a tool                    │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  Parse function name and arguments              │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌──────────────┐    ┌──────────────┐
│ Audio tool?  │    │  Notes tool? │
└──────┬───────┘    └──────┬───────┘
       │                   │
       ▼                   ▼
┌──────────────┐    ┌──────────────┐
│ Call Whisper │    │ Write to file│
└──────┬───────┘    └──────┬───────┘
       │                   │
       └─────────┬─────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  Return result to agent                         │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  Agent continues conversation with result       │
└─────────────────────────────────────────────────┘
```

## File Structure & Data Flow

```
meeting_notes/
│
├── 2024-12-03_team_sync.md
│   ├── Header (date, time)
│   ├── Attendees list
│   ├── Summary
│   ├── Action Items
│   │   ├── - [ ] Task 1
│   │   ├── - [x] Task 2 (completed)
│   │   └── - [ ] Task 3
│   └── Full Transcript
│
└── 2024-12-04_product_planning.md
    └── (same structure)

              │
              ▼
     list_all_todos()
     scans all files
              │
              ▼
    Finds unchecked items:
    - [ ] Task 1 (team_sync)
    - [ ] Task 3 (team_sync)
              │
              ▼
    update_todo_status()
    changes [ ] to [x]
```

## User Interaction Modes

### Mode 1: Interactive CLI

```
Terminal
   │
   ▼
python meeting_notes_agent.py
   │
   ▼
┌─────────────────────┐
│  Agent Prompt       │
│  You:               │
└─────────────────────┘
   │
   ├─▶ "process file.mp3"  ─▶ Transcribe & analyze
   ├─▶ "todos"             ─▶ List all to-dos
   ├─▶ "mark X complete"   ─▶ Update status
   └─▶ "quit"              ─▶ Exit
```

### Mode 2: Programmatic

```python
from meeting_notes_agent import MeetingNotesAgent

agent = MeetingNotesAgent()
        │
        ▼
agent.process_meeting_audio("file.mp3")
        │
        ▼
agent.chat("Show all todos")
        │
        ▼
Results returned to your code
```

### Mode 3: Demo

```
python demo.py
   │
   ▼
Simulated transcript
   │
   ▼
Agent processes automatically
   │
   ▼
Shows results
   │
   ▼
Creates example files
```

## Tool Deep Dive

### transcribe_audio()

```
Input: audio_file_path
  │
  ▼
Open file
  │
  ▼
Send to OpenAI Whisper API
  │
  ▼
Receive transcript
  │
  ▼
Output: text string
```

### save_meeting_notes()

```
Input: {
  meeting_name,
  date,
  attendees[],
  summary,
  transcript,
  todos[]
}
  │
  ▼
Format Markdown
  │
  ▼
Create filename
  │
  ▼
Write to file
  │
  ▼
Output: filepath
```

### list_all_todos()

```
Input: (none)
  │
  ▼
Scan meeting_notes/
  │
  ▼
For each .md file:
  ├─▶ Read content
  ├─▶ Find "- [ ]" lines
  └─▶ Extract text
  │
  ▼
Output: [{meeting, file, todo}]
```

### update_todo_status()

```
Input: {filename, todo_text, completed}
  │
  ▼
Read file
  │
  ▼
Find matching line
  │
  ▼
Replace "- [ ]" with "- [x]"
  │
  ▼
Write file
  │
  ▼
Output: confirmation
```

## Key Design Patterns

### 1. Separation of Concerns
- Tools: Pure functions with single responsibility
- Agent: Orchestration and conversation management
- Storage: File system operations isolated

### 2. Conversation State
- History maintained throughout session
- Each message adds context
- Tool results feed back into conversation

### 3. Error Handling
```
Try Operation
  │
  ├─▶ Success ──▶ Return result
  │
  └─▶ Error ──▶ Log error
              └─▶ Return error message
```

### 4. Logging
```
Every operation:
  - Log entry
  - Execute
  - Log result
  - Return
```

## Data Transformations

```
Audio (Binary)
    ↓
Transcript (Text)
    ↓
Structured Data (JSON-like)
    ↓
Markdown (Formatted Text)
    ↓
File System (Persistent)
```

## Summary

The agent follows a clean, modular architecture:
1. **User Interface**: CLI or programmatic
2. **Agent Core**: GPT-4o with tool calling
3. **Tools**: Specialized functions
4. **Storage**: Markdown files
5. **State**: Conversation history

Each component is independent, testable, and maintainable.

