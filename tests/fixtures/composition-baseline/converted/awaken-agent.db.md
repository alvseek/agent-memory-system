> `<domain>` in the ops below is the agent you are acting as — the domain you passed to `awaken`, or the one `create-agent` made. With no awakening, `list_agents()` shows what exists; never guess one.

**A body read is a page, and a listing or a search is not a body.** Three shapes, and mixing them up is the one way to read partial context as whole:

- **`query`** answers *which records match*: metadata only (uuid, title, `content_summary`, tags, project, dates) plus **`blocks_total`** — how many timestamp groups that record's body holds. It never returns `content`.
- **`search`** answers *what matched*: the same metadata plus a plain-text **`snippet`** of the matching window, and no body under either name. Reaching a body from a hit is a deliberate `get(uuid)`.
- **`get(uuid)`** answers *what the record says*: as much of the body as fits under the content ceiling in one response — the whole of a small record, one **page** of a large one — or exactly one page when you pass `cursor`/`limit`. Every `get` response carries `blocks_returned` / `blocks_total` / `next_cursor`, so a non-null cursor is how you know a large record did not arrive whole.

A **timestamp group** is every sub-episode block in the record that shares one `###` H3 timestamp; a group is indivisible and counts as one, so `blocks_total: 5` means five distinct moments. Two rules follow, and only one of them is a continuation:

- **`next_cursor` non-null means more remains** — pass it straight back as `get(uuid, cursor=…)`, or with `limit=` to keep the page small. It names the *first group not returned*, so a block prepended in between cannot shift your place, and it is the only signal that answers "is there more?".
- **`blocks_returned` < `blocks_total` does *not* mean more remains.** A final page returns fewer than the whole record and is complete. Never continue on the count alone.

An unknown or malformed cursor, or a non-positive `limit`, is an error — never a quiet fall back to page one. Cursors are per record: pass the page's own `uuid` with its cursor. A record that is not an episode (identity, reasoning, emotional, knowledge, the profile, the RAS triggers) is one atomic block — `blocks_total: 1` — because it is not a rolling document. Nothing ever splits a sub-episode block, and no repair step exists: a retimestamped or deleted target makes the old cursor fail loudly rather than resume somewhere else.

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

**One call** — `awaken(domain)` (MCP tool) or `GET /api/awaken?agent_id=<domain>` (HTTP). It assembles and returns the agent's memory payload from Valaskjalf server-side, **project-blind**: no project is accepted or resolved, so `latest_episode` is the newest episode overall and the caller selects its own out of the index:

- `shared.reasoning` — whole fleet-shared reasoning records, read from the shared table rather than from any agent.
- `shared.knowledge_index` — metadata only: uuid, title, content_summary, tags, project and dates. Inspect this alongside the agent's knowledge_index and fetch relevant bodies with get(uuid). Never load every body during awakening. A null legacy summary or an empty index is valid; do not invent a body-derived fallback.
- `shared.ras` — the **universal RAS triggers** (fleet-wide): memory recovery after compaction, and copy-paste-don't-regenerate. Automatic trigger-to-action protocols, whole, alongside reasoning.
- `shared.user_profile` — who [USER-NAME] is (name, philosophy, agent vision), as a single whole record or `null`. Fleet memory too: it does not vary by agent. `null` means nobody has been asked yet, which is the first-run branch in Phase 1 — a record that exists with an empty value inside it is a deliberate blank and is **not** that case.
- `identity` + `reasoning` + `emotional` — this agent's own records, whole (layer ii). `identity` includes the agent's core knowledge and RAS triggers.
- `knowledge_index` + `episodic_index` — metadata-only indexes; bodies via `get(uuid)` on demand (layer iii). Each index entry carries its `project`; the index itself never counts groups, so a row does not say how large its body is. When that size matters before paying for the read, `query(record_type="episode")` returns a projection that does carry `blocks_total`. `search(text)` finds a record but returns only a `snippet`, never a body.
- `latest_episode` — **a page** of the newest episode **overall**, since no project is accepted or resolved: up to three timestamp groups, with `blocks_returned` / `blocks_total` / `next_cursor`. The returned record's own `project` tells you which project it belongs to, and its `uuid` is what continues the read. When the newest overall is not that project's, say so in the open-items report. A non-null `next_cursor` means the body continues; a count smaller than `blocks_total` with a null cursor means you already have all of it.

The 4-layer assembly is a single derived call.

