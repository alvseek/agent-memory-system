#!/bin/bash
# user-config-claude.sh - Configure user identity and work environment for the agent memory system
#
# Usage: ./control-files/core-memory/compile-scripts/user-config-claude.sh
#        bash control-files/core-memory/compile-scripts/user-config-claude.sh
#
# Thin orchestrator: runs the two configurators in order. Each owns exactly one runtime
# file and can also be run on its own to change just that half.
#   user-profile-claude.sh -> core-memory/output/0-core-user-profile.md
#   user-env-claude.sh     -> core-memory/output/1-core-environment-memory.md
#
# Idempotent: can be re-run to change values.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILE_SCRIPT="$SCRIPT_DIR/user-profile-claude.sh"
ENV_SCRIPT="$SCRIPT_DIR/user-env-claude.sh"

echo "=========================================="
echo "  Agent Memory - User Configuration"
echo "=========================================="
echo ""

# --- Part 1: User Profile ---

echo "Part 1/2: User profile"
echo "------------------------------------------"
echo ""

if [ ! -f "$PROFILE_SCRIPT" ]; then
    echo "ERROR: user-profile-claude.sh not found at $PROFILE_SCRIPT"
    exit 1
fi

bash "$PROFILE_SCRIPT"
profile_status=$?

if [ $profile_status -ne 0 ]; then
    echo ""
    echo "ERROR: User profile configuration failed. Aborting."
    exit $profile_status
fi

echo ""

# --- Part 2: Work Environment ---

echo "Part 2/2: Work environment"
echo "------------------------------------------"
echo ""

if [ ! -f "$ENV_SCRIPT" ]; then
    echo "ERROR: user-env-claude.sh not found at $ENV_SCRIPT"
    exit 1
fi

bash "$ENV_SCRIPT"
env_status=$?

if [ $env_status -ne 0 ]; then
    echo ""
    echo "ERROR: Environment configuration failed. Aborting."
    exit $env_status
fi

echo ""
echo "=========================================="
echo "  User Configuration Complete!"
echo "=========================================="
echo ""
echo "Next: Run the full setup to compile and install:"
echo "  bash control-files/setup-scripts/setup-claude-code.sh"
