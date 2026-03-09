#!/bin/bash
# user-config.sh - Configure user identity and OS for the agent memory system
#
# Usage: ./control-files/core-memory/compile-scripts/user-config.sh
#        bash control-files/core-memory/compile-scripts/user-config.sh
#
# Shows current values as defaults. Press Enter to keep existing values.
# Idempotent: can be re-run to change values.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_MEMORY_DIR="$(dirname "$SCRIPT_DIR")"
USER_PROFILE_FILE="$CORE_MEMORY_DIR/0-core-user-profile.md"
ENV_FILE="$CORE_MEMORY_DIR/1-core-environment-memory.md"

# Read current values from existing files
CURRENT_NAME=$(grep '\[USER-NAME\]' "$USER_PROFILE_FILE" 2>/dev/null | sed 's/.*\*\* = //')
CURRENT_PHILOSOPHY=$(grep '\[USER-PHILOSOPHY\]' "$USER_PROFILE_FILE" 2>/dev/null | sed 's/.*\*\* = //')
CURRENT_VISION=$(grep '\[USER-AGENT-VISION\]' "$USER_PROFILE_FILE" 2>/dev/null | sed 's/.*\*\* = //')

# Auto-detect OS
case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*) DETECTED_OS=1 ; DETECTED_OS_NAME="Windows (Git Bash)" ;;
    Linux*)               DETECTED_OS=2 ; DETECTED_OS_NAME="Linux" ;;
    Darwin*)              DETECTED_OS=3 ; DETECTED_OS_NAME="macOS" ;;
    *)                    DETECTED_OS=""  ; DETECTED_OS_NAME="Unknown" ;;
esac

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
echo "  Agent Memory - User Configuration"
echo "=========================================="
echo ""

# --- Step 1: User Identity ---

echo "Step 1/2: Set your identity"
echo "------------------------------------------"
echo ""

if [ -n "$CURRENT_NAME" ]; then
    read -rp "Your name [$(show_default "$CURRENT_NAME")]: " USER_NAME
    USER_NAME="${USER_NAME:-$CURRENT_NAME}"
else
    read -rp "Your name: " USER_NAME
fi
echo ""

if [ -n "$CURRENT_PHILOSOPHY" ]; then
    read -rp "Your philosophy [$(show_default "$CURRENT_PHILOSOPHY")]: " USER_PHILOSOPHY
    USER_PHILOSOPHY="${USER_PHILOSOPHY:-$CURRENT_PHILOSOPHY}"
else
    read -rp "Your philosophy (what drives your approach? optional, press Enter to skip): " USER_PHILOSOPHY
fi
echo ""

if [ -n "$CURRENT_VISION" ]; then
    read -rp "Your agent vision [$(show_default "$CURRENT_VISION")]: " USER_AGENT_VISION
    USER_AGENT_VISION="${USER_AGENT_VISION:-$CURRENT_VISION}"
else
    read -rp "Your agent vision (what you want from your AI agents? optional, press Enter to skip): " USER_AGENT_VISION
fi
echo ""

# Write 0-core-user-profile.md
cat > "$USER_PROFILE_FILE" << EOF
## AI Agent - User Profile

- **[USER-NAME]** = $USER_NAME
- **[USER-PHILOSOPHY]** = $USER_PHILOSOPHY
- **[USER-AGENT-VISION]** = $USER_AGENT_VISION
EOF

echo "✓ User profile saved"
echo ""

# --- Step 2: Operating System ---

echo "Step 2/2: Set your operating system"
echo "------------------------------------------"
echo ""

if [ -n "$DETECTED_OS" ]; then
    echo "  Auto-detected: $DETECTED_OS_NAME"
    echo ""
    echo "  1) Windows (Git Bash)"
    echo "  2) Linux"
    echo "  3) macOS"
    echo ""
    read -rp "Select your OS (press Enter for $DETECTED_OS_NAME) [1-3]: " OS_CHOICE
    OS_CHOICE="${OS_CHOICE:-$DETECTED_OS}"
else
    echo "  1) Windows (Git Bash)"
    echo "  2) Linux"
    echo "  3) macOS"
    echo ""
    read -rp "Select your OS [1-3]: " OS_CHOICE
fi
echo ""

# Write 1-core-environment-memory.md with only the selected OS block
case "$OS_CHOICE" in
    1)
        cat > "$ENV_FILE" << 'EOF'
## AI Agent - Current Global Work Environment Information
- **Operating System**: Windows
- **Claude Code Bash Tool**: Runs in **Git Bash** (NOT CMD or PowerShell)
  - Use Unix-style commands: `cp`, `rm`, `ls`, `mkdir`, `cat`, `grep`
  - Use forward slashes: `/c/Users/username/.claude/` (not `C:\Users\username\.claude\`)
  - Use Unix conditionals: `test -f file && echo "exists"` (not `if exist file`)
  - CMD syntax like `if exist ... (echo) else (echo)` will FAIL
EOF
        echo "✓ OS set to: Windows (Git Bash)"
        ;;
    2)
        cat > "$ENV_FILE" << 'EOF'
## AI Agent - Current Global Work Environment Information
- **Operating System**: Linux
- **Claude Code Bash Tool**: Runs in **Bash**
  - Standard Unix commands available
  - Use `~/` for home directory: `~/.claude/`
  - All standard shell features supported
EOF
        echo "✓ OS set to: Linux"
        ;;
    3)
        cat > "$ENV_FILE" << 'EOF'
## AI Agent - Current Global Work Environment Information
- **Operating System**: macOS
- **Claude Code Bash Tool**: Runs in **Bash** (or Zsh)
  - Standard Unix commands available
  - Use `~/` for home directory: `~/.claude/`
  - All standard shell features supported
EOF
        echo "✓ OS set to: macOS"
        ;;
    *)
        echo "ERROR: Invalid choice. Please run the script again and select 1, 2, or 3."
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "  User Configuration Complete!"
echo "=========================================="
echo ""
echo "Next: Run the full setup to compile and install:"
echo "  bash control-files/setup-scripts/setup-claude-code.sh"
