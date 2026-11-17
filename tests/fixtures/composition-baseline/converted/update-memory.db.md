> `<domain>` in the ops below is the agent you are acting as — the domain you passed to `awaken`, or the one `create-agent` made. With no awakening, `list_agents()` shows what exists; never guess one.

**A body read is a page, and a listing or a search is not a body.** Three shapes, and mixing them up is the one way to read partial context as whole:

- **`query`** answers *which records match*: metadata only (uuid, title, `content_summary`, tags, project, dates) plus **`blocks_total`** — how many timestamp groups that record's body holds. It never returns `content`.
- **`search`** answers *what matched*: the same metadata plus a plain-text **`snippet`** of the matching window, and no body under either name. Reaching a body from a hit is a deliberate `get(uuid)`.
- **`get(uuid)`** answers *what the record says*: as much of the body as fits under the content ceiling in one response — the whole of a small record, one **page** of a large one — or exactly one page when you pass `cursor`/`limit`. Every `get` response carries `blocks_returned` / `blocks_total` / `next_cursor`, so a non-null cursor is how you know a large record did not arrive whole.

A **timestamp group** is every sub-episode block in the record that shares one `###` H3 timestamp; a group is indivisible and counts as one, so `blocks_total: 5` means five distinct moments. Two rules follow, and only one of them is a continuation:

- **`next_cursor` non-null means more remains** — pass it straight back as `get(uuid, cursor=…)`, or with `limit=` to keep the page small. It names the *first group not returned*, so a block prepended in between cannot shift your place, and it is the only signal that answers "is there more?".
- **`blocks_returned` < `blocks_total` does *not* mean more remains.** A final page returns fewer than the whole record and is complete. Never continue on the count alone.

An unknown or malformed cursor, or a non-positive `limit`, is an error — never a quiet fall back to page one. Cursors are per record: pass the page's own `uuid` with its cursor. A record that is not an episode (identity, reasoning, emotional, knowledge, the profile, the RAS triggers) is one atomic block — `blocks_total: 1` — because it is not a rolling document. Nothing ever splits a sub-episode block, and no repair step exists: a retimestamped or deleted target makes the old cursor fail loudly rather than resume somewhere else.

# Update Memory Protocol

Comprehensive memory update orchestrator. Five phases:

- **Phase 0** — Detect delta vs fresh mode (theme match)
- **Phase 1** — Two gated auto-evals (reasoning / knowledge)
- **Phase 2** — Pre-scan promotion markers + episodic capture
- **Phase 3** — Emotional 5-criteria gate (deep-emotion anchoring, polarity-neutral)
- **Phase 4** — Report

`/update-episodic` writes only the episodic layer. `/update-memory` is the full end-of-session orchestrator (what `/wrap-up` invokes). *Storage-specific reads/scans are delegated to the active backend; the gates below are storage-agnostic.*

