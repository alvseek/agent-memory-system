# Update Knowledge Memory Protocol

Capture domain expertise, technical patterns, research findings, and best practices that enhance agent capabilities. *How* the knowledge store + index are written is delegated to the active **storage backend**.

## Arguments

`$ARGUMENTS`

- `/update-knowledge [context]` → Document the knowledge described in context
- `/update-knowledge` → Will ask for context

If no arguments provided, ask: "What knowledge or domain expertise should I document?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: Evaluate Capture Criteria

**Capture when:**
- Domain expertise discoveries (new frameworks, libraries, patterns)
- Technical patterns (architectural solutions, design patterns)
- Research findings (comparative analysis, benchmarks, evaluations)
- Best practices with evidence (proven approaches backed by data)
- Specialized knowledge enhancing capabilities (tooling, methodologies)

**Don't capture:**
- Temporary workarounds or project-specific hacks
- Unverified claims or assumptions
- Context already covered in existing knowledge files
- Information that should be in episodic memory instead

> **Scope**: `/update-knowledge` writes **general** knowledge (research, core-domain, cross-cutting) — cross-project, always **central**. Project-specific context (VM access, deploy procedures, conventions) + project-scoped knowledge are handled by the coding overlay, not here.

### Step 2: Compose from the Template

Compose the entry using the knowledge-file template (**§ template**).

**Quality Standards:**
- Back claims with sources, documentation, or proven experience
- Include links to official documentation when available
- Reference specific examples or case studies
- Distinguish between proven practices and experimental approaches

### Step 3: Persist

Persist the composed entry into the knowledge store (**§ persist-knowledge**).

### Step 4: Register in the Knowledge Index

Add an entry to the knowledge directory for discoverability (**§ update-knowledge-index**). Consider whether new knowledge should be core vs. specialized.

**Cross-Reference Standards:**
- Use markdown links for all file references: `[Pattern Name](file.md)`
- Include context in link text: `[Database Migration Strategy](migrations.md#strategy)`
- Test links to ensure they work properly

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

### § persist-knowledge

`insert(agent_id="<domain>", record_type="knowledge", title="<knowledge area>", tags=[…], content="<knowledge doc>", content_summary="<the entry's Summary row>", template_version="<the template's current stamp>")`. Read `knowledge-file-template` from resources first and declare its `template_version` — a missing or stale version is refused. `content_summary` is required for a knowledge record: pass the entry's `**Summary**` row verbatim, because that one line is what the knowledge index lists the record by. General/central knowledge only — Munnin is project-blind (no project-scoped knowledge).

### § update-knowledge-index

**No-op.** The knowledge directory is a derived `query(record_type="knowledge")` — it reflects every insert automatically.

### § template

**Served as an MCP Resource** (`knowledge-file-template`) — read it from resources.

---
