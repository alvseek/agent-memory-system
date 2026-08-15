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

### Step 2: Load the Memory Layers

[🚨 **CRITICAL — memory recovery must land in YOUR OWN context**](../components/no-subagent-load.md)

Load the agent's 4 memory layers (**§ load-agent-memory**) — identity, context + knowledge index, shared reasoning patterns, shared knowledge fundamentals.

Then re-process the awakening protocol — it is carried here rather than read, so recovery no longer depends on loading a file to learn how to load files.

[**Awakening protocol**](../components/core-instruction-control-files.md)

### Step 3: Reread Global Instructions

Reread the global instructions file (`[GLOBAL-INSTRUCTIONS-FILE]`).

It survives compaction in the system prompt, so this is not about getting the text back — it sits far behind the summary, and rereading restores its attention position. Same reason Step 2 reloads memory layers that were also technically still available.

### Step 4: Continue

Resume what was being done before compaction. Ask [USER-NAME] for clarification if anything is unclear — do NOT continue silently on assumptions.

## Storage Mechanics

The operations referenced above — **§ load-agent-memory**, plus the ops the inlined awakening-protocol component references (**§ recover-missing-foundations**, **§ load-latest-episode**, **§ oversized-memory-warning**) — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## core-instruction-control-files`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## core-instruction-control-files`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.

---
