#!/bin/bash

# Wrapper script to run the team formation agent daily
# This script loads the .env file and uses the virtual environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Set paths
VENV_PYTHON="$PROJECT_ROOT/env/bin/python"
AGENT_SCRIPT="$SCRIPT_DIR/agentic_agent.py"
ENV_FILE="$PROJECT_ROOT/.env"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/agent_$(date +%Y%m%d_%H%M%S).log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    log "ERROR: Virtual environment Python not found at $VENV_PYTHON"
    exit 1
fi

# Check if agent script exists
if [ ! -f "$AGENT_SCRIPT" ]; then
    log "ERROR: Agent script not found at $AGENT_SCRIPT"
    exit 1
fi

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    log "WARNING: .env file not found at $ENV_FILE, continuing without it"
fi

# Load environment variables from .env file if it exists
if [ -f "$ENV_FILE" ]; then
    log "Loading environment variables from $ENV_FILE"
    set -a
    source "$ENV_FILE"
    set +a
fi

# Change to the project root directory
cd "$PROJECT_ROOT"

# Run the agent script
log "Starting team formation agent..."
log "Using Python: $VENV_PYTHON"
log "Running script: $AGENT_SCRIPT"

"$VENV_PYTHON" "$AGENT_SCRIPT" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    log "Agent completed successfully"
else
    log "ERROR: Agent exited with code $EXIT_CODE"
fi

exit $EXIT_CODE
