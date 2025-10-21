#!/bin/bash
# ADW Orchestrator Startup Script
# This script starts the ADW orchestrator in monitor mode

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
WORKSPACE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "Starting ADW Orchestrator..."
echo "Script directory: $SCRIPT_DIR"
echo "Workspace directory: $WORKSPACE_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH"
    exit 1
fi

# Check if orchestrator script exists
ORCHESTRATOR_SCRIPT="$SCRIPT_DIR/adw_orchestrator.py"
if [ ! -f "$ORCHESTRATOR_SCRIPT" ]; then
    echo "Error: ADW orchestrator script not found at $ORCHESTRATOR_SCRIPT"
    exit 1
fi

# Make sure the script is executable
chmod +x "$ORCHESTRATOR_SCRIPT"

# Create logs directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/logs"

# Start the orchestrator
echo "Starting ADW orchestrator in monitor mode..."
echo "Press Ctrl+C to stop"
echo "Logs will be written to: $SCRIPT_DIR/logs/"
echo "Monitoring for triggers in: $SCRIPT_DIR/"
echo ""

cd "$WORKSPACE_DIR"

# Run the orchestrator with workspace parameter
python3 "$ORCHESTRATOR_SCRIPT" --workspace "$WORKSPACE_DIR"