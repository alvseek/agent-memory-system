#!/bin/bash
# setup-codex.sh - Complete Codex setup: user config + compile core memory + install procedures as skills
#
# Usage: ./control-files/setup-scripts/setup-codex.sh
#        bash control-files/setup-scripts/setup-codex.sh
#
# This script orchestrates:
#   0. User configuration (identity + OS) - always runs, shows defaults
#   1. Compile core memory and write to ~/.codex/AGENTS.md
#   2. Install all procedures as Codex skills in ~/.agents/skills/
#
# Notes:
#   - Codex AGENTS.md is the closest equivalent to Claude's global CLAUDE.md
#   - Codex skills are the closest equivalent to Claude slash commands
#   - Codex hooks are intentionally not configured here because official Windows support is currently disabled

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTROL_FILES_DIR="$(dirname "$SCRIPT_DIR")"
USER_CONFIG_SCRIPT="$CONTROL_FILES_DIR/core-memory/compile-scripts/user-config.sh"
COMPILE_WRITE_SCRIPT="$CONTROL_FILES_DIR/core-memory/compile-scripts/compile-write-to-codex.sh"
SETUP_PROCEDURES_SCRIPT="$CONTROL_FILES_DIR/procedures/setup-scripts/setup-all-codex.sh"

echo "=========================================="
echo "  Codex - Complete Setup"
echo "=========================================="
echo ""

echo "Step 0/3: Configure user identity and OS"
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

echo "Step 1/3: Compile core memory -> ~/.codex/AGENTS.md"
echo "------------------------------------------"

if [ ! -f "$COMPILE_WRITE_SCRIPT" ]; then
    echo "ERROR: compile-write-to-codex.sh not found at $COMPILE_WRITE_SCRIPT"
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

echo "Step 2/3: Install procedures -> ~/.agents/skills/"
echo "------------------------------------------"

if [ ! -f "$SETUP_PROCEDURES_SCRIPT" ]; then
    echo "ERROR: setup-all-codex.sh not found at $SETUP_PROCEDURES_SCRIPT"
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
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
