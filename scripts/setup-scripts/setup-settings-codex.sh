#!/bin/bash
# setup-settings-codex.sh - Configure ~/.codex/config.toml
#
# Configures:
#   - tool_output_token_limit = 64000 (prevents truncation for large memory files)
#   - Codex SessionStart hook for memory recovery reminder (same intention as Claude SessionStart:compact)
#
# Usage: bash control-files/scripts/setup-scripts/setup-settings-codex.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$(dirname "$SCRIPT_DIR")"  # control-files/scripts/
CODEX_HOOK_SCRIPT="$SCRIPTS_DIR/codex-agent-refresh.sh"
CODEX_CONFIG_PATH="$HOME/.codex/config.toml"

if [ ! -f "$CODEX_HOOK_SCRIPT" ]; then
    echo "ERROR: codex-agent-refresh.sh not found at $CODEX_HOOK_SCRIPT"
    exit 1
fi

mkdir -p "$(dirname "$CODEX_CONFIG_PATH")"
if [ ! -f "$CODEX_CONFIG_PATH" ]; then
    touch "$CODEX_CONFIG_PATH"
fi

# Backup before editing
cp "$CODEX_CONFIG_PATH" "$CODEX_CONFIG_PATH.bak-$(date +%Y%m%d-%H%M%S)"

# Step 1: Ensure tool_output_token_limit = 64000
if grep -Eq '^[[:space:]]*tool_output_token_limit[[:space:]]*=' "$CODEX_CONFIG_PATH"; then
    sed -i -E 's/^[[:space:]]*tool_output_token_limit[[:space:]]*=.*/tool_output_token_limit = 64000/' "$CODEX_CONFIG_PATH"
else
    printf "\ntool_output_token_limit = 64000\n" >> "$CODEX_CONFIG_PATH"
fi
echo "  + Set Codex tool_output_token_limit = 64000"

# Step 2: Enable codex_hooks feature
if grep -Eq '^[[:space:]]*\[features\][[:space:]]*$' "$CODEX_CONFIG_PATH"; then
    if grep -Eq '^[[:space:]]*codex_hooks[[:space:]]*=' "$CODEX_CONFIG_PATH"; then
        sed -i -E 's/^[[:space:]]*codex_hooks[[:space:]]*=.*/codex_hooks = true/' "$CODEX_CONFIG_PATH"
    else
        awk '
            BEGIN { inserted=0 }
            {
                print $0
                if (!inserted && $0 ~ /^[[:space:]]*\[features\][[:space:]]*$/) {
                    print "codex_hooks = true"
                    inserted=1
                }
            }
        ' "$CODEX_CONFIG_PATH" > "$CODEX_CONFIG_PATH.tmp" && mv "$CODEX_CONFIG_PATH.tmp" "$CODEX_CONFIG_PATH"
    fi
else
    printf "\n[features]\ncodex_hooks = true\n" >> "$CODEX_CONFIG_PATH"
fi
echo "  + Enabled Codex hooks feature flag"

# Step 3: Install/refresh managed SessionStart hook block
HOOK_START="# AGENT-MEMORY-CODEX-HOOK-START"
HOOK_END="# AGENT-MEMORY-CODEX-HOOK-END"
HOOK_COMMAND="bash \"$CODEX_HOOK_SCRIPT\""

# Remove existing managed block if present
if grep -Fq "$HOOK_START" "$CODEX_CONFIG_PATH"; then
    awk -v s="$HOOK_START" -v e="$HOOK_END" '
        $0 == s { skip=1; next }
        $0 == e { skip=0; next }
        !skip { print }
    ' "$CODEX_CONFIG_PATH" > "$CODEX_CONFIG_PATH.tmp" && mv "$CODEX_CONFIG_PATH.tmp" "$CODEX_CONFIG_PATH"
fi

cat >> "$CODEX_CONFIG_PATH" <<EOF

$HOOK_START
[[hooks.SessionStart]]
matcher = "startup|resume|clear"

[[hooks.SessionStart.hooks]]
type = "command"
command = '$HOOK_COMMAND'
timeout = 30
statusMessage = "Injecting memory recovery reminder"
$HOOK_END
EOF

echo "  + Installed Codex SessionStart hook (memory recovery reminder)"
echo ""
echo "Settings written to $CODEX_CONFIG_PATH"
echo "Restart Codex for hook/config changes to take effect."
