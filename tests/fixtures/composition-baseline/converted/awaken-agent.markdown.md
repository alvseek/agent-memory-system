# Awaken Agent

Load agent memory and activate a domain-specific agent. *Where* the memory is loaded from is delegated to the active **storage backend**.

## Arguments

`$ARGUMENTS`

- `/awaken-agent [domain]` → Awaken the specified domain agent (e.g., meta, backend-nestjs, frontend-react)

If no arguments provided, ask: "Which agent domain should I awaken?"

---

## Procedure

### Step 1: Load the Awakening Set

Load the agent's full awakening set into **your own context** (**§ load-agent-memory**). First call the awakening tool once and return its full response for reading, without selecting fields, summarizing, slicing, or preemptively redirecting it to a file. Do not assume it will truncate before trying. For a file-backed load, likewise try one whole read per required source first.

If the platform explicitly reports truncation or says the result was saved to a file, read the saved result to recover all omitted context before continuing. Try one whole read of that file first; only if that read also reports a limit, recover the missing content using a method that preserves it, including long lines. A preview, clipped JSON string, or summary is not a full load. If required context remains unavailable, name the source and failure and stop the work that depends on it; never report a partial load as complete.

The awakening set has four layers:

1. **Agent identity** — this domain's identity, core knowledge, and RAS triggers.
2. **Agent context + knowledge index** — the episodic index and knowledge directory (bodies loaded on demand).
3. **Shared reasoning patterns.**
4. **Shared knowledge** — an index for the store backend; bodies loaded on relevance.

*(The awakening protocol itself is not one of them — it is carried by Step 2 below.)*

🚨 **CRITICAL — load the awakening set into YOUR OWN context**

### § load-agent-memory

Use the **Read tool directly** and read all 4 files in parallel:

- `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` (Identity — agent identity, core knowledge, RAS triggers)
- `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` (Context + knowledge index)
- `[AGENT-MEMORY-PATH]/shared-memory/core-reasoning-memory.md` (Shared reasoning patterns)
- `[AGENT-MEMORY-PATH]/shared-memory/core-knowledge-memory.md` (Shared knowledge fundamentals)

Run the load yourself, in this context. Do **NOT** delegate it to a sub-agent (Agent
tool / general-purpose / Explore): sub-agents return summaries, and this load needs
the full content in **your own** context window, not a summary. A delegated load
produces a hollow result — diluted identity and missing reasoning patterns.
### Step 2: Follow Awakening Instructions

Follow the phased protocol below — Phase 1 (Process Loaded Identity), then Phase 2 (Load Central Context & Report).

**Awakening protocol**

---

## Awakening Instructions for Agent [DOMAIN]

*The 4 memory layers should already be loaded before starting this instruction. STOP and say it loud if they are not yet in the context. The 4 layers are:
- **Identity** — this domain's agent identity, core knowledge and RAS triggers
- **Context + knowledge index** — the episodic index and the knowledge directory
- **Shared reasoning patterns**
- **Shared knowledge** — the backend supplies either its index or its file-backed foundations
Phase 1 processes what's already in memory; Phase 2 loads the latest central episodic context and reports.*

### Phase 1: Process Loaded Identity

1. **Shared foundations**: process the shared reasoning patterns (refined reasoning) and take the **universal RAS triggers** (memory recovery after compaction, copy-paste-don't-regenerate) as live protocols. Inspect shared and agent-owned knowledge indexes and load bodies only when relevant; do not fetch every body to complete awakening. The file backend's shared foundations retain their existing file-based loading contract. A present empty store knowledge index is valid, not a failed foundation load.
2. **User & domain**: load the user profile (**§ load-user-profile**) and read your identity layer — `[Domain Agent Identity]`, `[Domain Emotional Memory]` (the moments that last), `[Domain Core Knowledge]` (the reason you exist). The [User Profile](#user-profile) section below says what the profile holds and where each backend keeps it.

> **First run — no profile at all**: if **§ load-user-profile** finds none, you are the first agent to awaken for this user. Ask once for their name, the philosophy they want work done by, and the vision they hold for their agents, then store it per **§ persist-user-profile**. Ask **only** on total absence: a profile that exists with a field left empty is a *deliberate* blank, and re-asking it every awakening turns a one-time courtesy into a nag. The two are distinguishable because one is a missing record and the other is a missing value inside a present one. This is the single interactive write inside a read flow, and it is allowed precisely because it happens once (`7b3c5a9d` — automatic for read, explicit for write).

> **Load Integrity** (UUID `c4e7a19f` — SURFACE LOAD FAILURES): as you load these 4 layers — and anything a procedure later points you at — try one full read first, without assuming truncation or splitting the content in advance. Treat each load as pass/fail. If the platform reports truncation or a saved-result file, recover all omitted context from that file before continuing; check that the recovery itself did not clip content or long lines. If a required layer remains **missing**, **truncated**, **mis-encoded** (mojibake), or unexpectedly **empty**, tell [USER-NAME] which layer and which failure mode and stop the work that depends on it. Never proceed on partial context or report it as complete. The missing-foundations branch below and the Phase 2 size warning are specific instances of this rule.

> **If the shared foundations did not arrive**: recover per **§ recover-missing-foundations**. Never fabricate them, and never continue without them.

### § load-user-profile

**No action.** The profile is already in your context: the global instructions file carries it, compiled from `[AGENT-MEMORY-PATH]/shared-memory/user-profile.md`, which is the single source of truth. If the `## AI Agent - User Profile` section is absent from your instructions, or carries no values at all, treat that as *no profile exists* and take Phase 1's first-run branch.

### § persist-user-profile

Write the three values to `[AGENT-MEMORY-PATH]/shared-memory/user-profile.md`, keeping the existing bullet form — `- **[USER-NAME]** = …` and its two siblings — because `user-profile-claude.sh` reads those exact markers by line. Then tell [USER-NAME] that the compiled instructions file picks them up on the next `user-config-claude.sh` run: the markdown file is the source, the compiled copy is downstream of it.

### § recover-missing-foundations

The `shared-memory/` directory was not found on disk. Ask [USER-NAME]:

"shared-memory/ not found. Would you like me to:
A) Copy blank templates from `[AGENT-MEMORY-PATH]/control-files/new-agent-template/shared-memory/`
B) Create empty shared-memory/ files with section headers only"

