#!/bin/bash
# Compile core memory and write to global Codex AGENTS.md
# Usage: ./compile-write-to-codex.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPILE_SCRIPT="$SCRIPT_DIR/compile.sh"
WRITE_SCRIPT="$SCRIPT_DIR/write-to-codex.sh"

echo "=== Compile & Write to Codex AGENTS.md ==="
echo ""

echo "Step 1: Compiling core memory files..."
echo "----------------------------------------"

if [ ! -f "$COMPILE_SCRIPT" ]; then
    echo "ERROR: compile.sh not found at $COMPILE_SCRIPT"
    exit 1
fi

bash "$COMPILE_SCRIPT"
compile_status=$?

if [ $compile_status -ne 0 ]; then
    echo ""
    echo "ERROR: Compilation failed. Aborting."
    exit 1
fi

echo ""
echo "Step 2: Writing to Codex AGENTS.md..."
echo "----------------------------------------"

if [ ! -f "$WRITE_SCRIPT" ]; then
    echo "ERROR: write-to-codex.sh not found at $WRITE_SCRIPT"
    exit 1
fi

bash "$WRITE_SCRIPT"
write_status=$?

if [ $write_status -ne 0 ]; then
    echo ""
    echo "Write cancelled or failed."
    exit $write_status
fi

echo ""
echo "=== Complete! ==="
