#!/bin/bash
# setup-all-codex.sh - Install the agent-memory CORE procedures as Codex user skills.
#
# Installs ONLY the memory core (this repo): awaken-agent, refresh-memory, wrap-up, and memory/*.
# The coding overlay (agent-memory-coding-skill) is a separate repo that ships its OWN installer.
# Each installer owns its own manifest, so they coexist in the same target dir.
#
# Usage:        bash control-files/procedures/setup-scripts/setup-all-codex.sh
# Env override: AGENT_MEMORY_TARGET_DIR (default: ~/.agents/skills)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$(dirname "$SCRIPT_DIR")"                 # control-files/procedures (awaken-agent, refresh-memory, wrap-up)
MEMORY_DIR="$CORE_DIR/memory"                       # control-files/procedures/memory
TARGET_DIR="${AGENT_MEMORY_TARGET_DIR:-$HOME/.agents/skills}"
MANIFEST_FILE="$TARGET_DIR/.agent-memory-codex-manifest"

echo "=== Setup agent-memory CORE Codex Skills ==="
echo ""
echo "Source (core):   $CORE_DIR"
echo "Source (memory): $MEMORY_DIR"
echo "Target:          $TARGET_DIR"
echo ""

if [ ! -d "$CORE_DIR" ]; then echo "Error: core directory not found: $CORE_DIR"; exit 1; fi
if [ ! -d "$MEMORY_DIR" ]; then echo "Error: memory directory not found: $MEMORY_DIR"; exit 1; fi

mkdir -p "$TARGET_DIR"

# Clean up previously installed CORE skills using the core manifest (leaves overlay skills untouched).
if [ -f "$MANIFEST_FILE" ]; then
    echo "Cleaning up previously installed core skills..."
    CLEANED=0
    while IFS= read -r skill_dir; do
        if [ -n "$skill_dir" ] && [ -d "$TARGET_DIR/$skill_dir" ]; then
            rm -rf "$TARGET_DIR/$skill_dir"
            CLEANED=$((CLEANED + 1))
        fi
    done < "$MANIFEST_FILE"
    echo "  Removed $CLEANED previously installed core skills"
    echo ""
fi

create_skill_from_markdown() {
    local source_file="$1"
    local base_name skill_dir_name skill_dir title description

    base_name="$(basename "$source_file" .md)"
    skill_dir_name="agent-memory-$base_name"
    skill_dir="$TARGET_DIR/$skill_dir_name"

    mkdir -p "$skill_dir"

    title="$(sed -n 's/^# //p' "$source_file" | head -n 1)"
    if [ -z "$title" ]; then
        title="$base_name"
    fi

    description="Use when the user wants the \"$title\" procedure or explicitly mentions $base_name."

    {
        echo "---"
        echo "name: $base_name"
        echo "description: $description"
        echo "---"
        echo ""
        echo "Follow this procedure exactly. Treat the content below as the canonical workflow."
        echo ""
        cat "$source_file"
    } > "$skill_dir/SKILL.md"

    echo "$skill_dir_name" >> "$MANIFEST_FILE"
}

: > "$MANIFEST_FILE"
TOTAL_COUNT=0
for dir in "$CORE_DIR" "$MEMORY_DIR"; do
    for file in "$dir"/*.md; do
        [ -f "$file" ] || continue
        create_skill_from_markdown "$file"
        TOTAL_COUNT=$((TOTAL_COUNT + 1))
    done
done

if [ "$TOTAL_COUNT" -eq 0 ]; then
    echo "Error: No .md files found in source directories"
    exit 1
fi

echo ""
echo "Successfully installed $TOTAL_COUNT core Codex skills!"
echo ""
echo "Installed core skills:"
while IFS= read -r skill_dir; do
    if [ -f "$TARGET_DIR/$skill_dir/SKILL.md" ]; then
        skill_name="$(sed -n 's/^name: //p' "$TARGET_DIR/$skill_dir/SKILL.md" | head -n 1)"
        echo "  \$$skill_name"
    fi
done < "$MANIFEST_FILE"
