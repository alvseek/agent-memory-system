#!/bin/bash
# setup-all-codex.sh - Install agent-memory procedures as Codex user skills
#
# Usage: ./control-files/procedures/setup-scripts/setup-all-codex.sh
#        bash control-files/procedures/setup-scripts/setup-all-codex.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(dirname "$SCRIPT_DIR")"
MEMORY_DIR="$SOURCE_DIR/memory"
TARGET_DIR="$HOME/.agents/skills"
MANIFEST_FILE="$TARGET_DIR/.agent-memory-codex-manifest"

echo "=== Setup All Procedures as Codex Skills ==="
echo ""
echo "Source (wizard): $SOURCE_DIR"
echo "Source (memory): $MEMORY_DIR"
echo "Target: $TARGET_DIR"
echo ""

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory not found: $SOURCE_DIR"
    exit 1
fi

if [ ! -d "$MEMORY_DIR" ]; then
    echo "Error: Memory directory not found: $MEMORY_DIR"
    exit 1
fi

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

SOURCE_COUNT=$(find "$SOURCE_DIR" -maxdepth 1 -type f -name '*.md' | wc -l)
MEMORY_COUNT=$(find "$MEMORY_DIR" -maxdepth 1 -type f -name '*.md' | wc -l)
TOTAL_COUNT=$((SOURCE_COUNT + MEMORY_COUNT))

if [ "$TOTAL_COUNT" -eq 0 ]; then
    echo "Error: No .md files found in source directories"
    exit 1
fi

create_skill_from_markdown() {
    local source_file="$1"
    local base_name
    local skill_dir_name
    local skill_dir
    local title
    local description

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

echo "Converting $SOURCE_COUNT wizard procedures into skills..."
for file in "$SOURCE_DIR"/*.md; do
    [ -f "$file" ] || continue
    create_skill_from_markdown "$file"
done

echo "Converting $MEMORY_COUNT memory procedures into skills..."
for file in "$MEMORY_DIR"/*.md; do
    [ -f "$file" ] || continue
    create_skill_from_markdown "$file"
done

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
