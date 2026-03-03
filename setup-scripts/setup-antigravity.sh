#!/bin/bash
# setup-antigravity.sh - Complete Antigravity setup: user config + compile core memory + setup procedures
#
# Usage: ./control-files/setup-scripts/setup-antigravity.sh
#        bash control-files/setup-scripts/setup-antigravity.sh
#
# This script orchestrates:
#   0. User configuration (identity + OS) — skipped if already configured
#   1. Compile core memory and write to ~/.gemini/GEMINI.md
#   2. Setup all procedures as workflows in ~/.gemini/workflows/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTROL_FILES_DIR="$(dirname "$SCRIPT_DIR")"
USER_CONFIG_SCRIPT="$CONTROL_FILES_DIR/core-memory/compile-scripts/user-config.sh"
USER_PROFILE_FILE="$CONTROL_FILES_DIR/core-memory/0-core-user-profile.md"
COMPILE_WRITE_SCRIPT="$CONTROL_FILES_DIR/core-memory/compile-scripts/compile-write-to-antigravity.sh"
SETUP_PROCEDURES_SCRIPT="$CONTROL_FILES_DIR/procedures/setup-scripts/setup-all-antigravity.sh"

echo "=========================================="
echo "  Antigravity - Complete Setup"
echo "=========================================="
echo ""

# Step 0: User configuration (identity + OS)
if [ -f "$USER_PROFILE_FILE" ] && ! grep -q '\[Your Name Here\]' "$USER_PROFILE_FILE"; then
    echo "Step 0/3: User profile already configured — skipping"
    echo ""
else
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
fi

# Step 1: Compile core memory and write to GEMINI.md
echo "Step 1/3: Compile core memory → ~/.gemini/GEMINI.md"
echo "------------------------------------------"

if [ ! -f "$COMPILE_WRITE_SCRIPT" ]; then
    echo "ERROR: compile-write-to-antigravity.sh not found at $COMPILE_WRITE_SCRIPT"
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

# Step 2: Setup all procedures as workflows
echo "Step 2/3: Setup procedures → ~/.gemini/workflows/"
echo "------------------------------------------"

if [ ! -f "$SETUP_PROCEDURES_SCRIPT" ]; then
    echo "ERROR: setup-all-antigravity.sh not found at $SETUP_PROCEDURES_SCRIPT"
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
