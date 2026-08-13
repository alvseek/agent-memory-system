# Awaken Agent

Load agent memory and activate a domain-specific agent. *Where* the memory is loaded from is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)).

## Arguments

`$ARGUMENTS`

- `/awaken-agent [domain]` → Awaken the specified domain agent (e.g., meta, backend-nestjs, frontend-react)

If no arguments provided, ask: "Which agent domain should I awaken?"

---

## Procedure

### Step 1: Load the Awakening Set

Load the agent's full awakening set into **your own context** (**§ load-agent-memory**) — five layers:

1. **Shared foundations + awakening instructions** — the shared reasoning/knowledge foundations and the phased awakening protocol.
2. **Agent identity** — this domain's identity, core knowledge, and RAS triggers.
3. **Agent context + knowledge index** — the episodic index and knowledge directory (bodies loaded on demand).
4. **Shared reasoning patterns.**
5. **Shared knowledge fundamentals.**

🚨 **CRITICAL — load into YOUR OWN context, do NOT delegate to a sub-agent** (Agent tool / general-purpose / Explore). Sub-agents return summaries; awakening needs the full content in your own context window. A delegated load produces a hollow awakening with diluted identity and missing reasoning patterns.

### Step 2: Follow Awakening Instructions

Follow the phased protocol from the loaded awakening instructions (`core-instruction-control-files.md`) — Phase 1 (Process Loaded Identity), then Phase 2 (Load Project Context & Report).

---

## Storage Mechanics

The operation referenced above — **§ load-agent-memory** — is defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## awaken-agent`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## awaken-agent`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.
