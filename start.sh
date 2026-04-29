#!/bin/bash

# Activate Python virtual environment
source ./venv/bin/activate

# Stop any existing watcher first
pkill -f "watcher_docling_status.py" 2>/dev/null || true

# Start the watcher in background
nohup python3 watcher_docling_status.py > watcher.log 2>&1 &

echo "Watcher started in background. Logs in watcher.log"