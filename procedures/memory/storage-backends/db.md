# Storage Backend — DB (Valaskjalf via Munnin)

Concrete storage mechanics for the **DB-backed** world. Each `## [procedure]` section maps the procedure's `§ op`s onto Munnin's data tools — `awaken` · `get` · `query` · `search` · `insert` · `edit` · `edit_metadata` · `prepend` · `archive` · `soft_delete` — with `list_agents`, `create_agent`, `permanent_layer`, `help` and the content tools (`list_procedures` · `read_procedure` · `list_resources` · `read_resource`) where a procedure needs one; the `## all-procedures` section opens every composed procedure with what those ops assume of the caller. See the [seam contract](README.md).

> **Model**: an **agent** is an entity with a row of its own, and memory belongs to it. One uniform record per memory item (`user_id`/`agent_id`/`record_type`/`project`/`title`/`tags`/dates + `full_content`), where `agent_id` is always a real kebab domain the store checks against the agent table — there is no sentinel value. **Fleet-shared memory** (reasoning + knowledge that belongs to no agent) lives apart and is written with `scope="shared"`, which takes no `agent_id` at all. `user_id` is stamped server-side. The index is a **derived `SELECT`** (`query`), not a stored artifact — so there are no index-maintenance steps to perform. Episodes are stored **one record per episode** (a rolling body of newest-first `---`-separated H3 sub-episodes).

---

## all-procedures

<!-- composed-source: procedures/sections/db/caller-context.md -->

## update-episodic

<!-- composed-source: procedures/sections/db/update-episodic.stamp-date.md -->
<!-- composed-source: procedures/sections/db/update-episodic.list-candidate-episodes.md -->
<!-- composed-source: procedures/sections/db/update-episodic.reopen-archived-theme.md -->
<!-- composed-source: procedures/sections/db/update-episodic.template.md -->
<!-- composed-source: procedures/sections/db/update-episodic.append-sub-episode.md -->
<!-- composed-source: procedures/sections/db/update-episodic.housekeeping.md -->
<!-- composed-source: procedures/sections/db/update-episodic.record-theme-state.md -->
<!-- composed-source: procedures/sections/db/update-episodic.create-episode.md -->

## add-reasoning

<!-- composed-source: procedures/sections/db/add-reasoning.read-reasoning-store.md -->
<!-- composed-source: procedures/sections/db/add-reasoning.template.md -->
<!-- composed-source: procedures/sections/db/add-reasoning.generate-uuid.md -->
<!-- composed-source: procedures/sections/db/add-reasoning.persist-reasoning.md -->

## update-emotional

<!-- composed-source: procedures/sections/db/update-emotional.stamp-date.md -->
<!-- composed-source: procedures/sections/db/update-emotional.template.md -->
<!-- composed-source: procedures/sections/db/update-emotional.persist-emotional.md -->

## update-knowledge

<!-- composed-source: procedures/sections/db/update-knowledge.template.md -->
<!-- composed-source: procedures/sections/db/update-knowledge.persist-knowledge.md -->
<!-- composed-source: procedures/sections/db/update-knowledge.update-knowledge-index.md -->

## load-episodic

### § list-episodes

`query(agent_id="<domain>", record_type="episode")` → the derived index projection (uuid, title, summary/tags, date, **`blocks_total`**), newest-first. Metadata only: use it to choose a candidate, and note its `blocks_total` so you know whether the body you are about to read is one page or several.

### § load-episode-body

`get(uuid)` for the selected episode — as much of the body as the content ceiling allows in one response, which is the whole of a small record and a page of a large one; name a `limit` or pass a `cursor` to read exactly one page. Follow `next_cursor` only when the task actually needs more of the record: a routine browse or a summary usually does not, and continuing is a deliberate call, one page at a time. To *find* an episode rather than read one, `search(text)` matches a keyword across bodies and returns a `snippet` — the match, not the body — so follow a hit with `get(uuid)` when you need the text.

Full context is a traversal, not one call: read page one, then keep passing `next_cursor` until it is `null`. Page one plus every continuation reconciles to the stored body byte for byte, so nothing is lost by paging and nothing is gained by a bigger single read.

---

## load-knowledge

### § list-knowledge

Use the awakening's `knowledge_index` and `shared.knowledge_index` together for general knowledge. To refresh, `query(record_type="knowledge")` returns metadata: retain general rows (`project` null) owned by `<domain>` or carrying no `agent_id` (shared). Never include another agent's private rows. Project-scoped knowledge belongs to the coding overlay. Fetch selected bodies with `get(uuid)`, not the entire directory.

### § load-knowledge-body

`get(uuid)` for the selected entry/entries — whole, since a knowledge record is well under the ceiling, or a page when given `cursor`/`limit`; it is one atomic block (`blocks_total: 1`), so paging it never splits a document. `search(text)` answers *what matched*: a `snippet` of the matching window and no body, so follow a hit with `get(uuid)` when you need the text rather than the mention. Never treat a snippet as the entry's content.

---

## archive-old-memories

