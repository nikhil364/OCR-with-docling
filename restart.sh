#!/bin/bash

# Stop watcher
./stop_watcher.sh
sleep 1

# Activate Python virtual environment
source ./venv/bin/activate

# Clean incomplete outputs (status.json = 1)
echo "Cleaning incomplete PDF outputs..."
incomplete_count=0
for status_file in $(find ocr_output -type f -name "status.json"); do
    status=$(jq -r '.complete_docling' "$status_file")
    if [ "$status" = "1" ]; then
        folder=$(dirname "$status_file")
        echo "Removing incomplete folder: $folder"
        rm -rf "$folder"
        ((incomplete_count++))
    fi
done

echo "Removed $incomplete_count incomplete PDF folders."

# Count completed PDFs
completed_count=$(find ocr_output -type f -name "status.json" | xargs -n1 jq -r '.complete_docling' | grep -c "^0$")
echo "Completed PDFs: $completed_count"

# Start watcher in background
nohup python3 watcher_docling_status.py > watcher.log 2>&1 &

echo "Watcher restarted in background. Logs in watcher.log"