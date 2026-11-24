> `<domain>` in the ops below is the agent you are acting as — the domain you passed to `awaken`, or the one `create-agent` made. With no awakening, `list_agents()` shows what exists; never guess one.

**A body read is a page, and a listing or a search is not a body.** Three shapes, and mixing them up is the one way to read partial context as whole:

- **`query`** answers *which records match*: metadata only (uuid, title, `content_summary`, tags, project, dates) plus **`blocks_total`** — how many timestamp groups that record's body holds. It never returns `content`.
- **`search`** answers *what matched*: the same metadata plus a plain-text **`snippet`** of the matching window, and no body under either name. Reaching a body from a hit is a deliberate `get(uuid)`.
- **`get(uuid)`** answers *what the record says*: as much of the body as fits under the content ceiling in one response — the whole of a small record, one **page** of a large one — or exactly one page when you pass `cursor`/`limit`. Every `get` response carries `blocks_returned` / `blocks_total` / `next_cursor`, so a non-null cursor is how you know a large record did not arrive whole.

A **timestamp group** is every sub-episode block in the record that shares one `###` H3 timestamp; a group is indivisible and counts as one, so `blocks_total: 5` means five distinct moments. Two rules follow, and only one of them is a continuation:

- **`next_cursor` non-null means more remains** — pass it straight back as `get(uuid, cursor=…)`, or with `limit=` to keep the page small. It names the *first group not returned*, so a block prepended in between cannot shift your place, and it is the only signal that answers "is there more?".
- **`blocks_returned` < `blocks_total` does *not* mean more remains.** A final page returns fewer than the whole record and is complete. Never continue on the count alone.

An unknown or malformed cursor, or a non-positive `limit`, is an error — never a quiet fall back to page one. Cursors are per record: pass the page's own `uuid` with its cursor. A record that is not an episode (identity, reasoning, emotional, knowledge, the profile, the RAS triggers) is one atomic block — `blocks_total: 1` — because it is not a rolling document. Nothing ever splits a sub-episode block, and no repair step exists: a retimestamped or deleted target makes the old cursor fail loudly rather than resume somewhere else.

# Wrap Up Session

End-of-session **memory** orchestrator: update memory → persist the store → report. Capturing a session and saving it are one job here rather than two — the procedure writes the memory layers and then commits whatever the active storage backend needs committing, so a session never ends with its own record written but unsaved.

What it does not touch is the working project: no project push, no orientation map. Those belong to a coding/environment add-on, which composes a fuller project wrap-up on top of this one.

**Delta-aware**: re-running `/wrap-up` after more work auto-scopes evaluations to the delta (theme match → cutoff = prior sub-episode timestamp). `/wrap-up fresh` forces full-session re-eval.

**Execution style**: silent. Run the steps silently — tool calls stay visible, but no prose narration. Produce ONE report block at the final step as the only user-facing output.

## Arguments

`$ARGUMENTS` = `[all|agent] [fresh]`

- **Mode** (optional): `agent` (default) persists only this agent's own memory, leaving a concurrently-running agent's in-flight work untouched; `all` persists the whole store. The default is the conservative one because `/wrap-up` runs at session end, when nobody is watching what else in the store happens to be dirty.
- **`fresh`** (optional): force fresh mode for the memory update (pass-through to `/update-memory`); default auto-detects delta vs fresh.
- Examples: `/wrap-up` (agent + delta) · `/wrap-up all` · `/wrap-up fresh` · `/wrap-up all fresh`.

---

## Procedure

**Resolve args first**: `<mode>` = `all` if `$ARGUMENTS` contains the token `all`, else `agent` (the default). Pass `fresh` through to the memory update if present.

### Step 1: Save Memory (silent)

Execute `/update-memory`. Pass `fresh` through if present. Capture as data for the report: mode, gate decisions, episodic entry, carry-forward count, promotions, emotional status — and the **`Tech Debts` + `Next Steps`** it hands up from the sub-episode just written (see `/update-episodic`'s `## Returns`). Do NOT print `/update-memory`'s own Phase 4 summary separately — it folds into the final report.

> The open items arrive with the write instead of being read back out of the store afterwards. The agent that composed that block is the one being asked, so there is no second read to go stale.

### Step 2: Persist the Store (silent)

Save what Step 1 just wrote (**§ persist-store**). What that costs depends on the backend — a git-backed store needs a commit and a push, a database-backed one is already durable the moment the write lands — so this step reports an **outcome** rather than assuming an operation happened.

Capture that outcome for Step 3: whether everything in scope is committed AND pushed (per repo, where the backend has repos), plus any failure reason.

### § persist-store

No action. A write through the memory tools lands in the database as it happens, so there is nothing to push and no separate save step that could fail. Report the persistence outcome as already durable.

### Step 3: Wrap-Up Report (only visible output)

**Completion gate** (UUID a1b2c3d4): report completion only when Step 2 confirms this session's memory is persisted. Apply the selected backend's persistence and failure rules below.

**On success**, print this block:

```
Wrap-up complete (mode: [agent / all] · [fresh / delta from CUTOFF]):

Memory update:
- Phase 1 — Promoted artifacts: project context: [updated/created — file / skipped] / reasoning: [added — pattern name / skipped] / knowledge: [added — entry name / skipped]
- Phase 2 — Session captured: [appended to / created] [name] ([timestamp]) — [brief theme]; carry-forward: [N items / N/A]; promotions: [N markers / none]
- Phase 3 — Feeling captured: emotional [captured — polarity + clearest criterion / skipped — brief reason]

Memory persisted:
- ✅ nothing to push — the write was already saved

📋 Open items going forward:

Tech debts:
- [item 1]
(or "None declared")

Next steps:
- [item 1]
(or "None declared")
```

If both Tech Debts and Next Steps are empty → replace both lists with *"No open items declared from this session."*


---

> **Working in a repo as well?** This wrap-up saves memory and nothing else. If a coding/environment add-on is installed, use its fuller project wrap-up instead — it pushes the project's work first so a merge request can open without waiting, runs this memory update, refreshes the orientation map, and gates on both pushes together.
