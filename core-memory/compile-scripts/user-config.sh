#!/bin/bash
# user-config.sh - Configure user identity and OS for the agent memory system
#
# Usage: ./control-files/core-memory/compile-scripts/user-config.sh
#        bash control-files/core-memory/compile-scripts/user-config.sh
#
# This script asks for:
#   1. User name, philosophy, and agent vision → writes to 0-core-user-profile.md
#   2. Operating system → writes the selected OS block to 1-core-environment-memory.md
#
# Idempotent: can be re-run to change values.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_MEMORY_DIR="$(dirname "$SCRIPT_DIR")"
USER_PROFILE_FILE="$CORE_MEMORY_DIR/0-core-user-profile.md"
ENV_FILE="$CORE_MEMORY_DIR/1-core-environment-memory.md"

echo "=========================================="
echo "  Agent Memory - User Configuration"
echo "=========================================="
echo ""

# --- Step 1: User Identity ---

echo "Step 1/2: Set your identity"
echo "------------------------------------------"
echo ""

read -rp "Your name: " USER_NAME
echo ""
read -rp "Your philosophy (what drives your approach to building software? optional, press Enter to skip): " USER_PHILOSOPHY
echo ""
read -rp "Your agent vision (what you want from your AI agent ecosystem? optional, press Enter to skip): " USER_AGENT_VISION
echo ""

# Write 0-core-user-profile.md
cat > "$USER_PROFILE_FILE" << EOF
## AI Agent - User Profile

- **[USER-NAME]** = $USER_NAME
- **[USER-PHILOSOPHY]** = $USER_PHILOSOPHY
- **[USER-AGENT-VISION]** = $USER_AGENT_VISION
EOF

echo "✓ User profile written to: $USER_PROFILE_FILE"
echo ""

# --- Step 2: Operating System ---

echo "Step 2/2: Set your operating system"
echo "------------------------------------------"
echo ""
echo "  1) Windows (Git Bash)"
echo "  2) Linux"
echo "  3) macOS"
echo ""
read -rp "Select your OS [1-3]: " OS_CHOICE
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
