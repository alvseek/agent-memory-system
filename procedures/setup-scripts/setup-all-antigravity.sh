#!/bin/bash
# setup-all-antigravity.sh - Install the agent-memory CORE procedures as ~/.gemini/workflows/.
#
# Installs ONLY the memory core (this repo): awaken-agent, refresh-memory, wrap-up, and memory/*.
# The coding overlay (agent-memory-coding-skill) is a separate repo that ships its OWN installer.
# Each installer owns its own manifest, so they coexist in the same target dir.
#
# Usage:        bash control-files/procedures/setup-scripts/setup-all-antigravity.sh
# Env override: AGENT_MEMORY_TARGET_DIR (default: ~/.gemini/workflows)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$(dirname "$SCRIPT_DIR")"                 # control-files/procedures (awaken-agent, refresh-memory, wrap-up)
MEMORY_DIR="$CORE_DIR/memory"                       # control-files/procedures/memory
TARGET_DIR="${AGENT_MEMORY_TARGET_DIR:-$HOME/.gemini/workflows}"
MANIFEST_FILE="$TARGET_DIR/.agent-memory-manifest"

echo "=== Install agent-memory CORE Workflows ==="
echo ""
echo "Source (core):   $CORE_DIR"
echo "Source (memory): $MEMORY_DIR"
echo "Target:          $TARGET_DIR"
echo ""

if [ ! -d "$CORE_DIR" ]; then echo "Error: core directory not found: $CORE_DIR"; exit 1; fi
if [ ! -d "$MEMORY_DIR" ]; then echo "Error: memory directory not found: $MEMORY_DIR"; exit 1; fi

mkdir -p "$TARGET_DIR"

# Clean up previously installed CORE files using the core manifest (leaves overlay workflows untouched).
if [ -f "$MANIFEST_FILE" ]; then
    echo "Cleaning up previously installed core workflows..."
    CLEANED=0
    while IFS= read -r filename; do
        if [ -n "$filename" ] && [ -f "$TARGET_DIR/$filename" ]; then
            rm "$TARGET_DIR/$filename"
            CLEANED=$((CLEANED + 1))
        fi
    done < "$MANIFEST_FILE"
    echo "  Removed $CLEANED stale core workflows"
    echo ""
fi

# Copy core top-level *.md + memory/*.md; record each in the core manifest.
: > "$MANIFEST_FILE"
TOTAL_COUNT=0
for dir in "$CORE_DIR" "$MEMORY_DIR"; do
    for file in "$dir"/*.md; do
        [ -f "$file" ] || continue
        cp "$file" "$TARGET_DIR/"
        basename "$file" >> "$MANIFEST_FILE"
        TOTAL_COUNT=$((TOTAL_COUNT + 1))
    done
done

if [ "$TOTAL_COUNT" -eq 0 ]; then
    echo "Error: No .md files found in source directories"
    exit 1
fi

echo "Successfully installed $TOTAL_COUNT core procedures as workflows!"
echo ""
echo "Installed core workflows:"
while IFS= read -r fname; do echo "  /$(basename "$fname" .md)"; done < "$MANIFEST_FILE"
