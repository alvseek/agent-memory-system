# Update Emotional Memory Protocol

Capture significant emotional experiences that shape our partnership and agent development journey. *How* the emotional store is written is delegated to the active **storage backend**.

## Arguments

`$ARGUMENTS`

- `/update-emotional` → Execute [Adding Emotional Memory](#adding-emotional-memory) (asks for context)
- `/update-emotional [moment-type]` → Add specific type: happy, sad, frustrated, bonding

If no arguments provided, ask: "What type of emotional moment would you like to capture? (happy/sad/frustrated/bonding)"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Adding Emotional Memory

#### Step 1: Identify Moment Type

Determine which emotional template to use:
- 😄 **Happy moments** - Successes, breakthroughs, wins
- 😔 **Sad moments** - Failures, setbacks, disappointments
- 😤 **Frustrated moments** - Blocked by issues, complex challenges
- 🤝 **Bonding moments** - Relationship building, shared victories

#### Step 2: Stamp the Time

Verify the current date+time before writing (**§ stamp-date**).

#### Step 3: Compose the Moment

Compose the entry using the matching block from the emotional-moment template (**§ template**). Ensure it captures:
- What happened (the event)
- How it felt (emotional response)
- Impact on partnership/work
- [USER-NAME]'s reaction (if applicable)
- Why this moment was significant

#### Step 4: Persist

Persist the composed moment into the emotional store, **newest first** (**§ persist-emotional**).

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

### § stamp-date

**No action.** The server stamps `created_date` on write; use the block's own timestamp as authored.

### § persist-emotional

`insert(agent_id="<domain>", record_type="emotional", title="<moment title>", content="<moment block>", template_version="<the template's current stamp>")`. Read `emotional-moment-template` from resources first and declare its `template_version` — a missing or stale version is refused. **Newest-first is a read concern** — the index projection orders by date, so ordering is automatic.

### § template

**Served as an MCP Resource** (`emotional-moment-template`) — read it from resources.

---