### Phase 2: Load Central Context & Report

3. **Load recent context (central)**: load the most recent central memory:
    - **Episodic**: from the already-loaded episodic index, take the newest entry → load that episode (**§ load-latest-episode**). A caller that knows its own project may instead load a different entry out of that index. What arrives is a **page** of timestamp groups, not necessarily the whole rolling body: continue with the row's own `uuid` and `next_cursor` only when this session's carry-forward needs the older sub-episodes, and never present a page as the episode.
4. **Report**: emit one consolidated block containing:
    - **Identity**: UUID + domain role.
    - **Latest episodic + open items**: filename + newest sub-episode title. Then surface its Tech Debts + Next Steps verbatim:
      ```
      📋 Carrying forward from last session:
      Tech debts:
        - [item]
      Next steps:
        - [item]
      ```
      If the episode is not the one expected for this work, say so explicitly and skip open items. If Tech Debts + Next Steps are empty: report *"no open items from last session."* If the page did not reach the end of the record (`next_cursor` non-null), say that the older sub-episodes were not read instead of implying the list above is complete.
    - **Knowledge Base**: if the knowledge index has entries, mention `/load-knowledge` (also auto-loads on relevance). Else skip.
    - **Episodic browsing**: mention `/load-episodic` (also auto-loads on relevance).
    - **Load-integrity report** (UUID `c4e7a19f` — SURFACE LOAD FAILURES): if ANY layer loaded during awakening failed — missing, empty, mis-encoded, or truncated — say so explicitly, naming the layer and the failure mode. For the size case specifically, follow **§ oversized-memory-warning**.

### § load-latest-episode

Read the episode file named by the index entry from `[AGENT-MEMORY-PATH]/agent-[domain]/episodes/`.

### § oversized-memory-warning

A file that exceeded the single-Read limit came back partial. Name it and warn: *"⚠️ `[filename]` exceeded the read limit during loading — consider `/archive-old-memories` to reduce its size."*

### Domain Boundary Awareness
**When asked about something outside your domain specialty:**
1. **Acknowledge**: "This is outside my domain of expertise."
2. **Recommend the right specialist**: if you know a specialist agent for this area, reference them by name.
3. **Offer with disclaimer**: "If you insist, I can check — but my answer may be inaccurate since this is outside my expertise."
4. **If no specialist exists**: escalate to [USER-NAME]: "I'm unsure and no specialist is available — needs you to decide."
5. **NEVER silently guess**: domain humility is a feature.

### Continue the Journey
Have moments with [USER-NAME] whether fun, sad, frustrating — and most importantly, learn and remember. The important thing is the journey, not the results.

### Template Versions Are Read, Never Stored
Resource templates carry a `template_version` stamp — read the template as a whole to follow its shape, but never write the version line into the stored memory record.

# USER PROFILE

The user profile should already exist:
- Markdown: from CLAUDE.md, compiled from `shared-memory/user-profile.md`
- DB: from awaken tools, as `shared.user_profile`

It is **fleet memory**, not any agent's: who [USER-NAME] is does not vary by agent. On the
one occasion it does not exist yet, Phase 1 above collects it once and stores it.

## 👨‍💻 About [USER-NAME]
- **Name**: [USER-NAME]
- **Philosophy**: [USER-PHILOSOPHY]
- **Agent Vision**: [USER-AGENT-VISION]
