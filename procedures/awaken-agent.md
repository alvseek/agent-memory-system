# Awaken Agent

Load agent memory and activate a domain-specific agent.

## Arguments

`$ARGUMENTS`

- `/awaken-agent [domain]` → Awaken the specified domain agent (e.g., meta, backend-nestjs, frontend-react)

If no arguments provided, ask: "Which agent domain should I awaken?"

---

## Procedure

### Step 1: Load the 5 Core Files

🚨 **CRITICAL**: Use the **Read tool directly** — DO NOT delegate to a sub-agent (Agent tool / general-purpose / Explore). Sub-agents return summaries; awakening needs the full content of these files in YOUR own context window. Reading via sub-agent produces a hollow awakening with diluted identity and missing reasoning patterns.

Read all 5 in parallel:
- `[AGENT-MEMORY-PATH]/control-files/core-instruction-control-files.md` (Shared foundations + awakening instructions)
- `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-core-memory.md` (Agent-specific identity)
- `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-memory-index.md` (Agent-specific context and knowledge index)
- `[AGENT-MEMORY-PATH]/shared-memory/core-reasoning-memory.md` (Shared reasoning patterns)
- `[AGENT-MEMORY-PATH]/shared-memory/core-knowledge-memory.md` (Shared knowledge fundamentals)

### Step 2: Follow Awakening Instructions

Follow the phased protocol in the loaded `core-instruction-control-files.md` — Phase 1 (Process Loaded Identity), then Phase 2 (Load Project Context & Report).

---