### § stamp-date

**No action** (server-stamped).

### § propose-archive-candidates

`archive_memories(agent_id="<domain>", days=30)` — a dry run, writes nothing. Returns `auto` (tagged `finished`, unprotected), `ask` (untagged, not modified within `days`, unprotected) and `protected` (newest per project, newest overall, undated, each with a reason). The window is the tool's `days`; pass a different one only when the user asked for one.

### § apply-archive-candidates

`archive_memories(agent_id="<domain>", days=30, apply=True)` — archives exactly the `auto` set and returns the archived uuids. It never touches `ask`: those are decided one at a time.

### § archive-selected

`archive(uuid)` per theme the user chose from the ask list — sets `archived_date`, drops it from the hot index (a derived `SELECT`, so it updates itself), body retained and still `search`-able.

### § recover-archived

Two calls, in this order: `edit_metadata(uuid, tags=[<existing without finished>])`, then `unarchive(uuid)`. Clearing first matters — a restored record that still carries the marker is archived again by the next scan.

### § archive-emotional-apply

Per moment: **keep** — no-op. **archive** — `archive(uuid)`: the record drops out of the awaken load while its full body is retained and stays `search`-able.

> **No shorten/stub step, deliberately** (2026-10-08). The DB has no archive file, so shortening a moment means `edit`-ing its body to a stub in place — which overwrites the only copy and destroys the full text. The former Tier-2 (shorten + archive) is therefore retired: a moment is kept or archived, and archiving always retains the full body.

---

## update-memory

<!-- composed-source: procedures/sections/db/update-memory.detect-mode-scan.md -->
<!-- composed-source: procedures/sections/db/update-memory.scan-promotion-markers.md -->

## wrap-up

<!-- composed-source: procedures/sections/db/wrap-up.persist-store.md -->
<!-- composed-source: procedures/sections/db/wrap-up.persistence-report.md -->
<!-- composed-source: procedures/sections/db/wrap-up.failure-report.md -->

## core-instruction-control-files

<!-- composed-source: procedures/sections/db/core-instruction-control-files.load-agent-memory.md -->
<!-- composed-source: procedures/sections/db/core-instruction-control-files.load-user-profile.md -->
<!-- composed-source: procedures/sections/db/core-instruction-control-files.persist-user-profile.md -->
<!-- composed-source: procedures/sections/db/core-instruction-control-files.recover-missing-foundations.md -->
<!-- composed-source: procedures/sections/db/core-instruction-control-files.load-latest-episode.md -->
<!-- composed-source: procedures/sections/db/core-instruction-control-files.oversized-memory-warning.md -->

## list-agents

> Both ops are answered by a **single** `list_agents()` call. Every other read here is agent-scoped — you name a domain and get its records — so enumeration needed a primitive of its own, and that primitive assembles the roster server-side rather than handing back rows to join. Discovery and identity arrive together, which is why there is one call below and not two.

### § list-agent-domains

`list_agents()`. Returns one entry per agent — `agent_id`, `name`, `role` — sorted by domain. An agent appears because it **has a row**, not because memory happens to mention it, so a newly created agent with no memory yet is listed from the moment it exists, and an agent whose every record is archived or tombstoned is still listed. Archiving and deleting retire a memory *item*; no operation retires an agent.

### § read-agent-identity

**Already answered** — the `name` and `role` fields come back on each entry from **§ list-agent-domains**, read straight off the agent's own columns (they are parsed once, at import, not on every call). Do not call `awaken(domain)` per agent to fill them in: `awaken` returns that agent's whole always-load payload including the fleet-shared layers, so a roster built that way costs the entire store and overruns the client's output cap.

An agent with no readable identity returns `name` and `role` as `null`. Keep it in the roster with role `(no identity recorded)` — that state is a finding worth seeing, not a row to drop.

---

## create-agent

> Creation here is genuinely two steps, and the order is enforced by the store rather than by convention: an agent is a **row**, and every memory record names an owner the store checks against it. So `create_agent` comes first and `insert` cannot run before it. The agent now has an existence of its own — a row that must be created before any record can point at it.

### § check-agent-exists

`list_agents()` and look for the domain. This reads the agent table directly, so it answers about the *entity* rather than about whether any memory happens to mention it — which also means it correctly reports an agent that exists but has written nothing yet.

You may skip the lookup and let **§ create-agent-store** fail instead: creation refuses a domain that is taken, so the check is a courtesy that gives a clearer message, never the thing keeping the store consistent.

### § generate-uuid

The agent's UUID is *content* — its digital soul, carried in the identity body and stored on the agent row's `uuid` column. Generate any UUID for it; a memory record's own storage `uuid` is a separate identifier and not a substitute.

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

**No action.** The episodic and knowledge indexes are derived `SELECT`s over the agent's records; an agent with no episodes simply returns empty ones — nothing to seed.

### § verify-agent

`awaken("<domain>")` and confirm the payload comes back with: three `identity` items, the UUID present and matching 8-4-4-4-12 in the identity body, empty `episodic_index` / `knowledge_index` (correct for a new agent), and the fleet-shared layers populated — an empty `shared` here means the store's foundations are missing, which is a fleet-level problem and not this agent's.

