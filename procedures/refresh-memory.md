# Refresh Memory

Recover agent memory after context compaction. Use as fallback when auto-recovery doesn't trigger.

## Arguments

`$ARGUMENTS`

- `/refresh-memory [domain]` → Refresh memory for the specified domain agent (e.g., meta, backend-nestjs, frontend-react)

If no arguments provided and agent identity is already known (e.g., from awakening earlier in the session), use the current domain automatically. Only ask "Which agent domain should I refresh memory for?" if the domain is truly unknown.

---

## Procedure

### Step 1: Stop and Pause

STOP doing anything else. Memory recovery takes priority.

### Step 2: Resolve Agent Memory Path

**Parameter**: [AGENT-MEMORY-PATH] (set per OS below)
- **Windows**: `C:\Users\[LOCAL-USER-NAME]\.claude\@agent-memory\`
- **Linux/macOS**: `/home/[LOCAL-USER-NAME]/.claude/@agent-memory/`

### Step 3: Read Core Files

Read these 5 files:
- `[AGENT-MEMORY-PATH]/control-files/core-instruction-control-files.md` (Shared foundations + awakening instructions)
- `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-core-memory.md` (Agent-specific identity)
- `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-memory-index.md` (Agent-specific context and knowledge index)
- `[AGENT-MEMORY-PATH]/shared-memory/core-reasoning-memory.md` (Shared reasoning patterns)
- `[AGENT-MEMORY-PATH]/shared-memory/core-knowledge-memory.md` (Shared knowledge fundamentals)

### Step 4: Reread Global Instructions

Reread the global instructions file (`[GLOBAL-INSTRUCTIONS-FILE]`).

### Step 5: Continue

Resume what was being done before compaction. Ask [USER-NAME] for clarification if anything is unclear — do NOT continue silently on assumptions.

---
