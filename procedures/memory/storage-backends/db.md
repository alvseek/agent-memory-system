# Storage Backend — DB (Valaskjalf via Munnin)

Concrete storage mechanics for the **DB-backed** world. Each `## [procedure]` section maps the procedure's `§ op`s onto the 8 generic Munnin data tools: `awaken` · `get` · `query` · `search` · `insert` · `edit` · `archive` · `soft_delete`. See the [seam contract](README.md).

> **Model**: one uniform record per memory item (`user_id`/`agent_id`/`record_type`/`project`/`title`/`tags`/dates + `full_content`). `user_id` is stamped server-side. The index is a **derived `SELECT`** (`query`), never a hand-edited file — so index-maintenance steps in the markdown backend become **no-ops** here. `agent_id` = a kebab domain or the reserved `__shared__`. Episodes are stored **one record per episode file** (a rolling body of newest-first `---`-separated H3 sub-episodes).

---

## update-episodic

### § stamp-date

**No action.** The server stamps `created_date` / `updated_date` on write. Use the block's H3 timestamp as authored; you do not shell out to `date`.

### § list-candidate-episodes

`query(agent_id="<domain>", record_type="episode", project="<project>")` → returns the derived index projection (uuid, title, tags, dates) for the agent's active episodes. Theme-match against `title`/`tags` exactly as the markdown flow matches filename/summary. (Archived episodes are excluded by default — pass `include_archived=True` only to reach them.)

### § append-sub-episode