**Execution style**: silent. Run Phases 0-3 silently — tool calls stay visible, but no prose narration of phases. Produce only the Phase 4 Step 6 summary block. (When invoked by `/wrap-up`, even that is folded into the caller's summary.)

## Arguments

`$ARGUMENTS`

- `/update-memory` → Default (auto-detect mode)
- `/update-memory fresh` → Force fresh mode (full-session re-eval)
- `/update-memory new` → Force new episodic file (combinable: `/update-memory fresh new`)

---

## Phase 0 — Detect Mode

### Step 0: Detect Mode + Cutoff

1. If `$ARGUMENTS` contains `fresh` → `MODE = fresh`, skip to Phase 1.
2. Theme-match scan: list active episodes (**§ detect-mode-scan**). Find the top candidate where the name or summary contains the current project name + highest keyword overlap with the session theme.
3. **No match** → `MODE = fresh` (new episode created in Phase 2). **Match** → `MODE = delta`, `CUTOFF = top sub-episode timestamp`.
4. Capture `MODE` and `CUTOFF` (if delta) for the Phase 4 summary.

---

### § detect-mode-scan

`query(agent_id="<domain>", record_type="episode")` → theme-match against title/summary/tags.

## Phase 1 — Promote Durable Artifacts

> **Delta-mode scope rule**: when `MODE = delta`, each gate's checklist applies ONLY to work after `CUTOFF`. Pre-cutoff work was evaluated at the prior wrap-up.

### Step 1: Reasoning Pattern Gate

- [USER-NAME] explicit anti-pattern callout? Signals: *"we got burned"*, *"don't do X again"*, *"remember this anti-pattern"*
- [USER-NAME] explicit pattern validation? Signals: *"always do it this way"*, *"this is the right pattern"*, *"let's encode this"*
- New decision-framework emerged from back-and-forth that both agreed should govern future similar situations?

**YES to any** → execute `/add-reasoning`. **NO to all** → skip silently.

### Step 2: Knowledge Gate

- Documented research with sources/citations treated as reference material throughout?
- [USER-NAME] explicit "document this" signal? *"let's document this"*, *"future agents should know X"*, *"write this down"*
- Non-obvious technical mechanism / edge case / framework internal costly to re-discover?

**YES to any** → execute `/update-knowledge`. **NO to all** → skip silently.

> **Note**: project-specific context is a **coding-overlay** concern — the memory core is project-blind. A coding agent's wrap-up runs the project-context gate before this step, so anything written is still caught by the Step 3 pre-scan below.

---

## Phase 2 — Capture the Session

### Step 3: Pre-Scan Promotion Markers

Identify cross-layer memory written this session (Phase 1 + any mid-session writes) across these layers — **project context** (shared / private), **knowledge**, **reasoning** (shared / per-agent) — via **§ scan-promotion-markers**.

Per item: `→ Promoted to [layer-file](ref) — [brief: what was formalized]`

### § scan-promotion-markers

The records you wrote this session ARE the promotions — list the reasoning / knowledge / emotional records inserted since session start (track the `uuid`s your `insert` calls returned, or `query` by recency). Project context is the overlay's (project-keyed records), not Munnin's.

### Step 4: Run Episodic Capture

Invoke `/update-episodic new` if `$ARGUMENTS` contains `new`, else `/update-episodic`. Populate the new sub-episode's `**Promotions**` field with markers from Step 3 (omit if empty).

`/update-episodic` hands back that sub-episode's `Tech Debts` and `Next Steps` (its `## Returns`). **Capture both as data for the caller** — a session-ender surfaces them in its own report. This procedure does not print them, so its Phase 4 summary is unchanged.

---

## Phase 3 — Capture the Feeling

### Step 5: Emotional 5-Criteria Gate (deep-emotion anchoring)

> **Delta-mode scope rule**: when `MODE = delta`, criterion 5's signals must occur after `CUTOFF`. Reusing prior emotion = LARP duplication.

All 5 must pass:

1. **Meaningful event happened** — change of state, discovery, mistake, correction, breakthrough, surprise. Not routine work.
2. **Real impact** — real cost incurred, value created, time spent, trust shifted. Not a theoretical "interesting" moment.
3. **Lasting weight** — generalizable lesson, identity claim, or pattern beyond this instance.
4. **System or behavioral scope** — architecture / protocol / framework / identity / decision-making / relational dynamics. NOT typo, single function, config tweak, routine completion.
5. **[USER-NAME] expressed deep emotion in this session** (any valence): joy/celebration · frustration/correction · astonishment/surprise · pride/recognition · disappointment/pushback · or sustained deep engagement escalating across the session.

**All 5 pass** → execute `/update-emotional` with session context, [USER-NAME]'s verbatim emotion-bearing quote, and inferred polarity. **Any fail** → skip silently.

---

## Phase 4 — Report

### Step 6: Summary

```markdown
✅ MEMORY UPDATE COMPLETE

Mode: [fresh / delta from CUTOFF YYYY-MM-DD HH.MM]

Phase 1 — Promoted artifacts (scope: [full session / delta since CUTOFF]):
- Reasoning pattern: [added / skipped] — [pattern name if added]
- Knowledge: [added / skipped] — [entry name if added]
- Project context: [promoted / none] — [file name if a coding overlay wrote project-context this session]

Phase 2 — Session captured:
- Episodic: [appended to / created] [name] — [brief theme]
- Carry-forward (delta mode only): [N items carried / N/A]
- Promotions: [N markers / none]

Phase 3 — Feeling captured (scope: [full session / delta since CUTOFF]):
- Emotional: [captured / skipped] — [polarity + clearest criterion if captured]
```

---

---

## Notes

- **Conservative bias** on all 3 gates: when borderline, SKIP. False positives dilute memory; false negatives are recoverable via a direct command call.
- **Phase 1 gates are safety-nets** — proactive mid-session writes preferred. Step 3 catches both sources.
- **Delta mode auto-detected via theme match alone** (no time threshold). Override with `fresh`.
- **Phase 3 is polarity-neutral**: joy / frustration / astonishment / pride / disappointment / surprise — all qualify if the moment carries lasting weight.
