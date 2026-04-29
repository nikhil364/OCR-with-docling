#!/bin/bash

# Stop the watcher
pkill -f "watcher_docling_status.py" 2>/dev/null || true
echo "Watcher stopped."