An episode is a single record whose body is the rolling, newest-first sub-episode list. To append newest-first:
1. `get(uuid)` the matched episode to read its current body.
2. `edit(uuid, old_string="<the current top of the body>", new_string="<new H3 block>\n\n---\n\n<the current top of the body>")` — prepends the new block above the previous newest, preserving the `---` separator (Edit-tool parity: `old_string` must uniquely match the body's opening).

The index reflects the change automatically (derived `SELECT`) — **no manual index maintenance**.

### § create-episode

`insert(agent_id="<domain>", record_type="episode", project="<project>", title="<project-theme>", tags=[…], content="<first sub-episode block>")`. The record is assembled and `uuid`-stamped server-side and appears in the index projection immediately — **no file scaffold, no index entry to add**.

### § housekeeping

**No-op.** Records are not line-bounded files: there is no 1000-line split (a large body is fine; shortening is a later curation *policy*, not a write mechanic) and no filename migration (records are keyed by `uuid`, not filenames).

### § template

**No file.** The sub-episode-block template is served as an MCP **Resource** (`episodic-entry-template`) — read it from resources, not a path. (There is no separate file-scaffold template: `§ create-episode` is an `insert`, not a `cp`.)

---

## add-reasoning

### § read-reasoning-store

`query(agent_id="<domain>", record_type="reasoning")` to see the existing patterns (or reuse the set already returned by `awaken`).

### § generate-uuid

**No shell command.** The pattern's cited UUID is content — generate any UUID for it; the `insert` response also returns the record's own `uuid` if you prefer to cite that.

### § persist-reasoning

`insert(agent_id="<domain>", record_type="reasoning", title="<short memorable title>", content="<full pattern block>")`.

### § template

**No file.** The reasoning-pattern template is served as an MCP **Resource** (`reasoning-pattern-template`) — read it from resources, not a path.

---

## update-emotional

### § stamp-date

**No action.** The server stamps `created_date` on write; use the block's own timestamp as authored.

### § persist-emotional

`insert(agent_id="<domain>", record_type="emotional", title="<moment title>", content="<moment block>")`. **Newest-first is a read concern** — the index projection orders by date, so there is no manual top-insert.

### § template

**No file.** The emotional-moment template is served as an MCP **Resource** (`emotional-moment-template`) — read it from resources, not a path.

---

## update-knowledge

### § persist-knowledge

`insert(agent_id="<domain>", record_type="knowledge", title="<knowledge area>", tags=[…], content="<knowledge doc>")`. General/central knowledge only — Munnin is project-blind (no project-scoped knowledge).

### § update-knowledge-index

**No-op.** The knowledge directory is a derived `query(record_type="knowledge")` — nothing to hand-edit.

### § template

**No file.** The knowledge-file template is served as an MCP **Resource** (`knowledge-file-template`) — read it from resources, not a path.

---

## load-episodic

### § list-episodes

`query(agent_id="<domain>", record_type="episode")` → the derived index projection (uuid, title, summary/tags, date), newest-first.

### § load-episode-body

`get(uuid)` for the selected episode(s); or `search(text)` to match a keyword across bodies.

---

## load-knowledge

### § list-knowledge

`query(agent_id="<domain>", record_type="knowledge")` → the derived knowledge directory (general/central only; project-scoped knowledge is the overlay's).

### § load-knowledge-body

`get(uuid)` for the selected entry/entries; or `search(text)` for a keyword.

---

## archive-old-memories

### § stamp-date

**No action** (server-stamped).

### § archive-episodes

`archive(uuid)` per episode past the cutoff — sets `archived_date`, drops it from the hot index, body retained + still `search`-able. **No file moves, no index edits.**

### § archive-emotional-apply

Per tier: **Tier 1 (keep)** — no-op. **Tier 3 (archive full)** — `archive(uuid)` (full body retained, cold, `search`-able). **Tier 2 (shorten + archive)** — `edit(uuid, <full>, <stub>)` to shrink the awaken payload.

> **Tier collapse note**: in the DB, `archive(uuid)` already keeps the full body *cold-but-searchable*, so the markdown Tier-2 vs Tier-3 split partly dissolves (the hot-index removal is exactly what `archive` does). Tier-2's extra nicety — a short echo staying *active* — maps to keeping the record active and `edit`-ing it to the stub (the full is recoverable from the import source). A dedicated archived-full-plus-active-stub pair is a future curation policy, not a v1 primitive.

---

## update-memory

### § detect-mode-scan

`query(agent_id="<domain>", record_type="episode")` → theme-match against title/summary/tags.

### § scan-promotion-markers

The records you wrote this session ARE the promotions — list the reasoning / knowledge / emotional records inserted since session start (track the `uuid`s your `insert` calls returned, or `query` by recency). Project context is the overlay's (project-keyed records), not Munnin's.

---

## wrap-up

### § read-newest-episode

`query(agent_id="<domain>", record_type="episode")` → newest; `get(uuid)` its body; read the top sub-episode block for `Tech Debts` + `Next Steps`.

---

## awaken-agent

### § load-agent-memory

**One call** — `awaken(domain)` (MCP tool) or `GET /api/awaken?agent_id=<domain>` (HTTP). It assembles and returns the agent's memory payload from Valaskjalf server-side:

- `shared.reasoning` + `shared.knowledge` — the `__shared__` always-load layer (layer i).
- `identity` + `reasoning` + `emotional` — this agent's own records, whole (layer ii). `identity` includes the agent's core knowledge and RAS triggers.
- `knowledge_index` + `episodic_index` — metadata-only indexes; bodies via `get(uuid)` / `search(text)` on demand (layer iii).
- `latest_episode` — the newest episode's full body.

No file reads, no parallel Reads — the 4-layer assembly is a single derived call.

> **⚠ Not covered by the payload (step-2 gap)**: the **awakening instructions** (`core-instruction-control-files.md` — the Phase 1/Phase 2 protocol referenced in Step 2) and the **user profile** are NOT part of `awaken`'s payload. They are not yet stored as records or served. Until that is resolved, a pure-DB client must obtain the Phase 1/2 process another way (e.g. this prompt's own text, or global context); the user profile reaches the agent via the global instructions file. See `docs/flows/awaken-db.md`.

---

## list-agents

> **⚠ Deferred — not yet implementable on the DB backend.** Listing agents means enumerating *distinct* `agent_id`s across the store, but the 8 generic data tools are all **agent-scoped** (`query(agent_id=…)`, `get(uuid)`, …) — there is no "list distinct agents" primitive yet. These ops are specified here for seam parity and will be filled in when Munnin gains an agent-enumeration capability. Until then the DB face does not serve `list-agents` (it is not registered as a Prompt).

### § list-agent-domains

**Deferred.** Will map to a Munnin agent-enumeration call (e.g. a `SELECT DISTINCT agent_id` projection exposed as a data tool), returning each `agent_id` and excluding the reserved `__shared__` sentinel. Not available in the current 8-tool surface.

### § read-agent-identity

**Deferred.** Once enumeration exists, map to `awaken(domain)` (or a `get`/`query` on the agent's identity record) to read the agent's Name + Role from its `identity` layer server-side — no file read.
