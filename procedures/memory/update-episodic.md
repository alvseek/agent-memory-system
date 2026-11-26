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
#### Step 4: Compare candidates

- Read each candidate’s title and summary.
- Ask: **Does the work being saved continue the task, decision, or problem recorded in this episode?**
- Use shared keywords as clues. Don’t choose an episode just because it uses the same words.

#### Step 5: Choose where to save

- **One clear match** → Append to it without asking.
- **No match** → Follow Step 3’s no-match rule.
- **Unsure** → Show only the plausible candidates. Give one reason each might fit, then ask: **“Append to one of these, or start a new episode?”** Wait for the answer.

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

2. **Compose the entry title and body** using the sub-episode template (**§ template**).

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

1. **Compose the first entry title and body** using the sub-episode template (**§ template**).

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

