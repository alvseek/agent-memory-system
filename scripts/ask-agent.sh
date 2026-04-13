#!/bin/bash
# ask-agent.sh — Blocking agent-to-agent communication
# Usage: ./ask-agent.sh <Name|UUID> "<prompt>" [fleet-map-path]
#
# Name → Full 5-file awakening + prompt (new session, registered in fleet map)
# UUID → Resume existing session + prompt (continuation)
#
# Returns: Agent's response (stdout), blocks until complete.

set -euo pipefail
source "$(dirname "$0")/fleet-common.sh"

# --- Usage ---
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <Name|UUID> \"<prompt>\" [fleet-map-path]"
    echo ""
    echo "  Name  → Awakens agent with full 5-file protocol + sends prompt (blocking)"
    echo "  UUID  → Resumes existing session + sends prompt (blocking)"
    echo ""
    echo "Examples:"
    echo "  $0 \"Backend Django\" \"What is the best model pattern for user auth?\""
    echo "  $0 \"3f8a2b1c-9d4e-4f7a-8e2b-5c6d9a1b4e7f\" \"Status update?\""
    exit 1
fi

TARGET="$1"
PROMPT="$2"
FLEET_MAP=$(resolve_fleet_map "${3:-}")

if is_uuid "$TARGET"; then
    # --- UUID mode: Resume existing session ---
    echo -e "${CYAN}[ask-agent] Resuming session: ${TARGET}${NC}" >&2
    claude --print --resume "$TARGET" "$PROMPT"
else
    # --- Name mode: Awaken new session ---
    verify_agent_exists "$TARGET"
    UUID=$(generate_uuid)

    echo -e "${CYAN}[ask-agent] Awakening ${TARGET} (UUID: ${UUID})${NC}" >&2

    FULL_PROMPT=$(build_awaken_prompt "$TARGET" "$PROMPT" "respond to this request:")
    TASK_THEME=$(echo "$PROMPT" | head -c 60 | tr '\n' ' ')

    add_fleet_entry "$FLEET_MAP" "$TARGET" "$UUID" "$TASK_THEME"
    echo -e "${GREEN}[ask-agent] Registered in fleet map${NC}" >&2

    claude --print --session-id "$UUID" "$FULL_PROMPT"
fi
