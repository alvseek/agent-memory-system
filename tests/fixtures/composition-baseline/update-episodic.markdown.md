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

Obtain the current date+time for the sub-episode H3 header and index-entry placement (**§ stamp-date**).

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

### Create New Episode

1. **Compose the first sub-episode block** using the sub-episode-block template (**§ template**). The H3 header includes the stamped date+time.

2. **Create a new episode** for `[project-name]-[context-theme]` seeded with that block, and register it in the index projection (**§ create-episode**).

3. **Set the theme's state**: a brand-new episode is by definition open, so ensure it carries no `finished` marker (**§ record-theme-state**). This is the same rule as the append branch, applied once, so a continuation can never inherit a stale marker.

---

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

### § stamp-date

ALWAYS CHECK DATE TIME FIRST for the sub-episode H3 header and index entry placement:
`date '+%Y-%m-%d %H:%M'`

### § list-candidate-episodes

Read `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` and locate `# Recent Context Episodes`. Collect all entries where the filename or summary contains the **project name**. These are scan candidates. (Archived entries live in `archive/` and are intentionally out of reach.)

### § append-sub-episode

1. **Open the chosen file** in `[AGENT-MEMORY-PATH]/agent-[domain]/episodes/`.
2. **Insert the sub-episode H3 block at the TOP** (newest-first within the file), above any older H3 blocks. Sub-episodes are separated by `---`.
3. **Update the index entry — MOVE-TO-TODAY rule**:
   - Locate the existing entry for this file in the index.
   - Delete it from its current date group (if the group becomes empty, remove the group header too).
   - Insert at the **top of today's date group** (`📂 YYYY-MM-DD:`); create today's group if it doesn't exist.
   - Update the summary from the new block's `**Summary**` row: carry that text verbatim, appended as `+ [new sub-topic]` when the overall theme still holds, or rewritten when the new sub-topic shifts it.

   > **Why move?** Awakening's project-scoped episodic load grabs the top entry as "latest episodic." The move preserves the "top = newest" invariant. Edit-in-place would leave a stale top entry and break awakening's selection logic.

### § create-episode

1. **Build filename**: `[project-name]-[context-theme].md` (no date prefix). Examples: `agent-memory-task-system-framework-rules.md`, `plko-jira-mcp-integration.md`. If a file at this name already exists (and a separate file is wanted), use an incrementing suffix: `[project-name]-[context-theme]-2.md`.
2. **Copy the file scaffold**:
   ```
   cp [AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/episodic-memory-template.md [AGENT-MEMORY-PATH]/agent-[domain]/episodes/[filename].md
   ```
3. **Set the frontmatter `project`** in the new file to the project name, then **replace the template placeholder** at the top with the composed sub-episode block. The frontmatter is what the importer reads into the record's `project`; the filename is convention, not the source.
4. **Add index entry**:
   - Insert at the **top of today's date group** (`📂 YYYY-MM-DD:`); create today's group if it doesn't exist.
   - Entry format: `- [filename.md](episodes/filename.md) - [one-line summary]`, where the summary is the new block's `**Summary**` row copied verbatim. This entry is the record's listed description, so it and the block must not diverge.

### § housekeeping

1. **Check line limit** after an append:
   - **> 500 lines**: warn — *"[filename] over 500 lines, consider splitting on next merge"*.
   - **> 1000 lines**: split — move the *just-added* sub-episode into `[project]-[theme]-2.md` (next incrementing suffix if `-2` exists). Add `> Continues from [original-filename]` at the top of the new file. Add a new index entry for the split file under today's date group.
2. **Lazy filename migration** (one-time per file): if the chosen file still uses the legacy `YYYY-MM-DD-HH.MM-[project]-[theme].md` format, rename it to `[project]-[theme].md` as part of this append and update the index entry's filename reference. If a file at the new name already exists (rare collision), use the line-limit `-{n}` suffix rule.

> **Episodes folder structure**:
> ```
> episodes/
> ├── [project-name]-[context-theme].md        # Active episode file (rolling per theme)
> ├── [project-name]-[context-theme]-2.md      # Split file when 1000-line cap hit
> ├── YYYY-MM-DD-HH.MM-[project]-[theme].md    # Legacy dated files (lazy migration)
> └── archive/                                  # Archived old episodes (via /archive-old-memories)
>     └── YYYY-archived-context.md
> ```
> Legacy filenames are migrated lazily — only renamed when the file gets its next merge-append. No bulk sweep.

### § template

The sub-episode block format → read `[AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/episodic-entry-template.md`.

### § record-theme-state

Edit the episode file's frontmatter `tags:` line in place: add `finished` when this block closes the theme, remove it when it does not. Touch nothing else — the body and the other frontmatter fields stay verbatim.

When no `tags:` line exists yet, add one beneath `project:` in the same block. The importer reads episode frontmatter tags into the record, so the marker survives a later import into the DB store even though no tool here reads it.

### § reopen-archived-theme

Markdown keeps no archive flag on a record: an archived episode is one whose index line was moved into `archive/[YYYY]-archived-context.md`, while the file itself never moved. To reopen it, remove `finished` from the file's frontmatter, move its index line back from the archive file into the episode index (newest-first, under today's date group), and decrement the archive's count. Then append normally.

---
