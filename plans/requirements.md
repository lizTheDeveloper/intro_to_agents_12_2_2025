# Meeting Notes Agent Requirements

## Overview
Transform the basic agent framework into a meeting notes agent that can:
- Transcribe audio recordings of meetings
- Extract and track to-do items
- Maintain organized meeting notes in Markdown format

## Core Functionality

### 1. Audio Transcription
- Accept audio file paths (mp3, wav, m4a, etc.)
- Use OpenAI Whisper API for transcription
- Handle speaker diarization if possible

### 2. To-Do Extraction
- Identify action items and to-dos from meeting transcripts
- Extract assignees when mentioned
- Capture due dates when mentioned
- Track status (pending, completed)

### 3. Markdown Note Management
- Generate structured meeting notes
- Include: date, attendees, summary, action items
- Save notes in organized directory structure
- Support updating existing notes
- Use GitHub-style checkboxes for to-do items

### 4. Tools
- `transcribe_audio`: Transcribe audio file to text
- `extract_todos`: Parse transcript for action items
- `save_meeting_notes`: Save formatted notes to Markdown file
- `update_todo_status`: Mark to-do items as complete

## Technical Requirements
- Python 3.11
- OpenAI SDK (already installed)
- Handle audio files locally
- Store notes in `/meeting_notes` directory
- Use ISO date format for filenames (YYYY-MM-DD_meeting_name.md)

## User Experience
- Simple command-line interface
- Clear output of transcription progress
- Automatic note generation
- Easy to-do tracking