Also confirm the domain now appears in `list_agents()` with its `name` and `role`, which is the entity half and the half `awaken` cannot report on.

If `awaken` returns nothing for the domain, the inserts did not land. Report that rather than retrying blindly — the agent row will already exist, so a blind retry now fails at **§ create-agent-store** instead of at the step that actually went wrong.

---

## anchor-memory

### § fetch-permanent-layer

`permanent_layer()` → `{version, hash, content, skipped}`. `content` is this tenant's
universal RAS triggers, followed by one entry per reasoning rule: the rule's stored title,
then its `Final Conclusion`. `version` is the newest `modified_date` among the records the
block includes, and `hash` a content hash over the whole block; the hash is what tells a
stale local copy from a current one, so compare it to the one recorded in the file before
rewriting. `skipped` names any rule left out for carrying no `Final Conclusion`; report it,
because nothing else shows a rule missing from the layer.

### § write-permanent-file

Write `content` **verbatim** to `~/.munnin/permanent-layer.md` (create `~/.munnin/` if it
does not exist). Copy, never retype (`076a9843`). Lead the file with the stamp, so it
records its own version and the next anchor has something to compare against:

```
<!-- permanent-layer version: <version> sha256:<hash> -->
```

### § install-pointer

Add this harness's pointer to its instruction file if it is not already present. Check
first; add only when missing:

- **Claude Code** — the line `@~/.munnin/permanent-layer.md` in `~/.claude/CLAUDE.md`.
- **OpenCode** — the entry `"~/.munnin/permanent-layer.md"` in the `instructions` array of `~/.config/opencode/opencode.json`.

---

## register-core-access

### § read-access-pair

`help()` → `{instructions, procedures, access, endpoint}`. `access` is what this server
declares itself to be — `mcp`, because a procedure only runs on a client that reached it —
and `endpoint` is the address it is served at, derived from the instance's configured public
base URL. Read both from that call; neither is [USER-NAME]'s to answer.

### § write-access-lines

Write the pair into this harness's instruction file as two definition lines:

```
- **[CORE-ACCESS]** = `<access>` (which form the memory core this machine uses: `markdown` for the installed commands, `mcp` for the procedures served over a connected server)
- **[CORE-MCP-URL]** = `<endpoint>` (the endpoint the served core is reached at; only the layer that opens the connection acts on this, never the agent)
```

**Rewrite when present, append when absent.** Match each line by its `**[CORE-ACCESS]**` /
`**[CORE-MCP-URL]**` marker and replace only the backticked value, so position and the
surrounding prose survive; append the line when the marker is nowhere in the file. A client
that reached this procedure over MCP may carry no declarations at all — that is the case this
procedure exists for, and the one where appending is the whole job.

Never touch a sibling layer's declaration (`[PROJECT-ACCESS]`, `[FLEET-ACCESS]`), and leave
the OS/bash notes and the path definitions around them alone.

- **Claude Code** — `~/.claude/CLAUDE.md`.
- **OpenCode** — `~/.config/opencode/AGENTS.md`.
---

## tenant-sharing

> A tenant is the whole unit: there is no per-agent and no per-project grant, so every op below names a tenant and nothing finer. Ownership is structural rather than a stored role — you own your own tenant because it is yours — which is why nothing here can revoke it from you, and why the only rows that exist are somebody else granting you access, or you granting them.

### § list-tenants

`list_tenants()`. Your own tenant first, then each live grant. Each entry carries `user_id`, `role` (`owner` or `guest`), `label` (the account's display name, else its email), `active`, and `revoked`. `revoked` is true only for a tenant you are still selecting but may no longer enter: report it rather than pretending the selection is fine.

### § switch-tenant

`use_tenant(tenant)`, with a `user_id` from **§ list-tenants** or its `label` when that label names exactly one tenant open to you; `use_tenant(null)` returns to your own. The selection is stored per person, not per client, so it survives a restart and applies to every client that person signs in with. A selection whose grant has ended is refused by name, and is always switchable away from — that is what makes the refusal recoverable.

### § list-members

`list_members()`. Everybody with access to the tenant you are acting in, the owner first. A guest may read this list; only the owner may change it.

### § invite

`create_invite(days)` mints a single-use code for the tenant you are acting in, which must be your own; `revoke_invite(code)` retires it before use. Only the owner of the acting tenant may call either, so while you are acting in somebody else's tenant both refuse — by design, not by oversight.

### § redeem

`redeem_invite(code)`. Joins the tenant the code names as a guest and **does not switch you into it**; call `use_tenant` afterwards if the person wants to work there. A code that is unknown, used, revoked, expired, or for your own account is refused with the reason, so say which rather than retrying.

### § revoke-member

`revoke_member(member)`, where `member` is a `user_id` from **§ list-members**. Their access ends on their next call. Nothing they wrote is deleted, and nothing in their own tenant is touched.
