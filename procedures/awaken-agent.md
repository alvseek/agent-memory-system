# Awaken Agent

Load agent memory and activate a domain-specific agent.

## Arguments

`$ARGUMENTS`

- `/awaken-agent [domain]` → Awaken the specified domain agent (e.g., meta, backend-nestjs, frontend-react)

If no arguments provided, ask: "Which agent domain should I awaken?"

---

## Procedure

### Step 1: Resolve Agent Memory Path

**Parameter**: [AGENT-MEMORY-PATH] (set per OS below)
- **Windows**: `C:\Users\[LOCAL-USER-NAME]\.claude\@agent-memory\`
- **Linux/macOS**: `/home/[LOCAL-USER-NAME]/.claude/@agent-memory/`

### Step 2: Read Agent Memory Files

Read these 5 files:
- `[AGENT-MEMORY-PATH]/control-files/core-instruction-control-files.md` (Shared foundations + awakening instructions)
- `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-core-memory.md` (Agent-specific identity)
- `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-memory-index.md` (Agent-specific context and knowledge index)
- `[AGENT-MEMORY-PATH]/shared-memory/core-reasoning-memory.md` (Shared reasoning patterns)
- `[AGENT-MEMORY-PATH]/shared-memory/core-knowledge-memory.md` (Shared knowledge fundamentals)

### Step 3: Follow Awakening Instructions

Follow the "Awakening Instructions for Agent [DOMAIN]" phases described in core-instruction-control-files.md.

---
