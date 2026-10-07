#!/bin/bash
# set-core-access.sh - Stamp THIS harness's memory-core access mode into its instructions file.
#
# Usage: ./set-core-access.sh <target-instructions-file> <markdown|mcp> [endpoint]
#
# The compiled core memory is shared by every harness, but whether the core is reachable as
# served procedures depends on the harness: the MCP server is configured per client, so one
# harness can have it connected while another has only the installed commands. Baking a single
# value into the shared artifact would tell a harness to fetch procedures it cannot reach, so
# each write-to-<platform>.sh stamps its own value after copying - the same rule that makes
# [GLOBAL-INSTRUCTIONS-FILE] a per-harness value.
#
# Rewrites only the two definition lines. Exits non-zero when either is not found.

TARGET="${1:-}"
MODE="${2:-markdown}"
ENDPOINT="${3:-<unset>}"

if [ -z "$TARGET" ] || [ ! -f "$TARGET" ]; then
    echo "ERROR: target instructions file not found: ${TARGET:-<empty>}"
    exit 1
fi

case "$MODE" in
    markdown|mcp) ;;
    *)
        echo "ERROR: access mode must be 'markdown' or 'mcp', got: $MODE"
        exit 1
        ;;
esac

# awk (not sed) so the backtick delimiters need no shell escaping. Values travel through the
# environment, never `-v`: -v processes escape sequences and would eat backslashes.
tmp="$(mktemp)"
if ! MODE="$MODE" ENDPOINT="$ENDPOINT" awk '
    BEGIN { bt = sprintf("%c", 96); mode = ENVIRON["MODE"]; url = ENVIRON["ENDPOINT"] }
    !fmode && index($0, "**[CORE-ACCESS]**") {
        i = index($0, bt); rest = substr($0, i + 1); j = index(rest, bt)
        if (i > 0 && j > 0) { $0 = substr($0, 1, i) mode substr(rest, j); fmode = 1 }
    }
    !furl && index($0, "**[CORE-MCP-URL]**") {
        i = index($0, bt); rest = substr($0, i + 1); j = index(rest, bt)
        if (i > 0 && j > 0) { $0 = substr($0, 1, i) url substr(rest, j); furl = 1 }
    }
    { print }
    END {
        if (!fmode) {
            print "ERROR: [CORE-ACCESS] definition not found in " FILENAME > "/dev/stderr"
            exit 1
        }
        if (!furl) {
            print "ERROR: [CORE-MCP-URL] definition not found in " FILENAME > "/dev/stderr"
            exit 1
        }
    }
' "$TARGET" > "$tmp"; then
    rm -f "$tmp"
    exit 1
fi

cp "$tmp" "$TARGET"
rm -f "$tmp"
echo "✓ [CORE-ACCESS] -> $MODE ([CORE-MCP-URL] -> $ENDPOINT)"
