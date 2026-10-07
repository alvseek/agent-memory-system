#!/bin/bash
# Write compiled core memory to global AGENTS.md for OpenCode
# Usage: ./write-to-opencode.sh
#
# OpenCode V2 loads ~/.config/opencode/AGENTS.md as its global instruction file
# (the equivalent of Claude Code's ~/.claude/CLAUDE.md). It does NOT use
# CLAUDE.md as a fallback.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_FILE="$SCRIPT_DIR/../output/core-memory-compiled.md"
TARGET_FILE="$HOME/.config/opencode/AGENTS.md"

echo "=== Write Core Memory to OpenCode AGENTS.md ==="
echo ""

# Check if source file exists
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

# Check if target file exists
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
        # Create backup first
        backup_file="$TARGET_FILE.backup.$(date +%Y%m%d-%H%M%S)"
        cp "$TARGET_FILE" "$backup_file"
        echo ""
        echo "Backup created: $backup_file"

        # Overwrite
        cp "$SOURCE_FILE" "$TARGET_FILE"
        echo "OpenCode AGENTS.md has been overwritten."
    else
        echo ""
        echo "Cancelled. To copy manually, run:"
        echo "  cp \"$SOURCE_FILE\" \"$TARGET_FILE\""
        exit 0
    fi
else
    # No existing file, just copy
    cp "$SOURCE_FILE" "$TARGET_FILE"
    echo "OpenCode AGENTS.md created successfully."
fi

# [GLOBAL-INSTRUCTIONS-FILE] is the one platform-specific line in the compiled memory;
# stamp this harness's own destination now that the file is in place.
bash "$SCRIPT_DIR/set-global-instructions-file.sh" "$TARGET_FILE" || exit 1

# Core access is a per-client fact (is the MCP server connected HERE?), so stamp it per harness.
bash "$SCRIPT_DIR/set-core-access.sh" "$TARGET_FILE" "${CORE_ACCESS:-markdown}" "${CORE_MCP_URL:-<unset>}" || exit 1

echo ""
echo "Done! Total lines: $(wc -l < "$TARGET_FILE")"
