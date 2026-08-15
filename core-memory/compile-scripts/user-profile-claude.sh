#!/bin/bash
# user-profile-claude.sh - Configure user identity for the agent memory system
#
# Usage: ./control-files/core-memory/compile-scripts/user-profile-claude.sh
#        bash control-files/core-memory/compile-scripts/user-profile-claude.sh
#
# Writes core-memory/output/0-core-user-profile.md (the runtime file compile.sh prefers
# over the template). Shows current values as defaults - press Enter to keep them.
# Idempotent: can be re-run to change values. Runs standalone or via user-config-claude.sh.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_MEMORY_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$CORE_MEMORY_DIR/output"
TEMPLATE_USER_PROFILE_FILE="$CORE_MEMORY_DIR/0-core-user-profile.md"
USER_PROFILE_FILE="$OUTPUT_DIR/0-core-user-profile.md"

mkdir -p "$OUTPUT_DIR"

# First run: seed runtime file from template if missing
if [ ! -f "$USER_PROFILE_FILE" ] && [ -f "$TEMPLATE_USER_PROFILE_FILE" ]; then
    cp "$TEMPLATE_USER_PROFILE_FILE" "$USER_PROFILE_FILE"
fi

# Read current values from existing file
CURRENT_NAME=$(grep '\[USER-NAME\]' "$USER_PROFILE_FILE" 2>/dev/null | sed 's/.*\*\* = //')
CURRENT_PHILOSOPHY=$(grep '\[USER-PHILOSOPHY\]' "$USER_PROFILE_FILE" 2>/dev/null | sed 's/.*\*\* = //')
CURRENT_VISION=$(grep '\[USER-AGENT-VISION\]' "$USER_PROFILE_FILE" 2>/dev/null | sed 's/.*\*\* = //')

# Helper: truncate long strings for display
show_default() {
    local text="$1"
    local max="${2:-60}"
    if [ ${#text} -gt "$max" ]; then
        echo "${text:0:$max}..."
    else
        echo "$text"
    fi
}

echo "=========================================="
echo "  Agent Memory - User Profile"
echo "=========================================="
echo ""
echo "Set your identity"
echo "------------------------------------------"
echo ""

if [ -n "$CURRENT_NAME" ]; then
    echo "  Current: $(show_default "$CURRENT_NAME")"
    echo "  Press Enter to keep, or type to replace."
    read -rp "  > Your name: " USER_NAME
    USER_NAME="${USER_NAME:-$CURRENT_NAME}"
else
    read -rp "  > Your name: " USER_NAME
fi
echo ""

if [ -n "$CURRENT_PHILOSOPHY" ]; then
    echo "  Current: $(show_default "$CURRENT_PHILOSOPHY")"
    echo "  Press Enter to keep, or type to replace."
    read -rp "  > Your philosophy: " USER_PHILOSOPHY
    USER_PHILOSOPHY="${USER_PHILOSOPHY:-$CURRENT_PHILOSOPHY}"
else
    read -rp "  > Your philosophy (optional): " USER_PHILOSOPHY
fi
echo ""

if [ -n "$CURRENT_VISION" ]; then
    echo "  Current: $(show_default "$CURRENT_VISION")"
    echo "  Press Enter to keep, or type to replace."
    read -rp "  > Your agent vision: " USER_AGENT_VISION
    USER_AGENT_VISION="${USER_AGENT_VISION:-$CURRENT_VISION}"
else
    read -rp "  > Your agent vision (optional): " USER_AGENT_VISION
fi
echo ""

# Write 0-core-user-profile.md
cat > "$USER_PROFILE_FILE" << EOF
## AI Agent - User Profile

- **[USER-NAME]** = $USER_NAME
- **[USER-PHILOSOPHY]** = $USER_PHILOSOPHY
- **[USER-AGENT-VISION]** = $USER_AGENT_VISION
EOF

echo "✓ User profile saved: $USER_PROFILE_FILE"
