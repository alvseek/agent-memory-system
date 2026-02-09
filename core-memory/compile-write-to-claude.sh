#!/bin/bash
# Compile core memory and write to global CLAUDE.md
# Usage: ./compile-write-to-claude.sh
# This script runs compile.sh then write-to-claude.sh sequentially

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPILE_SCRIPT="$SCRIPT_DIR/compile.sh"
WRITE_SCRIPT="$SCRIPT_DIR/compiled/write-to-claude.sh"

echo "=== Compile & Write to CLAUDE.md ==="
echo ""

# Step 1: Run compile.sh
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
echo "Step 2: Writing to CLAUDE.md..."
echo "----------------------------------------"

if [ ! -f "$WRITE_SCRIPT" ]; then
    echo "ERROR: write-to-claude.sh not found at $WRITE_SCRIPT"
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
