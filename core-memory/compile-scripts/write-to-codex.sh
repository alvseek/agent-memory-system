#!/bin/bash
# Write compiled core memory to global AGENTS.md for Codex
# Usage: ./write-to-codex.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_FILE="$SCRIPT_DIR/../output/core-memory-compiled.md"
TARGET_FILE="$HOME/.codex/AGENTS.md"

echo "=== Write Core Memory to Codex AGENTS.md ==="
echo ""

if [ ! -f "$SOURCE_FILE" ]; then
    echo "ERROR: Source file not found!"
    echo "  $SOURCE_FILE"
    echo ""
    echo "Run compile.sh first to generate the compiled file."
    exit 1
fi

mkdir -p "$(dirname "$TARGET_FILE")"

echo "Source: $SOURCE_FILE"
echo "Target: $TARGET_FILE"
echo ""

if [ -f "$TARGET_FILE" ]; then
    echo "WARNING: AGENTS.md already exists!"
    echo "(A backup will be created before overwriting)"
    echo ""
    echo "Options:"
    echo "  [Y] Overwrite the existing file (backup will be created)"
    echo "  [N] Cancel and copy manually"
    echo ""
    read -p "Do you want to overwrite? (y/N): " confirm

    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        backup_file="$TARGET_FILE.backup.$(date +%Y%m%d-%H%M%S)"
        cp "$TARGET_FILE" "$backup_file"
        echo ""
        echo "Backup created: $backup_file"

        cp "$SOURCE_FILE" "$TARGET_FILE"
        echo "Codex AGENTS.md has been overwritten."
    else
        echo ""
        echo "Cancelled. To copy manually, run:"
        echo "  cp \"$SOURCE_FILE\" \"$TARGET_FILE\""
        exit 0
    fi
else
    cp "$SOURCE_FILE" "$TARGET_FILE"
    echo "Codex AGENTS.md created successfully."
fi

echo ""
echo "Done! Total lines: $(wc -l < "$TARGET_FILE")"
