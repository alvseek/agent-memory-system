#!/bin/bash
# setup-all-claude-code.sh - Install the agent-memory CORE procedures as ~/.claude/commands/ slash commands.
#
# Installs ONLY the memory core (this repo): awaken-agent, refresh-memory, wrap-up, and memory/*.
# The coding overlay (agent-memory-coding-skill) is a separate repo that ships its OWN installer —
# a coding agent runs both; a chat agent runs only this one. Each installer owns its own manifest,
# so they coexist in the same target dir and clean up independently.
#
# Usage:        bash control-files/procedures/setup-scripts/setup-all-claude-code.sh
# Env override: AGENT_MEMORY_TARGET_DIR (default: ~/.claude/commands)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$(dirname "$SCRIPT_DIR")"                 # control-files/procedures (awaken-agent, refresh-memory, wrap-up)
MEMORY_DIR="$CORE_DIR/memory"                       # control-files/procedures/memory
TARGET_DIR="${AGENT_MEMORY_TARGET_DIR:-$HOME/.claude/commands}"
MANIFEST_FILE="$TARGET_DIR/.agent-memory-manifest"

echo "=== Setup agent-memory CORE Slash Commands ==="
echo ""
echo "Source (core):   $CORE_DIR"
echo "Source (memory): $MEMORY_DIR"
echo "Target:          $TARGET_DIR"
echo ""

if [ ! -d "$CORE_DIR" ]; then echo "Error: core directory not found: $CORE_DIR"; exit 1; fi
if [ ! -d "$MEMORY_DIR" ]; then echo "Error: memory directory not found: $MEMORY_DIR"; exit 1; fi

mkdir -p "$TARGET_DIR"

# Clean up previously installed CORE files using the core manifest (leaves overlay commands untouched).
# Never delete a file the sibling (overlay) manifest also claims — a stale manifest entry (e.g. a command
# that moved core<->overlay in a prior session) must not delete a command the other installer owns. This
# makes the two installers order-independent and robust to cross-repo moves.
SIBLING_MANIFEST="$TARGET_DIR/.agent-memory-coding-skill-manifest"
if [ -f "$MANIFEST_FILE" ]; then
    echo "Cleaning up previously installed core commands..."
    CLEANED=0
    while IFS= read -r filename; do
        if [ -n "$filename" ] && [ -f "$TARGET_DIR/$filename" ]; then
            if [ -f "$SIBLING_MANIFEST" ] && grep -qxF "$filename" "$SIBLING_MANIFEST"; then
                continue   # owned by the overlay installer — don't delete
            fi
            rm "$TARGET_DIR/$filename"
            CLEANED=$((CLEANED + 1))
        fi
    done < "$MANIFEST_FILE"
    echo "  Removed $CLEANED stale core commands"
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

echo "Successfully installed $TOTAL_COUNT core procedures!"
echo ""
echo "Installed core commands:"
while IFS= read -r fname; do echo "  /$(basename "$fname" .md)"; done < "$MANIFEST_FILE"
