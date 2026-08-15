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
#   3. Configure Codex settings (tool_output_token_limit + SessionStart hook)
#
# Notes:
#   - Codex AGENTS.md is the closest equivalent to Claude's global CLAUDE.md
#   - Codex skills are the closest equivalent to Claude slash commands
#   - SessionStart hook is configured to inject memory recovery reminder context

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTROL_FILES_DIR="$(dirname "$SCRIPT_DIR")"
# Shares the Claude configurator: what it writes (profile + env) is platform-agnostic today.
# A Codex-specific configurator is deferred.
USER_CONFIG_SCRIPT="$CONTROL_FILES_DIR/core-memory/compile-scripts/user-config-claude.sh"
COMPILE_WRITE_SCRIPT="$CONTROL_FILES_DIR/core-memory/compile-scripts/compile-write-to-codex.sh"
SETUP_PROCEDURES_SCRIPT="$CONTROL_FILES_DIR/procedures/setup-scripts/setup-all-codex.sh"
SETUP_SETTINGS_SCRIPT="$CONTROL_FILES_DIR/scripts/setup-scripts/setup-settings-codex.sh"

echo "=========================================="
echo "  Codex - Complete Setup"
echo "=========================================="
echo ""

echo "Step 0/4: Configure user identity and OS"
echo "------------------------------------------"

if [ ! -f "$USER_CONFIG_SCRIPT" ]; then
    echo "ERROR: user-config-claude.sh not found at $USER_CONFIG_SCRIPT"
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

echo "Step 1/4: Compile core memory -> ~/.codex/AGENTS.md"
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

echo "Step 2/4: Install procedures -> ~/.agents/skills/"
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

echo "Step 3/4: Configure Codex settings -> ~/.codex/config.toml"
echo "------------------------------------------"

if [ ! -f "$SETUP_SETTINGS_SCRIPT" ]; then
    echo "ERROR: setup-settings-codex.sh not found at $SETUP_SETTINGS_SCRIPT"
    exit 1
fi

bash "$SETUP_SETTINGS_SCRIPT"
settings_status=$?

if [ $settings_status -ne 0 ]; then
    echo ""
    echo "ERROR: Codex settings setup failed."
    exit $settings_status
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
