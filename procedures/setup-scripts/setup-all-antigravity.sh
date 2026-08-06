#!/bin/bash
# setup-all-antigravity.sh - Install agent-memory procedures as ~/.gemini/workflows/.
#
# Sources the memory CORE (control-files) plus, when present, the coding-skill OVERLAY
# (agent-memory-coding-skill). A chat agent installs core only; a coding agent installs core+skill.
# Uses a manifest to track installed files and clean up stale workflows on re-run.
#
# Usage:
#   bash control-files/procedures/setup-scripts/setup-all-antigravity.sh             # core + skill (if overlay present)
#   bash control-files/procedures/setup-scripts/setup-all-antigravity.sh --core-only # force chat profile (core only)
# Env overrides:
#   AGENT_MEMORY_SKILL_DIR   path to the overlay's procedures/ dir (default: sibling of control-files)
#   AGENT_MEMORY_TARGET_DIR  install target             (default: ~/.gemini/workflows)
#   AGENT_MEMORY_PROFILE     set to "core-only" to force the chat profile

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$(dirname "$SCRIPT_DIR")"                 # control-files/procedures (core: awaken-agent, refresh-memory, wrap-up)
MEMORY_DIR="$CORE_DIR/memory"                       # control-files/procedures/memory
AGGREGATOR_DIR="$(cd "$CORE_DIR/../.." 2>/dev/null && pwd)"
SKILL_DIR="${AGENT_MEMORY_SKILL_DIR:-$AGGREGATOR_DIR/agent-memory-coding-skill/procedures}"
TARGET_DIR="${AGENT_MEMORY_TARGET_DIR:-$HOME/.gemini/workflows}"
MANIFEST_FILE="$TARGET_DIR/.agent-memory-manifest"

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

echo "=== Install agent-memory Workflows ==="
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

# Assemble source dirs: core always, skill when the coding profile is active.
SRC_DIRS=("$CORE_DIR" "$MEMORY_DIR")
[ "$INSTALL_SKILL" -eq 1 ] && SRC_DIRS+=("$SKILL_DIR")

# Copy each source's top-level *.md and record it in the manifest.
: > "$MANIFEST_FILE"
TOTAL_COUNT=0
for dir in "${SRC_DIRS[@]}"; do
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
