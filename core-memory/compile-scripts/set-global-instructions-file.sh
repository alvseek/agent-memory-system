#!/bin/bash
# set-global-instructions-file.sh - Point [GLOBAL-INSTRUCTIONS-FILE] at this harness's own file.
#
# Usage: ./set-global-instructions-file.sh <target-instructions-file>
#
# The compiled core memory (core-memory-compiled.md) is shared by every harness, but the
# [GLOBAL-INSTRUCTIONS-FILE] definition must name the file the CURRENT harness reads:
# ~/.claude/CLAUDE.md (Claude Code), ~/.config/opencode/AGENTS.md (OpenCode),
# ~/.codex/AGENTS.md (Codex), ~/.gemini/GEMINI.md (Antigravity). The configurator cannot know
# that destination, so each write-to-<platform>.sh runs this after copying. The value is
# written in the OS's native form (C:\... on Windows) to match the rest of the environment
# block.
#
# Rewrites only the definition line: the RAS reference to [GLOBAL-INSTRUCTIONS-FILE] is left
# untouched. Exits non-zero when the definition line is not found.

TARGET="${1:-}"
if [ -z "$TARGET" ] || [ ! -f "$TARGET" ]; then
    echo "ERROR: target instructions file not found: ${TARGET:-<empty>}"
    exit 1
fi

# Native path form: Git Bash ships cygpath; Linux/macOS paths are already native.
NATIVE="$TARGET"
if command -v cygpath >/dev/null 2>&1; then
    NATIVE="$(cygpath -w "$TARGET")"
fi

# awk (not sed) so the backtick delimiters need no shell escaping. The path travels through
# the environment, never `-v`: -v processes escape sequences and would eat the backslashes of
# a Windows path (C:\Users\... arrives as C:Users...).
tmp="$(mktemp)"
if ! NATIVE="$NATIVE" awk '
    BEGIN { bt = sprintf("%c", 96); p = ENVIRON["NATIVE"] }
    !found && index($0, "**[GLOBAL-INSTRUCTIONS-FILE]**") {
        i = index($0, bt)       # opening backtick of the value
        rest = substr($0, i + 1)
        j = index(rest, bt)     # closing backtick of the value
        if (i > 0 && j > 0) {
            $0 = substr($0, 1, i) p substr(rest, j)
            found = 1
        }
    }
    { print }
    END {
        if (!found) {
            print "ERROR: [GLOBAL-INSTRUCTIONS-FILE] definition not found in " FILENAME > "/dev/stderr"
            exit 1
        }
    }
' "$TARGET" > "$tmp"; then
    rm -f "$tmp"
    exit 1
fi

# cp (not mv) so the target keeps its existing permissions.
cp "$tmp" "$TARGET"
rm -f "$tmp"
echo "✓ [GLOBAL-INSTRUCTIONS-FILE] -> $NATIVE"
