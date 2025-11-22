#!/bin/bash

TARGET_DIR="/Users/mariusiordan/Documents/Documents/Screenshoots"
LOGFILE="/var/log/cleanup.log"

# 1. Check directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Directory $TARGET_DIR not found!"
    exit 1
fi

echo "Cleanup started at: $(date)" >> "$LOGFILE"

# find $TARGET_DIR -type f -mtime +3

for file in $(find "$TARGET_DIR" -type f -name "*.png" -mtime +180); do
    echo "Deleting at: $file" >> "$LOGFILE"
    rm -f "$file"
done

# 3. Print completion message
echo "Cleanup completed at: $(date)" >> "$LOGFILE"

exit 0







