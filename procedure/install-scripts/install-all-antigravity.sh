#!/bin/bash
# install-procedures-antigravity.sh - Install all procedures (wizard + memory) to ~/.gemini/workflows/
#
# Usage: ./control-files/procedure/install-scripts/install-procedures-antigravity.sh
#        bash control-files/procedure/install-scripts/install-procedures-antigravity.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(dirname "$SCRIPT_DIR")"
MEMORY_DIR="$SOURCE_DIR/memory"
TARGET_DIR="$HOME/.gemini/workflows"

echo "=== Install All Procedures as Antigravity Workflows ==="
echo ""
echo "Source (wizard): $SOURCE_DIR"
echo "Source (memory): $MEMORY_DIR"
echo "Target: $TARGET_DIR"
echo ""

# Check if source directories exist
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory not found: $SOURCE_DIR"
    exit 1
fi

if [ ! -d "$MEMORY_DIR" ]; then
    echo "Error: Memory directory not found: $MEMORY_DIR"
    exit 1
fi

# Create target directory if it doesn't exist
if [ ! -d "$TARGET_DIR" ]; then
    echo "Creating target directory: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
fi

# Count files to copy
WIZARD_COUNT=$(ls -1 "$SOURCE_DIR"/*.md 2>/dev/null | wc -l)
MEMORY_COUNT=$(ls -1 "$MEMORY_DIR"/*.md 2>/dev/null | wc -l)
TOTAL_COUNT=$((WIZARD_COUNT + MEMORY_COUNT))

if [ "$TOTAL_COUNT" -eq 0 ]; then
    echo "Error: No .md files found in source directories"
    exit 1
fi

# Copy wizard procedures
echo "Copying $WIZARD_COUNT wizard procedures..."
cp "$SOURCE_DIR"/*.md "$TARGET_DIR/"

# Copy memory procedures
echo "Copying $MEMORY_COUNT memory procedures..."
cp "$MEMORY_DIR"/*.md "$TARGET_DIR/"

if [ $? -eq 0 ]; then
    echo ""
    echo "Successfully installed $TOTAL_COUNT procedures as workflows!"
    echo ""
    echo "Installed workflows:"
    ls -1 "$TARGET_DIR"/*.md 2>/dev/null | xargs -I {} basename {} .md | sed 's/^/  \//'
else
    echo "Error: Failed to copy files"
    exit 1
fi
