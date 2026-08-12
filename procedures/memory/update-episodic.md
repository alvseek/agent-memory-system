# Update Episodic Memory Protocol

Capture session context as **rolling per-theme episodes**. The default flow scans active (non-archived) episodes for the current project, finds theme matches, and appends a dated sub-episode to the matching one — or creates a new episode if none matches. *How* episodes are physically listed / created / appended is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)).

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

2. **Compose the sub-episode block** using the [Detailed Entry Template](../../templates/episodic-entry-template.md). The H3 header includes the stamped date+time:
   ```
   ### YYYY-MM-DD HH.MM - [SESSION SUB-THEME] (agent: [domain])
   ```

3. **Append it newest-first** to the chosen episode (at the top, above older sub-episodes) and reflect the change in the index projection (**§ append-sub-episode**).

4. **Run post-write housekeeping** (**§ housekeeping**).

---

### Create New Episode

1. **Compose the first sub-episode block** using the [Detailed Entry Template](../../templates/episodic-entry-template.md). The H3 header includes the stamped date+time.

2. **Create a new episode** for `[project-name]-[context-theme]` seeded with that block, and register it in the index projection (**§ create-episode**).

---

### Force New Episode

`/update-episodic new` bypasses the scan + heuristic + confirm flow. Execute [Create New Episode](#create-new-episode) directly. Use when:
- The current session is intentionally a new theme even if it overlaps an existing one
- The agent wants to start fresh for any reason

Cross-layer orchestration is still handled by `/update-memory` if invoked through that command.

---

## Storage Mechanics

The operations referenced above — **§ stamp-date**, **§ list-candidate-episodes**, **§ append-sub-episode**, **§ create-episode**, **§ housekeeping** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow [storage-backends/markdown.md → ## update-episodic](storage-backends/markdown.md#update-episodic).
- **DB (Munnin)** — served automatically; the equivalents live in [storage-backends/db.md → ## update-episodic](storage-backends/db.md#update-episodic).

See the [seam contract](storage-backends/README.md) for how this swap works.

---

## Templates

### Detailed Entry Template

The sub-episode block format → **[templates/episodic-entry-template.md](../../templates/episodic-entry-template.md)**.
