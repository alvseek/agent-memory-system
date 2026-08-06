#!/bin/bash
# setup-all-codex.sh - Install agent-memory procedures as Codex user skills.
#
# Sources the memory CORE (control-files) plus, when present, the coding-skill OVERLAY
# (agent-memory-coding-skill). A chat agent installs core only; a coding agent installs core+skill.
# Uses a manifest to track installed skills and clean up stale ones on re-run.
#
# Usage:
#   bash control-files/procedures/setup-scripts/setup-all-codex.sh             # core + skill (if overlay present)
#   bash control-files/procedures/setup-scripts/setup-all-codex.sh --core-only # force chat profile (core only)
# Env overrides:
#   AGENT_MEMORY_SKILL_DIR   path to the overlay's procedures/ dir (default: sibling of control-files)
#   AGENT_MEMORY_TARGET_DIR  install target             (default: ~/.agents/skills)
#   AGENT_MEMORY_PROFILE     set to "core-only" to force the chat profile

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$(dirname "$SCRIPT_DIR")"                 # control-files/procedures (core: awaken-agent, refresh-memory, wrap-up)
MEMORY_DIR="$CORE_DIR/memory"                       # control-files/procedures/memory
AGGREGATOR_DIR="$(cd "$CORE_DIR/../.." 2>/dev/null && pwd)"
SKILL_DIR="${AGENT_MEMORY_SKILL_DIR:-$AGGREGATOR_DIR/agent-memory-coding-skill/procedures}"
TARGET_DIR="${AGENT_MEMORY_TARGET_DIR:-$HOME/.agents/skills}"
MANIFEST_FILE="$TARGET_DIR/.agent-memory-codex-manifest"

# Profile: install the overlay when present, unless forced core-only.
INSTALL_SKILL=0
if [ "$1" = "--core-only" ] || [ "$AGENT_MEMORY_PROFILE" = "core-only" ]; then
    PROFILE="core-only"
elif [ -d "$SKILL_DIR" ]; then
    PROFILE="core+skill"
    INSTALL_SKILL=1
else
    PROFILE="core-only (overlay not found)"
fi

echo "=== Setup agent-memory Codex Skills ==="
echo ""
echo "Profile:         $PROFILE"
echo "Source (core):   $CORE_DIR"
echo "Source (memory): $MEMORY_DIR"
[ "$INSTALL_SKILL" -eq 1 ] && echo "Source (skill):  $SKILL_DIR"
echo "Target:          $TARGET_DIR"
echo ""

if [ ! -d "$CORE_DIR" ]; then echo "Error: core directory not found: $CORE_DIR"; exit 1; fi
if [ ! -d "$MEMORY_DIR" ]; then echo "Error: memory directory not found: $MEMORY_DIR"; exit 1; fi

mkdir -p "$TARGET_DIR"

if [ -f "$MANIFEST_FILE" ]; then
    echo "Cleaning up previously installed skills..."
    CLEANED=0
    while IFS= read -r skill_dir; do
        if [ -n "$skill_dir" ] && [ -d "$TARGET_DIR/$skill_dir" ]; then
            rm -rf "$TARGET_DIR/$skill_dir"
            CLEANED=$((CLEANED + 1))
        fi
    done < "$MANIFEST_FILE"
    echo "  Removed $CLEANED previously installed skills"
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

# Assemble source dirs: core always, skill when the coding profile is active.
SRC_DIRS=("$CORE_DIR" "$MEMORY_DIR")
[ "$INSTALL_SKILL" -eq 1 ] && SRC_DIRS+=("$SKILL_DIR")

: > "$MANIFEST_FILE"
TOTAL_COUNT=0
for dir in "${SRC_DIRS[@]}"; do
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
echo "Successfully installed $TOTAL_COUNT Codex skills!"
echo ""
echo "Installed skills:"
while IFS= read -r skill_dir; do
    if [ -f "$TARGET_DIR/$skill_dir/SKILL.md" ]; then
        skill_name="$(sed -n 's/^name: //p' "$TARGET_DIR/$skill_dir/SKILL.md" | head -n 1)"
        echo "  \$$skill_name"
    fi
done < "$MANIFEST_FILE"
