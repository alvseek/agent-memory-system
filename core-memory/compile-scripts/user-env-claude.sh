#!/bin/bash
# user-env-claude.sh - Configure work environment (OS + agent memory path) for the agent memory system
#
# Usage: ./control-files/core-memory/compile-scripts/user-env-claude.sh
#        bash control-files/core-memory/compile-scripts/user-env-claude.sh
#
# Writes core-memory/output/1-core-environment-memory.md (the runtime file compile.sh prefers
# over the template). This script is the SINGLE writer of that file - anything the environment
# memory must carry has to be emitted here, not only in the template (a template-only edit is
# silently discarded on the next run).
#
# Idempotent: can be re-run to change values. Runs standalone or via user-config-claude.sh.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_MEMORY_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$CORE_MEMORY_DIR/output"
TEMPLATE_ENV_FILE="$CORE_MEMORY_DIR/1-core-environment-memory.md"
ENV_FILE="$OUTPUT_DIR/1-core-environment-memory.md"

mkdir -p "$OUTPUT_DIR"

# First run: seed runtime file from template if missing
if [ ! -f "$ENV_FILE" ] && [ -f "$TEMPLATE_ENV_FILE" ]; then
    cp "$TEMPLATE_ENV_FILE" "$ENV_FILE"
fi

# Read the current agent memory path NOW - Step 1 rewrites the whole file from a
# heredoc, so by Step 2 the previous value is gone and cannot be offered as a default.
# Anchored to the DEFINITION line: [STORAGE-BACKENDS-PATH] quotes [AGENT-MEMORY-PATH]
# inside its own value, so an unanchored match would return two lines.
CURRENT_PATH=$(grep '^- \*\*\[AGENT-MEMORY-PATH\]\*\* = ' "$ENV_FILE" 2>/dev/null | head -1 | sed 's/.*\*\* = `//;s/`$//')

# Auto-detect OS
case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*) DETECTED_OS=1 ; DETECTED_OS_NAME="Windows (Git Bash)" ;;
    Linux*)               DETECTED_OS=2 ; DETECTED_OS_NAME="Linux" ;;
    Darwin*)              DETECTED_OS=3 ; DETECTED_OS_NAME="macOS" ;;
    *)                    DETECTED_OS=""  ; DETECTED_OS_NAME="Unknown" ;;
esac

echo "=========================================="
echo "  Agent Memory - Work Environment"
echo "=========================================="
echo ""

# --- Step 1: Operating System ---

echo "Step 1/2: Set your operating system"
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
        STORAGE_BACKENDS_SUFFIX='\control-files\procedures\memory\storage-backends'
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
        STORAGE_BACKENDS_SUFFIX='/control-files/procedures/memory/storage-backends'
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
        STORAGE_BACKENDS_SUFFIX='/control-files/procedures/memory/storage-backends'
        ;;
    *)
        echo "ERROR: Invalid choice. Please run the script again and select 1, 2, or 3."
        exit 1
        ;;
esac

echo ""

# --- Step 2: Agent Memory Path ---

echo "Step 2/2: Set agent memory path"
echo "------------------------------------------"
echo ""

# Auto-detect based on OS choice. GLOBAL_INSTRUCTIONS_FILE is derived the same way -
# it is where write-to-claude.sh lands the compiled core memory ($HOME/.claude/CLAUDE.md),
# written in the selected OS's native form.
case "$OS_CHOICE" in
    1) DETECTED_PATH="C:\\Users\\$(whoami)\\.claude\\@agent-memory\\"
       GLOBAL_INSTRUCTIONS_FILE="C:\\Users\\$(whoami)\\.claude\\CLAUDE.md" ;;
    2) DETECTED_PATH="/home/$(whoami)/.claude/@agent-memory/"
       GLOBAL_INSTRUCTIONS_FILE="/home/$(whoami)/.claude/CLAUDE.md" ;;
    3) DETECTED_PATH="/Users/$(whoami)/.claude/@agent-memory/"
       GLOBAL_INSTRUCTIONS_FILE="/Users/$(whoami)/.claude/CLAUDE.md" ;;
esac

if [ -n "$CURRENT_PATH" ]; then
    echo "  Current: $CURRENT_PATH"
    echo "  Auto-detected: $DETECTED_PATH"
    echo "  Press Enter to keep current, or type a new path."
    read -rp "  > Agent memory path: " AGENT_MEMORY_PATH_INPUT
    AGENT_MEMORY_PATH_INPUT="${AGENT_MEMORY_PATH_INPUT:-$CURRENT_PATH}"
else
    echo "  Auto-detected: $DETECTED_PATH"
    echo "  Press Enter to accept, or type a custom path."
    read -rp "  > Agent memory path: " AGENT_MEMORY_PATH_INPUT
    AGENT_MEMORY_PATH_INPUT="${AGENT_MEMORY_PATH_INPUT:-$DETECTED_PATH}"
fi
echo ""

# Append agent memory path to environment file.
# [STORAGE-BACKENDS-PATH] is DERIVED, not prompted: it is always [AGENT-MEMORY-PATH] plus a
# fixed suffix, written with the selected OS's path separator (set in Step 1). It is emitted
# as a placeholder reference, not the expanded path, so it resolves off the line above it.
cat >> "$ENV_FILE" << EOF
- **[AGENT-MEMORY-PATH]** = \`${AGENT_MEMORY_PATH_INPUT}\`
- **[STORAGE-BACKENDS-PATH]** = \`[AGENT-MEMORY-PATH]${STORAGE_BACKENDS_SUFFIX}\` (memory procedures' concrete \`§ op\`s per storage backend — absolute so the pointer survives slash-command install)
- **[GLOBAL-INSTRUCTIONS-FILE]** = \`${GLOBAL_INSTRUCTIONS_FILE}\` (this compiled file's own destination — post-compaction recovery rereads it to restore attention position)
EOF

echo "✓ Agent memory path saved"
echo "✓ Storage backends path derived"
echo "✓ Global instructions file derived"
echo "✓ Environment saved: $ENV_FILE"
