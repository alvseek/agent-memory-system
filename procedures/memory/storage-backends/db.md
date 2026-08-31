# Storage Backend — DB (Valaskjalf via Munnin)

Concrete storage mechanics for the **DB-backed** world. Each `## [procedure]` section maps the procedure's `§ op`s onto the 8 generic Munnin data tools: `awaken` · `get` · `query` · `search` · `insert` · `edit` · `archive` · `soft_delete`. See the [seam contract](README.md).

> **Model**: an **agent** is an entity with a row of its own, and memory belongs to it. One uniform record per memory item (`user_id`/`agent_id`/`record_type`/`project`/`title`/`tags`/dates + `full_content`), where `agent_id` is always a real kebab domain the store checks against the agent table — there is no sentinel value. **Fleet-shared memory** (reasoning + knowledge that belongs to no agent) lives apart and is written with `scope="shared"`, which takes no `agent_id` at all. `user_id` is stamped server-side. The index is a **derived `SELECT`** (`query`), not a stored artifact — so there are no index-maintenance steps to perform. Episodes are stored **one record per episode** (a rolling body of newest-first `---`-separated H3 sub-episodes).

---

## update-episodic

### § stamp-date

**No action.** The server stamps `created_date` / `updated_date` on write. Use the block's H3 timestamp as authored; you do not shell out to `date`.

### § list-candidate-episodes

`query(agent_id="<domain>", record_type="episode", project="<project>")` → returns the derived index projection (uuid, title, tags, dates) for the agent's active episodes. Theme-match against `title`/`tags`. (Archived episodes are excluded by default — pass `include_archived=True` only to reach them.)

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

### § persist-store

No action. A write through the memory tools lands in the database as it happens, so there is nothing to push and no separate save step that could fail. Report the persistence outcome as already durable.

---

## core-instruction-control-files

### § load-agent-memory

**One call** — `awaken(domain)` (MCP tool) or `GET /api/awaken?agent_id=<domain>` (HTTP). It assembles and returns the agent's memory payload from Valaskjalf server-side:

- `shared.reasoning` + `shared.knowledge` — the fleet-shared always-load layer (layer i), read from the shared table rather than from any agent.
- `shared.user_profile` — who [USER-NAME] is (name, philosophy, agent vision), as a single whole record or `null`. Fleet memory too: it does not vary by agent. `null` means nobody has been asked yet, which is the first-run branch in Phase 1 — a record that exists with an empty value inside it is a deliberate blank and is **not** that case.
- `identity` + `reasoning` + `emotional` — this agent's own records, whole (layer ii). `identity` includes the agent's core knowledge and RAS triggers.
- `knowledge_index` + `episodic_index` — metadata-only indexes; bodies via `get(uuid)` / `search(text)` on demand (layer iii).
- `latest_episode` — the newest episode's full body.

No file reads, no parallel Reads — the 4-layer assembly is a single derived call.

> **Not covered by the payload — and no longer needs to be**: the **awakening instructions** (the Phase 1/Phase 2 protocol) are not a record and are not served, because they are a **component** inlined into this procedure at compile time — the process rides in the prompt, the data comes from `awaken`. That is the whole of what the payload leaves out; the user profile used to be listed here too, and is now a record like any other (`shared.user_profile`, above). See `docs/flows/awaken-db.md` in the memory-server repo.

### § recover-missing-foundations

The shared foundations are the fleet-shared records (`shared.reasoning` + `shared.knowledge`) that `awaken` returns, and a store holding none returns them as **empty fields on a 200** rather than failing — so nothing raises an error, and this check is all that stands between a hollow awakening and continuing as if the foundations were there. Diagnose before acting:

- **Other layers also short or cut mid-record** → the payload was **truncated in transit** (the MCP tool-result cap), not empty at rest. The store is fine; the transport is not.
- **Only `shared.reasoning` / `shared.knowledge` empty** → the store genuinely holds no fleet-shared records for this user (importer never run, or the wrong tenant). This is **not** an agent-scoping mistake: fleet memory has no `agent_id` to get wrong.

Recovery is **server-side** — seed the records (importer / `insert`); there is nothing to create on this end. Report which of the two it is and STOP: do not fabricate the foundations and do not continue on partial context (`c4e7a19f`).

### § load-user-profile

Already in the `awaken` payload: `shared.user_profile` is the whole record, or `null`. `null` means no profile has ever been written for this user, which is Phase 1's first-run branch. A record that exists with an empty value inside it is **not** that case — that is a deliberate blank, and re-asking it turns a one-time courtesy into a nag.

### § persist-user-profile

`insert(scope="shared", record_type="user_profile", title="User Profile", content="<the profile markdown>")`. No `agent_id`: the profile has no owner, and `scope="shared"` forbids one. Write **one** record carrying all three values in the same bullet form the markdown backend uses — never one record per field, because presence is answered by a row count and three rows would admit partial states with no rule for resolving them.

### § load-latest-episode

Already present as `latest_episode` in the `awaken` payload — no extra call. Use `get(uuid)` only when loading a *different* episode than the newest.

### § oversized-memory-warning

