#!/bin/bash
# setup-all-antigravity.sh - Setup all procedures (wizard + memory) to ~/.gemini/workflows/
#
# Usage: ./control-files/procedures/setup-scripts/setup-all-antigravity.sh
#        bash control-files/procedures/setup-scripts/setup-all-antigravity.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(dirname "$SCRIPT_DIR")"
MEMORY_DIR="$SOURCE_DIR/memory"
TARGET_DIR="$HOME/.gemini/workflows"
MANIFEST_FILE="$TARGET_DIR/.agent-memory-manifest"

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

# Clean up previously installed files using manifest
if [ -f "$MANIFEST_FILE" ]; then
    echo "Cleaning up previously installed workflows..."
    CLEANED=0
    while IFS= read -r filename; do
        if [ -n "$filename" ] && [ -f "$TARGET_DIR/$filename" ]; then
            rm "$TARGET_DIR/$filename"
            CLEANED=$((CLEANED + 1))
        fi
    done < "$MANIFEST_FILE"
    echo "  Removed $CLEANED stale workflows"
    echo ""
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
    # Write manifest of installed files
    : > "$MANIFEST_FILE"
    for file in "$SOURCE_DIR"/*.md; do
        basename "$file" >> "$MANIFEST_FILE"
    done
    for file in "$MEMORY_DIR"/*.md; do
        basename "$file" >> "$MANIFEST_FILE"
    done

    echo ""
    echo "Successfully installed $TOTAL_COUNT procedures as workflows!"
    echo ""
    echo "Installed workflows:"
    ls -1 "$TARGET_DIR"/*.md 2>/dev/null | xargs -I {} basename {} .md | sed 's/^/  \//'

    # First-run warning: detect unrecognized files not in manifest
    UNRECOGNIZED=""
    for file in "$TARGET_DIR"/*.md; do
        [ -f "$file" ] || continue
        fname=$(basename "$file")
        if ! grep -qxF "$fname" "$MANIFEST_FILE"; then
            UNRECOGNIZED="$UNRECOGNIZED  $fname\n"
        fi
    done

    if [ -n "$UNRECOGNIZED" ]; then
        echo ""
        echo "WARNING: Found unrecognized .md files in $TARGET_DIR"
        echo "These may be stale workflows from a previous installation:"
        echo -e "$UNRECOGNIZED"
        echo "To clean up, manually delete them from: $TARGET_DIR"
    fi
else
    echo "Error: Failed to copy files"
    exit 1
fi
