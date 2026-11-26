+++
format_version = 2
id = "update-episodic"
kind = "procedure"
title = "Update Episodic Memory Protocol"
description = "Save a dated session entry in a new or existing episode for the current project."
argument_name = "mode"
argument_description = "`new` to force a new episode instead of appending"
+++
# Update Episodic Memory Protocol

An episode groups dated session entries by theme. By default, look for a matching active episode in the current project. Add the entry to that episode, or create one if none matches.

## Arguments

`$ARGUMENTS` — optional `new`. Use it to [create a separate episode](#force-new-episode) without scanning for a match. Otherwise, follow the [default flow](#default-flow).

---

## Procedure

### Default Flow

#### Step 1: Stamp the Time

Get the current local date and time for the new entry’s heading (`YYYY-MM-DD HH.MM`), whether adding to an episode or creating one.

@start storage id="update-episodic.stamp-date" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.stamp-date" applies_to="markdown"
@end storage
#### Step 2: Identify Project + Theme

- **Project:** Use the project supplied by the caller. If none is supplied, leave the episode unassigned. For a new unassigned episode, use the theme alone as its name.
- **Theme:** Identify the subject of the work being recorded. Choose keywords from that subject to compare candidate episodes.

#### Step 3: List + Scan Candidate Episodes

List the acting agent’s active (non-archived) episodes for the selected project, or only their unassigned episodes if no project was supplied (**§ list-candidate-episodes**).

@start storage id="update-episodic.list-candidate-episodes" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.list-candidate-episodes"
@end storage

If no active episode matches, search the archive in the same scope **only if the user asked to continue a specific theme**. Reopen a matching episode to continue that work (**§ reopen-archived-theme**). Otherwise create a new episode, including for follow-up work on a finished theme.

@start storage id="update-episodic.reopen-archived-theme" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.reopen-archived-theme"
@end storage
#### Step 4: Match Heuristic

For each candidate, score theme overlap:
- Tokenize the candidate's filename (sans extension and any legacy date prefix) and summary
- Count keyword overlap with this session's theme keywords
- Higher overlap = stronger merge signal

Identify:
- **Top match**: highest-scoring candidate (if any meaningful overlap exists)
- **Runner-ups**: 2nd-3rd scoring candidates if scores are close

If no candidate has meaningful overlap, use Step 3’s no-match rule.

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

> `/update-episodic` saves the episode and updates its index. To evaluate the session for reasoning, knowledge, or emotional memory as well, use `/update-memory`.

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

2. **Compose the sub-episode block** using the sub-episode-block template (**§ template**). The H3 header includes the stamped date+time and the domain you are acting as:
   ```
   ### YYYY-MM-DD HH.MM - [SESSION SUB-THEME] (agent: [domain])
   ```

3. **Append it newest-first** to the chosen episode (at the top, above older sub-episodes) and reflect the change in the index projection (**§ append-sub-episode**).

4. **Run post-write housekeeping** (**§ housekeeping**).

5. **Set the theme's state**: does this block close the theme? Ensure the record carries the `finished` marker when it does and does not carry it when it does not (**§ record-theme-state**). One state per block, written once at the end — never remove the marker in order to add it back in the same run.

---

@start storage id="update-episodic.template" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.template"
@end storage
@start storage id="update-episodic.append-sub-episode" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.append-sub-episode"
@end storage
@start storage id="update-episodic.housekeeping" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.housekeeping"
@end storage
@start storage id="update-episodic.record-theme-state" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.record-theme-state"
@end storage
### Create New Episode

1. **Compose the first sub-episode block** using the sub-episode-block template (**§ template**). The H3 header includes the stamped date+time and the domain you are acting as.

2. **Create a new episode** for `[project-name]-[context-theme]` seeded with that block, and register it in the index projection (**§ create-episode**).

3. **Set the theme's state**: a brand-new episode is by definition open, so ensure it carries no `finished` marker (**§ record-theme-state**). This is the same rule as the append branch, applied once, so a continuation can never inherit a stale marker.

---

@start storage id="update-episodic.create-episode" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.create-episode"
@end storage
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