> **Not covered by the payload — and no longer needs to be**: the **awakening instructions** (the Phase 1/Phase 2 protocol) are not a record and are not served, because they are a **component** inlined into this procedure at compile time — the process rides in the prompt, the data comes from `awaken`. That is the whole of what the payload leaves out; the user profile used to be listed here too, and is now a record like any other (`shared.user_profile`, above). See `docs/flows/awaken-db.md` in the memory-server repo.

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

Already in the `awaken` payload: `shared.user_profile` is the whole record, or `null`. `null` means no profile has ever been written for this user, which is Phase 1's first-run branch. A record that exists with an empty value inside it is **not** that case — that is a deliberate blank, and re-asking it turns a one-time courtesy into a nag.

### § persist-user-profile

`insert(scope="shared", record_type="user_profile", title="User Profile", content="<the profile markdown>")`. No `agent_id`: the profile has no owner, and `scope="shared"` forbids one. Write **one** record carrying all three values in the same bullet form the markdown backend uses — never one record per field, because presence is answered by a row count and three rows would admit partial states with no rule for resolving them.

### § recover-missing-foundations

The whole shared reasoning foundation and the metadata-only shared knowledge directory have different load contracts. An empty `shared.knowledge_index` is a valid empty directory, not a missing foundation. A missing/malformed field is a payload failure. Check reasoning separately before diagnosing:

- **Other layers also short or cut mid-record** → the payload was **truncated in transit** (the MCP tool-result cap), not empty at rest. The store is fine; the transport is not.
- **Only `shared.reasoning` unexpectedly empty** → the store has no active shared reasoning for this user (possibly an unseeded or wrong tenant). This is not an agent-scoping mistake. Do not treat an empty knowledge index as evidence of the same problem.

For **transport truncation**, recover the complete response per **§ oversized-memory-warning** before diagnosing the store. Only genuinely absent records need **server-side** recovery — seeding the records (importer / `insert`); there is nothing to create on this end. If the foundations remain unavailable, report the failure and STOP: do not fabricate them and do not continue on partial context (`c4e7a19f`).

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

Already present as `latest_episode` in the `awaken` payload — a **page** of the newest episode **overall**, since no project is accepted or resolved. Read the page as the bounded starting context it is: `blocks_returned` of `blocks_total` groups, plus the record's `uuid` and a `next_cursor`. A non-null cursor means the record continues; continue with `get(latest_episode.uuid, cursor=…)` only when this session actually needs the older sub-episodes, and remember that a final page returns fewer than `blocks_total` with a null cursor. A caller whose own project is not the newest one selects its entry out of `episodic_index` and loads **that** uuid the same way; the payload's own is the default, and the fallback when the index holds nothing for the project.

Do not report a page as "the episode". The open-items report should name the newest sub-episodes you actually read, and say a cursor remains when one does.

### § oversized-memory-warning

First call `awaken(domain)` once and return the full response for reading, without selecting fields, summarizing, slicing, or preemptively redirecting it to a file. Do not assume it will truncate before trying. If the client/platform explicitly reports truncation or says the result was saved to a file, read that saved result to recover all omitted context. Try one whole file read first; only after an observed read limit, recover the remainder using a method that preserves the full content, including long lines. Check the recovery output for further clipping and do not continue until all required context from the response is loaded. If recovery remains impossible, name the source and failure and stop the work that depends on it. Concrete evidence of omitted content, such as an omission notice or an incomplete record, also requires recovery; anticipated size alone does not.

Episodes no longer arrive as one unbounded body, so a truncated `latest_episode` is not the expected state and must not be explained away as "normal for a big episode": a page reports its own coverage, and a `next_cursor` is a fact rather than a truncation. The ceiling bounds one record's **content**, not the whole payload — the fixed layers, the indexes and the JSON envelope are whole and sit outside it — so a response can still exceed a client cap on those, and that is a separate finding to report, not something a cursor fixes.

### Resolving references to other procedures and templates

Everything served here is composed for Munnin, and the slash commands installed beside you are the **markdown** compilation of the same procedures — they would write files where this store holds records. So when a served procedure tells you to **execute, invoke or run** `/<name>`, do not invoke the slash command: call `read_procedure("<name>")` and follow what it returns, passing what the command would have taken (a domain, a mode) as `argument`. When one points at a file by relative path — a template (`resources/<stem>.md`) or a script (`scripts/<stem>.sh`) — call `read_resource("<stem>")`. This applies to instructions to *act*; prose that merely names a procedure needs no call. Unsure what is served — `list_procedures()` and `list_resources()`. If a named procedure is not served, say so rather than substituting another.

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
