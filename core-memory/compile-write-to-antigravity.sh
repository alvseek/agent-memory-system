#!/bin/bash
# Compile core memory and write to global GEMINI.md for Antigravity
# Usage: ./compile-write-to-antigravity.sh
# This script runs compile.sh then compiled/write-to-gemini.sh sequentially

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPILE_SCRIPT="$SCRIPT_DIR/compile.sh"
WRITE_SCRIPT="$SCRIPT_DIR/compiled/write-to-gemini.sh"

echo "=== Compile & Write to GEMINI.md (Antigravity) ==="
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
echo "Step 2: Writing to GEMINI.md..."
echo "----------------------------------------"

if [ ! -f "$WRITE_SCRIPT" ]; then
    echo "ERROR: write-to-gemini.sh not found at $WRITE_SCRIPT"
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
