#!/bin/bash
# setup-claude-code.sh - Complete Claude Code setup: user config + compile core memory + procedures + settings
#
# Usage: ./control-files/setup-scripts/setup-claude-code.sh
#        bash control-files/setup-scripts/setup-claude-code.sh
#
# This script orchestrates:
#   0. User configuration (identity + OS) — shows defaults, press Enter to keep
#   1. Compile core memory and write to ~/.claude/CLAUDE.md
#   2. Setup all procedures as slash commands in ~/.claude/commands/
#   3. Configure settings.json (hooks + bypass permissions)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTROL_FILES_DIR="$(dirname "$SCRIPT_DIR")"
USER_CONFIG_SCRIPT="$CONTROL_FILES_DIR/core-memory/compile-scripts/user-config.sh"
COMPILE_WRITE_SCRIPT="$CONTROL_FILES_DIR/core-memory/compile-scripts/compile-write-to-claude.sh"
SETUP_PROCEDURES_SCRIPT="$CONTROL_FILES_DIR/procedures/setup-scripts/setup-all-claude-code.sh"
SETUP_SETTINGS_SCRIPT="$CONTROL_FILES_DIR/scripts/setup-scripts/setup-settings-claude-code.sh"

echo "=========================================="
echo "  Claude Code - Complete Setup"
echo "=========================================="
echo ""

# Step 0: User configuration (identity + OS)
# Always run — shows current values as defaults, press Enter to keep existing
echo "Step 0/4: Configure user identity and OS"
echo "------------------------------------------"

if [ ! -f "$USER_CONFIG_SCRIPT" ]; then
    echo "ERROR: user-config.sh not found at $USER_CONFIG_SCRIPT"
    exit 1
fi

bash "$USER_CONFIG_SCRIPT"
config_status=$?

if [ $config_status -ne 0 ]; then
    echo ""
    echo "ERROR: User configuration failed. Aborting."
    exit 1
fi

echo ""

# Step 1: Compile core memory and write to CLAUDE.md
echo "Step 1/4: Compile core memory → ~/.claude/CLAUDE.md"
echo "------------------------------------------"

if [ ! -f "$COMPILE_WRITE_SCRIPT" ]; then
    echo "ERROR: compile-write-to-claude.sh not found at $COMPILE_WRITE_SCRIPT"
    exit 1
fi

bash "$COMPILE_WRITE_SCRIPT"
compile_status=$?

if [ $compile_status -ne 0 ]; then
    echo ""
    echo "ERROR: Core memory compilation failed. Aborting."
    exit 1
fi

echo ""

# Step 2: Setup all procedures as slash commands
echo "Step 2/4: Setup procedures → ~/.claude/commands/"
echo "------------------------------------------"

if [ ! -f "$SETUP_PROCEDURES_SCRIPT" ]; then
    echo "ERROR: setup-all-claude-code.sh not found at $SETUP_PROCEDURES_SCRIPT"
    exit 1
fi

bash "$SETUP_PROCEDURES_SCRIPT"
setup_status=$?

if [ $setup_status -ne 0 ]; then
    echo ""
    echo "ERROR: Procedure setup failed."
    exit $setup_status
fi

echo ""

# Step 3: Configure settings.json (hooks + bypass permissions)
echo "Step 3/4: Configure settings → ~/.claude/settings.json"
echo "------------------------------------------"

if [ ! -f "$SETUP_SETTINGS_SCRIPT" ]; then
    echo "ERROR: setup-settings-claude-code.sh not found at $SETUP_SETTINGS_SCRIPT"
    exit 1
fi

bash "$SETUP_SETTINGS_SCRIPT"
settings_status=$?

if [ $settings_status -ne 0 ]; then
    echo ""
    echo "ERROR: Settings setup failed."
    exit $settings_status
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
