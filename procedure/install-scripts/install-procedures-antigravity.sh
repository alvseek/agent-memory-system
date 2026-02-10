#!/bin/bash
# install-slash-command-procedures-antigravity.sh - Copy all procedures to .agent/workflows/ for slash command access in Antigravity
#
# Usage: ./control-files/procedure/install-scripts/install-procedures-antigravity.sh
#        bash control-files/procedure/install-scripts/install-procedures-antigravity.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_MEMORY_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SOURCE_DIR="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="$HOME/.gemini/workflows"

echo "=== Install Procedures as Antigravity Workflows ==="
echo ""
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"
echo ""

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ Error: Source directory not found: $SOURCE_DIR"
    exit 1
fi

# Create target directory if it doesn't exist
if [ ! -d "$TARGET_DIR" ]; then
    echo "Creating target directory: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
fi

# Count files to copy
FILE_COUNT=$(ls -1 "$SOURCE_DIR"/*.md 2>/dev/null | wc -l)

if [ "$FILE_COUNT" -eq 0 ]; then
    echo "❌ Error: No .md files found in source directory"
    exit 1
fi

# Copy all procedure files
echo "Copying $FILE_COUNT procedure files..."
cp "$SOURCE_DIR"/*.md "$TARGET_DIR/"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Successfully installed $FILE_COUNT procedures as workflows!"
    echo ""
    echo "Installed workflows:"
    ls -1 "$TARGET_DIR"/*.md | xargs -I {} basename {} .md | sed 's/^/  \//'
else
    echo "❌ Error: Failed to copy files"
    exit 1
fi
