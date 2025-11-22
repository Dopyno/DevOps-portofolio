#!/bin/bash

TARGET_DIR="/tmp"
LOGFILE="/var/log/cleanup.log"

# 1. Check directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Directory $TARGET_DIR not found!"
    exit 1
fi

echo "Cleanup started at: $(date)" >> "$LOGFILE"

# 2. Find and delete files older than 3 days
# 👉 Your task:
# Use 'find' to search for files older than 3 days
# For each file, write to the log, then delete it.

# Example find command:
# find $TARGET_DIR -type f -mtime +3

# 3. Print completion message
echo "Cleanup completed at: $(date)" >> "$LOGFILE"

exit 0

