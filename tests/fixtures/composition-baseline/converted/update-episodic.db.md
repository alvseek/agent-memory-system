> `<domain>` in the ops below is the agent you are acting as — the domain you passed to `awaken`, or the one `create-agent` made. With no awakening, `list_agents()` shows what exists; never guess one.

**A body read is a page, and a listing or a search is not a body.** Three shapes, and mixing them up is the one way to read partial context as whole:

- **`query`** answers *which records match*: metadata only (uuid, title, `content_summary`, tags, project, dates) plus **`blocks_total`** — how many timestamp groups that record's body holds. It never returns `content`.
- **`search`** answers *what matched*: the same metadata plus a plain-text **`snippet`** of the matching window, and no body under either name. Reaching a body from a hit is a deliberate `get(uuid)`.
- **`get(uuid)`** answers *what the record says*: as much of the body as fits under the content ceiling in one response — the whole of a small record, one **page** of a large one — or exactly one page when you pass `cursor`/`limit`. Every `get` response carries `blocks_returned` / `blocks_total` / `next_cursor`, so a non-null cursor is how you know a large record did not arrive whole.

A **timestamp group** is every sub-episode block in the record that shares one `###` H3 timestamp; a group is indivisible and counts as one, so `blocks_total: 5` means five distinct moments. Two rules follow, and only one of them is a continuation:

- **`next_cursor` non-null means more remains** — pass it straight back as `get(uuid, cursor=…)`, or with `limit=` to keep the page small. It names the *first group not returned*, so a block prepended in between cannot shift your place, and it is the only signal that answers "is there more?".
- **`blocks_returned` < `blocks_total` does *not* mean more remains.** A final page returns fewer than the whole record and is complete. Never continue on the count alone.

An unknown or malformed cursor, or a non-positive `limit`, is an error — never a quiet fall back to page one. Cursors are per record: pass the page's own `uuid` with its cursor. A record that is not an episode (identity, reasoning, emotional, knowledge, the profile, the RAS triggers) is one atomic block — `blocks_total: 1` — because it is not a rolling document. Nothing ever splits a sub-episode block, and no repair step exists: a retimestamped or deleted target makes the old cursor fail loudly rather than resume somewhere else.

# Update Episodic Memory Protocol

Capture session context as **rolling per-theme episodes**. The default flow scans active (non-archived) episodes for the current project, finds theme matches, and appends a dated sub-episode to the matching one — or creates a new episode if none matches. *How* episodes are physically listed / created / appended is delegated to the active **storage backend**.

## Arguments

`$ARGUMENTS`

