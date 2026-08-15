# Awaken Agent

Load agent memory and activate a domain-specific agent. *Where* the memory is loaded from is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)).

## Arguments

`$ARGUMENTS`

- `/awaken-agent [domain]` → Awaken the specified domain agent (e.g., meta, backend-nestjs, frontend-react)

If no arguments provided, ask: "Which agent domain should I awaken?"

---

## Procedure

### Step 1: Load the Awakening Set

Load the agent's full awakening set into **your own context** (**§ load-agent-memory**) — four layers:

1. **Agent identity** — this domain's identity, core knowledge, and RAS triggers.
2. **Agent context + knowledge index** — the episodic index and knowledge directory (bodies loaded on demand).
3. **Shared reasoning patterns.**
4. **Shared knowledge fundamentals.**

*(The awakening protocol itself is not one of them — it is carried by Step 2 below.)*

[🚨 **CRITICAL — load the awakening set into YOUR OWN context**](components/no-subagent-load.md)

### Step 2: Follow Awakening Instructions

Follow the phased protocol below — Phase 1 (Process Loaded Identity), then Phase 2 (Load Central Context & Report).

[**Awakening protocol**](components/core-instruction-control-files.md)

---

## Storage Mechanics

The operations referenced above — **§ load-agent-memory**, plus the ops the inlined awakening-protocol component references (**§ recover-missing-foundations**, **§ load-latest-episode**, **§ oversized-memory-warning**) — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## core-instruction-control-files`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## core-instruction-control-files`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.
