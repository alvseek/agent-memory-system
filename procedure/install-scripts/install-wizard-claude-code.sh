#!/bin/bash
# install-wizard-claude-code.sh - Install only wizard procedures (high-wizard, quick-wizard, wide-ocean) to ~/.claude/commands/
#
# Usage: ./control-files/procedure/install-scripts/install-wizard-claude-code.sh
#        bash control-files/procedure/install-scripts/install-wizard-claude-code.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="$HOME/.claude/commands"

echo "=== Install Wizard Procedures as Slash Commands ==="
echo ""
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"
echo ""

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory not found: $SOURCE_DIR"
    exit 1
fi

# Create target directory if it doesn't exist
if [ ! -d "$TARGET_DIR" ]; then
    echo "Creating target directory: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
fi

# Count wizard files to copy
FILE_COUNT=$(ls -1 "$SOURCE_DIR"/*.md 2>/dev/null | wc -l)

if [ "$FILE_COUNT" -eq 0 ]; then
    echo "Error: No .md files found in source directory"
    exit 1
fi

# Copy wizard procedures only (root .md files)
echo "Copying $FILE_COUNT wizard procedures..."
cp "$SOURCE_DIR"/*.md "$TARGET_DIR/"

if [ $? -eq 0 ]; then
    echo ""
    echo "Successfully installed $FILE_COUNT wizard procedures!"
    echo ""
    echo "Installed commands:"
    ls -1 "$SOURCE_DIR"/*.md | xargs -I {} basename {} .md | sed 's/^/  \//'
else
    echo "Error: Failed to copy files"
    exit 1
fi