- `/update-episodic` → Default flow: scan, heuristic match, confirm, then append or create (see [Default Flow](#default-flow))
- `/update-episodic new` → Force new episode, skip scan/heuristic (see [Force New Episode](#force-new-episode))

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Default Flow

#### Step 1: Stamp the Time

Obtain the current date+time for the sub-episode H3 header (**§ stamp-date**).

### § stamp-date

**No action.** The server stamps `created_date` / `updated_date` on write; use the block's H3 timestamp as authored.

#### Step 2: Identify Project + Theme

Determine:
- **Project name**: the current project being worked on (from working directory or session context — e.g., `agent-memory`, `plko`, `ocx-platform`)
- **Theme keywords**: 2-5 noun/topic keywords summarizing this session's focus (e.g., `episodic`, `rolling-file`, `redesign`)

#### Step 3: List + Scan Candidate Episodes

List the active (non-archived) episodes for the current project (**§ list-candidate-episodes**). Collect all whose filename or summary contains the **project name** — these are the scan candidates.

If no candidates → skip to Step 6 (Create branch).

> **Why active-only?** The active episode set is already at hand (loaded at awakening / cheap to query). Archived entries are intentionally out of reach — old context should not be merged into.
>
> **The one exception, and only on request**: when the user names a theme that is not in the active list because they are continuing it, look for it among the archived episodes before creating a second record for the same theme. Reopening is a deliberate action, never a scan behaviour: it clears the `finished` marker and returns the record to the active set (**§ reopen-archived-theme**), and the block then appends normally. A theme that is genuinely finished gets a successor file instead (Step 6, Create branch).

### § list-candidate-episodes

`query(agent_id="<domain>", record_type="episode", project="<project>")` → returns the derived index projection (uuid, title, content_summary, tags, dates, **`blocks_total`**) for the agent's active episodes. Theme-match against `title`/`tags`, and read `content_summary` when the theme alone is ambiguous. There is no body here — reading one is a deliberate `get(uuid)`, a page at a time (see `## all-procedures`). `blocks_total` tells you how much body that read will hold before you pay for it. (Archived episodes are excluded by default — pass `include_archived=True` only to reach them.)

### § reopen-archived-theme

Two calls, in this order: `edit_metadata(uuid, tags=[<existing without finished>])`, then `unarchive(uuid)`. Clearing first matters — leave the marker in place and the next scan archives the theme straight back. `unarchive` returns the record to the index and to newest-episode selection, after which the append lands normally.

#### Step 4: Match Heuristic

For each candidate, score theme overlap:
- Tokenize the candidate's filename (sans extension and any legacy date prefix) and summary
- Count keyword overlap with this session's theme keywords
- Higher overlap = stronger merge signal

Identify:
- **Top match**: highest-scoring candidate (if any meaningful overlap exists)
- **Runner-ups**: 2nd-3rd scoring candidates if scores are close

If the top match has zero meaningful overlap, treat as "no match" → skip to Step 6 (Create branch).

#### Step 5: Confirm Match

Present the top match (and any close runner-ups) to [USER-NAME]:

```
Theme match candidate(s) found:
  → [name] — [summary] (overlap: keyword1, keyword2)
  → [runner-up name] — [summary] (overlap: keyword1)

Append a new sub-episode to this one? Or create a new episode?
  A) Append to [top-match]
  B) Create new episode
  C) Append to a different existing one (specify)
```

Wait for response. Auto-default to **A** only if confidence is high (≥3 strong overlapping keywords AND same project tag). Otherwise wait for explicit confirmation.

#### Step 6: Branch — Append OR Create

- **If Append** → execute [Append Sub-Episode](#append-sub-episode)
- **If Create** → execute [Create New Episode](#create-new-episode)

> **Scope note**: `/update-episodic` only writes the episode + its index projection. Cross-layer concerns (promotion markers to project context / knowledge / reasoning, and emotional memory auto-capture) are handled by `/update-memory`, which calls this procedure and then orchestrates the cross-layer work. If you're calling `/update-episodic` directly and want cross-layer orchestration, use `/update-memory` instead.

---

### Append Sub-Episode

1. **Carry-forward review of prior open items**: the target's most recent prior sub-episode (the top H3 our new block will sit above) holds the latest open items. Review them so the new block stays self-contained:
   - **a. Read prior open items**: extract the `**Tech Debts**` and `**Next Steps**` fields from the prior top sub-episode's Outcomes.
   - **b. Review each against work done since that prior sub-episode's timestamp**:
     - *Resolved by the delta work?* → drop from carry-forward list.
     - *Still open?* → keep (verbatim, or refined if the delta clarified scope).
   - **c. Stage the carry-forward list**: the new block's `**Tech Debts**` and `**Next Steps**` become the **union** of (still-open carried forward) + (genuinely new items from this delta window).

   > **Why this matters**: both wrap-up and awakening read only the newest sub-episode when surfacing open items. Without carry-forward, prior unresolved debts get hidden and the next awakening won't see them. Carry-forward keeps the newest block self-contained, preserving the read-newest-only invariant.

   > **Why no time threshold**: the prior sub-episode's timestamp is deterministic. Recent prior (same conversation) → full context to review each item. Older prior (different session) → items are still carry-forward candidates, reviewed on their own descriptions; items that can't be confidently evaluated default to "still open" (conservative, per UUID a1b2c3d4 — debts never silently dropped).

2. **Compose the sub-episode block** using the sub-episode-block template (**§ template**). The H3 header includes the stamped date+time:
   ```
   ### YYYY-MM-DD HH.MM - [SESSION SUB-THEME] (agent: [domain])
   ```

3. **Append it newest-first** to the chosen episode (at the top, above older sub-episodes) and reflect the change in the index projection (**§ append-sub-episode**).

4. **Run post-write housekeeping** (**§ housekeeping**).

5. **Set the theme's state**: does this block close the theme? Ensure the record carries the `finished` marker when it does and does not carry it when it does not (**§ record-theme-state**). One state per block, written once at the end — never remove the marker in order to add it back in the same run.

---

### § template

**Served as an MCP Resource** (`episodic-entry-template`) — read it from resources. (`§ create-episode` inserts the record directly, so there is no separate scaffold template.)

### § append-sub-episode

An episode is a single record whose body is the rolling, newest-first sub-episode list. Newest-first then needs no read and no string match — two writes:
1. `prepend(uuid, text="<new H3 block>\n\n---\n\n")` — the new block lands above the previous newest, and the separator you include keeps the two apart. Nothing has to match, so there is no `old_string` to get uniquely right.
2. `edit_metadata(uuid, content_summary="<the record's summary>")` — the summary is metadata and has one writer, so it moves in its own call.

`content_summary` is the whole new summary, not an appended fragment: it describes the record's newest content, so skipping step 2 leaves the listing describing a block the body no longer starts with. Two writes can also disagree if the second fails, which is why both steps belong to this op rather than to the caller's judgement — that is the price of one owner per field.

The index reflects the change automatically (derived `SELECT`).

### § housekeeping

**No-op.** The stored body has no length limit — shortening is a later curation *policy*, not a write mechanic — and records are keyed by `uuid`, so there is no split or rename to perform. Delivery is what is bounded now: a body is read as pages of timestamp groups, so a large record costs a cursor and not a truncated answer. Do not add a "split this record" step to compensate for a page.

### § record-theme-state

`edit_metadata(uuid, tags=[…])` — the tag list is written whole, so pass the record's existing tags with `finished` added when the block closes the theme, and the existing tags with it removed when it does not. `tags` is metadata with one writer, so this never rides on the body append. The write bumps `modified_date`, which is why the archive scan weighs the tag before the age.

A newly created episode carries no marker, so a create needs no call; an append that changes the state does.

### Create New Episode

1. **Compose the first sub-episode block** using the sub-episode-block template (**§ template**). The H3 header includes the stamped date+time.

2. **Create a new episode** for `[project-name]-[context-theme]` seeded with that block, and register it in the index projection (**§ create-episode**).

3. **Set the theme's state**: a brand-new episode is by definition open, so ensure it carries no `finished` marker (**§ record-theme-state**). This is the same rule as the append branch, applied once, so a continuation can never inherit a stale marker.

---

### § create-episode

`insert(agent_id="<domain>", record_type="episode", project="<project>", title="<project-theme>", tags=[…], content="<first sub-episode block>", content_summary="<the block's Summary row>", template_version="<the template's current stamp>")`. Read `episodic-entry-template` from resources first and declare its `template_version` — a missing or stale version is refused. `content_summary` is required for an episode: pass the block's `**Summary**` row verbatim, because that one line is what the index projection lists the record by. The record is assembled and `uuid`-stamped server-side and appears in the index projection immediately.

### Force New Episode

`/update-episodic new` bypasses the scan + heuristic + confirm flow. Execute [Create New Episode](#create-new-episode) directly. Use when:
- The current session is intentionally a new theme even if it overlaps an existing one
- The agent wants to start fresh for any reason

Cross-layer orchestration is still handled by `/update-memory` if invoked through that command.

---

## Returns

This procedure hands two values back to its caller — **`Tech Debts`** and **`Next Steps`**, exactly as they were written into the sub-episode block. They are **captured as data, never printed**: `/update-memory` runs this procedure inside its silent phases, and the caller that surfaces open items prints them once in its own summary.

Both branches produce them:

- **Append** — the union staged in [Append Sub-Episode](#append-sub-episode) step 1c: items carried forward from the prior top sub-episode that are still open, plus genuinely new items from this delta window.
- **Create** — the two fields as composed for the first sub-episode of a new episode. There is no prior block to carry forward from, so the lists hold this session's items alone. An empty list is a real answer here — it means "none declared", not "not available".

Because both branches compose these lists before writing them, a caller never has to re-read the store to learn what the newest sub-episode says: the agent that wrote the block is the one being asked.

---

