#!/bin/bash
# delegate-agent.sh — Background agent-to-agent delegation
# Usage: ./delegate-agent.sh <Name|UUID> "<prompt>" [fleet-map-path]
#
# Name → Full 5-file awakening + prompt (new session, background)
# UUID → Resume existing session + prompt (background)
#
# Returns: UUID of the target session (stdout), agent works in background.

set -euo pipefail
source "$(dirname "$0")/fleet-common.sh"

# --- Usage ---
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <Name|UUID> \"<prompt>\" [fleet-map-path]"
    echo ""
    echo "  Name  → Awakens agent with full 5-file protocol + sends prompt (background)"
    echo "  UUID  → Resumes existing session + sends prompt (background)"
    echo ""
    echo "  Returns the UUID so the caller can check status later."
    echo ""
    echo "Examples:"
    echo "  $0 \"Backend Django\" \"Implement user auth middleware per the spec...\""
    echo "  $0 \"3f8a2b1c-...\" \"Continue with the next step\""
    exit 1
fi

TARGET="$1"
PROMPT="$2"
FLEET_MAP=$(resolve_fleet_map "${3:-}")

if is_uuid "$TARGET"; then
    # --- UUID mode: Resume in background ---
    echo -e "${CYAN}[delegate-agent] Resuming session in background: ${TARGET}${NC}" >&2
    claude --print --resume "$TARGET" "$PROMPT" &
    echo "$TARGET"
else
    # --- Name mode: Awaken new session in background ---
    verify_agent_exists "$TARGET"
    UUID=$(generate_uuid)

    echo -e "${CYAN}[delegate-agent] Awakening ${TARGET} in background (UUID: ${UUID})${NC}" >&2

    FULL_PROMPT=$(build_awaken_prompt "$TARGET" "$PROMPT" "work on this delegated task autonomously. When finished, summarize what you did and what deliverables were produced:")
    TASK_THEME=$(echo "$PROMPT" | head -c 60 | tr '\n' ' ')

    add_fleet_entry "$FLEET_MAP" "$TARGET" "$UUID" "$TASK_THEME"
    echo -e "${GREEN}[delegate-agent] Registered in fleet map${NC}" >&2

    claude --print --session-id "$UUID" "$FULL_PROMPT" &
    echo "$UUID"
fi
