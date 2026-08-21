#!/bin/bash
# user-profile-claude.sh - Configure user identity for the agent memory system
#
# Usage: ./control-files/core-memory/compile-scripts/user-profile-claude.sh
#        bash control-files/core-memory/compile-scripts/user-profile-claude.sh
#
# Writes TWO files, and the distinction matters:
#   [AGENT-MEMORY-PATH]/shared-memory/user-profile.md  - the SOURCE OF TRUTH. Private,
#       outside the public framework repo, and also what the memory server imports.
#   core-memory/output/0-core-user-profile.md          - DERIVED from it on every run.
#       compile.sh finds core-memory sources by filename inside output/, so this copy is
#       what carries the profile into the global instructions file. Never edit it.
#
# Requires [AGENT-MEMORY-PATH], which it READS from the environment configurator's output
# rather than deriving - a submodule must not reason about whatever contains it. That is
# why user-config-claude.sh runs the environment half first.
#
# Shows current values as defaults - press Enter to keep them.
# Idempotent: can be re-run to change values. Runs standalone or via user-config-claude.sh.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_MEMORY_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$CORE_MEMORY_DIR/output"
ENV_FILE="$OUTPUT_DIR/1-core-environment-memory.md"
RUNTIME_PROFILE_FILE="$OUTPUT_DIR/0-core-user-profile.md"

mkdir -p "$OUTPUT_DIR"

# Where the profile actually lives. [AGENT-MEMORY-PATH] is READ from the environment
# configurator's output, never derived from this script's own location: control-files is
# a submodule and must not reason about whatever contains it, or a standalone clone of the
# public repo would be computing a path to a private store that isn't there. That is why
# user-config-claude.sh runs the environment half FIRST.
AGENT_MEMORY_PATH=$(sed -n 's/^- \*\*\[AGENT-MEMORY-PATH\]\*\* = `\(.*\)`$/\1/p' "$ENV_FILE" 2>/dev/null | head -1)
if [ -z "$AGENT_MEMORY_PATH" ]; then
    echo "ERROR: [AGENT-MEMORY-PATH] is not set."
    echo "       Run user-env-claude.sh first — user-config-claude.sh does that for you."
    echo "       This script will not guess where to put private values."
    exit 1
fi

# The env file stores a native OS path; convert on Windows so bash can use it.
STORE_DIR="$AGENT_MEMORY_PATH"
if command -v cygpath >/dev/null 2>&1; then
    STORE_DIR="$(cygpath -u "$AGENT_MEMORY_PATH" 2>/dev/null || echo "$AGENT_MEMORY_PATH")"
fi
USER_PROFILE_FILE="${STORE_DIR%/}/shared-memory/user-profile.md"

if [ ! -d "${STORE_DIR%/}/shared-memory" ]; then
    echo "ERROR: no shared-memory/ under $STORE_DIR"
    echo "       [AGENT-MEMORY-PATH] does not point at an agent-memory store."
    exit 1
fi

# Read current values. `sed -n …p` prints ONLY on a match, so an absent line and an empty
# value both yield "" — a plain `sed s///` would echo the whole line back when it failed
# to match, and that unmatched line would then be offered as a keep-this default.
read_field() { sed -n "s/^- \*\*\[$1\]\*\* = //p" "$USER_PROFILE_FILE" 2>/dev/null | head -1; }
CURRENT_NAME=$(read_field "USER-NAME")
CURRENT_PHILOSOPHY=$(read_field "USER-PHILOSOPHY")
CURRENT_VISION=$(read_field "USER-AGENT-VISION")

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

# Write the source of truth: the private store. One authored copy, outside the public repo.
if ! cat > "$USER_PROFILE_FILE" << EOF
## AI Agent - User Profile

- **[USER-NAME]** = $USER_NAME
- **[USER-PHILOSOPHY]** = $USER_PHILOSOPHY
- **[USER-AGENT-VISION]** = $USER_AGENT_VISION
EOF
then
    echo "ERROR: could not write $USER_PROFILE_FILE"
    exit 1
fi

# Materialize the compile input from it. It is DERIVED, never edited: output/ is
# gitignored, so the values stay out of the public repo, and re-running this refreshes it.
if ! cp "$USER_PROFILE_FILE" "$RUNTIME_PROFILE_FILE"; then
    echo "ERROR: profile saved to $USER_PROFILE_FILE, but the compile input at"
    echo "       $RUNTIME_PROFILE_FILE could not be refreshed — the global instructions"
    echo "       file will still carry the previous values until this succeeds."
    exit 1
fi

echo "✓ User profile saved: $USER_PROFILE_FILE"
echo "  compile input refreshed: $RUNTIME_PROFILE_FILE"
