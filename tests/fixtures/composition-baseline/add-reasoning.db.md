# Add Reasoning Memory Protocol

Capture anti-patterns and decision-making approaches as **lean, memorable** reasoning entries. *How* the store is read/written is delegated to the active **storage backend**.

## Arguments

`$ARGUMENTS`

- `/add-reasoning [context]` → Document the reasoning pattern described in context
- `/add-reasoning` → Will ask for context

If no arguments provided, ask: "What reasoning pattern or anti-pattern should I document?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below to prevent context loss and ensure complete execution*

### Step 1: Read the Reasoning Store

Read the agent's current reasoning memory so the new pattern fits alongside the existing ones and doesn't duplicate one (**§ read-reasoning-store**).

### Step 2: Draft from the Template

Read the reasoning-pattern template (**§ template**) and draft the entry using its fixed structure.

### Step 3: Check the Entry

Check every required field against the template. For a new entry, generate its UUID (**§ generate-uuid**); for a rewrite, preserve the existing UUID. Keep the instructions, anchor, and example distinct, and check that the Final Conclusion stands on its own.

### Step 4: Persist

Persist the completed pattern into the reasoning store (**§ persist-reasoning**).

---

> `<domain>` in the ops below is the agent you are acting as — the domain you passed to `awaken`, or the one `create-agent` made. With no awakening, `list_agents()` shows what exists; never guess one.

**A body read is a page, and a listing or a search is not a body.** Three shapes, and mixing them up is the one way to read partial context as whole:

- **`query`** answers *which records match*: metadata only (uuid, title, `content_summary`, tags, project, dates) plus **`blocks_total`** — how many timestamp groups that record's body holds. It never returns `content`.
- **`search`** answers *what matched*: the same metadata plus a plain-text **`snippet`** of the matching window, and no body under either name. Reaching a body from a hit is a deliberate `get(uuid)`.
- **`get(uuid)`** answers *what the record says*: as much of the body as fits under the content ceiling in one response — the whole of a small record, one **page** of a large one — or exactly one page when you pass `cursor`/`limit`. Every `get` response carries `blocks_returned` / `blocks_total` / `next_cursor`, so a non-null cursor is how you know a large record did not arrive whole.

A **timestamp group** is every sub-episode block in the record that shares one `###` H3 timestamp; a group is indivisible and counts as one, so `blocks_total: 5` means five distinct moments. Two rules follow, and only one of them is a continuation:

- **`next_cursor` non-null means more remains** — pass it straight back as `get(uuid, cursor=…)`, or with `limit=` to keep the page small. It names the *first group not returned*, so a block prepended in between cannot shift your place, and it is the only signal that answers "is there more?".
- **`blocks_returned` < `blocks_total` does *not* mean more remains.** A final page returns fewer than the whole record and is complete. Never continue on the count alone.

An unknown or malformed cursor, or a non-positive `limit`, is an error — never a quiet fall back to page one. Cursors are per record: pass the page's own `uuid` with its cursor. A record that is not an episode (identity, reasoning, emotional, knowledge, the profile, the RAS triggers) is one atomic block — `blocks_total: 1` — because it is not a rolling document. Nothing ever splits a sub-episode block, and no repair step exists: a retimestamped or deleted target makes the old cursor fail loudly rather than resume somewhere else.

### § read-reasoning-store

`query(agent_id="<domain>", record_type="reasoning")` to see the existing patterns (or reuse the set already returned by `awaken`).

### § generate-uuid

The pattern's cited UUID is content — generate any UUID for it; the `insert` response also returns the record's own `uuid` if you prefer to cite that.

### § persist-reasoning

`insert(agent_id="<domain>", record_type="reasoning", title="<short memorable title>", content="<full pattern block>", template_version="<the template's current stamp>")`. Read `reasoning-pattern-template` from resources first and declare its `template_version` — a missing or stale version is refused.

### § template

**Served as an MCP Resource** (`reasoning-pattern-template`) — read it from resources.

---
