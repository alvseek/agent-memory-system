#!/bin/bash
# setup-opencode.sh - Complete OpenCode setup (thin wrapper over setup-opencode.py)
#
# Usage: ./control-files/setup-scripts/setup-opencode.sh [--yes]
#        bash control-files/setup-scripts/setup-opencode.sh [--yes]
#
# The Python orchestrator is the real implementation (cross-platform + JSONC-safe
# settings merge). This wrapper keeps the repo's setup-scripts convention where
# every platform has a matching .sh entrypoint.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SETUP_PYTHON="$(command -v python3 || command -v python)"
if [ -z "$SETUP_PYTHON" ]; then
    echo "ERROR: python3/python not found (needed to run setup-opencode.py)"
    exit 1
fi

exec "$SETUP_PYTHON" "$SCRIPT_DIR/setup-opencode.py" "$@"