The truncation risk here is the **whole `awaken` payload** measured against the MCP tool-result cap, and exceeding it truncates **silently** — no error is raised. If any layer looks cut off mid-record, say so explicitly and treat it as a load failure (`c4e7a19f`). `/archive-old-memories` reduces the store, but narrowing what is requested is the more direct fix.

### Resolving references to other procedures and templates

Everything served here is composed for Munnin, and the slash commands installed beside you are the **markdown** compilation of the same procedures — they would write files where this store holds records. So when a served procedure tells you to **execute, invoke or run** `/<name>`, do not invoke the slash command: call `read_procedure("<name>")` and follow what it returns, passing what the command would have taken (a domain, a mode) as `argument`. When one points at a template by relative path (`resources/<stem>.md`), call `read_resource("<stem>")`. This applies to instructions to *act*; prose that merely names a procedure needs no call. Unsure what is served — `list_procedures()` and `list_resources()`. If a named procedure is not served, say so rather than substituting another.

---

## list-agents

> Both ops are answered by a **single** `list_agents()` call. Every other read here is agent-scoped — you name a domain and get its records — so enumeration needed a primitive of its own, and that primitive assembles the roster server-side rather than handing back rows to join. Discovery and identity arrive together, which is why there is one call below and not two.

### § list-agent-domains

`list_agents()`. Returns one entry per agent — `agent_id`, `name`, `role` — sorted by domain. An agent appears because it **has a row**, not because memory happens to mention it, so a newly created agent with no memory yet is listed from the moment it exists, and an agent whose every record is archived or tombstoned is still listed. Archiving and deleting retire a memory *item*; no operation retires an agent.

### § read-agent-identity

**Already answered** — the `name` and `role` fields come back on each entry from **§ list-agent-domains**, read straight off the agent's own columns (they are parsed once, at import, not on every call). Do not call `awaken(domain)` per agent to fill them in: `awaken` returns that agent's whole always-load payload including the fleet-shared layers, so a roster built that way costs the entire store and overruns the client's output cap.

An agent with no readable identity returns `name` and `role` as `null`. Keep it in the roster with role `(no identity recorded)` — that state is a finding worth seeing, not a row to drop.

---

## create-agent

> Creation here is genuinely two steps, and the order is enforced by the store rather than by convention: an agent is a **row**, and every memory record names an owner the store checks against it. So `create_agent` comes first and `insert` cannot run before it. There is still no directory to make — but there is now something to create, which is the difference between this backend and the one it replaced, where an agent existed only as a side effect of having records.

### § check-agent-exists

`list_agents()` and look for the domain. This reads the agent table directly, so it answers about the *entity* rather than about whether any memory happens to mention it — which also means it correctly reports an agent that exists but has written nothing yet.

You may skip the lookup and let **§ create-agent-store** fail instead: creation refuses a domain that is taken, so the check is a courtesy that gives a clearer message, never the thing keeping the store consistent.

### § generate-uuid

**No shell command.** The agent's UUID is *content* — its digital soul, carried in the identity body and stored on the agent row's `uuid` column. Generate any UUID for it; a memory record's own storage `uuid` is a separate identifier and not a substitute.

### § create-agent-store

`create_agent(agent_id="<domain>", name="<name>", role="<role>", uuid="<the generated UUID>")`.

This is the agent coming into being — the row its memory will point at. It **refuses a domain that already exists** rather than refreshing it, so re-running creation over a live agent raises instead of silently rewriting that agent's name. Nothing else needs seeding: the five record types (`identity` · `reasoning` · `emotional` · `knowledge` · `episode`) are the whole skeleton, each created on first write.

### § persist-identity

With the agent created, insert **three** `identity` records, mirroring the three sections the markdown template ships:

- `insert(agent_id="<domain>", record_type="identity", title="Agent Identity", content="<name, role, main purpose, the three responsibilities, created date, UUID>")`
- `insert(agent_id="<domain>", record_type="identity", title="Core Domain Knowledge", content="<empty — the agent grows this through use>")`
- `insert(agent_id="<domain>", record_type="identity", title="Domain RAS", content="<empty — triggers are added as they emerge>")`

Three records, not one: `awaken` returns `identity` as the agent's whole always-load private layer, and keeping the split means a DB-born agent and a markdown-born agent wake up with the same shape.

If any of these is refused with a foreign-key error, **§ create-agent-store** did not run or did not succeed — fix that rather than retrying the insert.

Fleet-shared memory needs nothing: it belongs to no agent, lives in its own table, and every agent already reads it through `awaken`.

### § initialize-index

**No action.** The episodic and knowledge indexes are derived `SELECT`s over the agent's records; an agent with no episodes simply returns empty ones. There is no index file to seed.

### § verify-agent

`awaken("<domain>")` and confirm the payload comes back with: three `identity` items, the UUID present and matching 8-4-4-4-12 in the identity body, empty `episodic_index` / `knowledge_index` (correct for a new agent), and the fleet-shared layers populated — an empty `shared` here means the store's foundations are missing, which is a fleet-level problem and not this agent's.

Also confirm the domain now appears in `list_agents()` with its `name` and `role`, which is the entity half and the half `awaken` cannot report on.

If `awaken` returns nothing for the domain, the inserts did not land. Report that rather than retrying blindly — the agent row will already exist, so a blind retry now fails at **§ create-agent-store** instead of at the step that actually went wrong.
