# Wrap Up Session

End-of-session orchestrator: comprehensive memory update + orientation map refresh + push + surface open items. Four active steps + summary.

Supports **delta wrap-up** out of the box: if you've already run `/wrap-up` earlier (in this conversation or a prior one) and continued working with more changes/fixes/questions, running `/wrap-up` again auto-detects the prior wrap-up via theme match and scopes Phase 1 + Phase 3 gate evaluations to the delta (work after the prior H3's timestamp). Carry-forward of unresolved open items is handled inside `/update-episodic`'s Append Sub-Episode branch.

## Arguments

`$ARGUMENTS`

- `/wrap-up` → Fire-and-forget session wrap-up (auto-detects delta vs fresh mode)
- `/wrap-up fresh` → Force fresh mode (full-session evaluation, ignores delta auto-detect — use when the auto-detect misfires or you genuinely want full-session re-eval)

---

## Procedure

### Step 1: Save Memory (Comprehensive)

Execute the [Update Memory Protocol](//@agent-memory/control-files/procedures/memory/update-memory.md) — pass the `fresh` arg through if present on `/wrap-up`'s invocation (i.e., `/wrap-up fresh` → `/update-memory fresh`). Otherwise invoke with default mode.

This orchestrates everything memory-related:
- **Phase 0** detects delta vs fresh mode (auto via theme + timestamp, or forced via `fresh` arg)
- Project context auto-eval (gated → conditional write via concrete checklist; scoped to delta if `MODE = delta`)
- Cross-layer promotion-marker pre-scan (project context / knowledge / reasoning)
- Episodic capture via `/update-episodic` (populates promotion markers + carry-forward of still-open items in the sub-episode when same-session predecessor exists)
- Emotional auto-capture if the 5-criteria gate passes (silent skip otherwise; scoped to delta if `MODE = delta`)

### Step 2: Refresh Orientation Map

If the session touched any orientation docs (READMEs, architecture docs, flow diagrams, ADRs), call:

```
/map-orientation --session-touched [path1,path2,...]
```

Pass the paths of orientation docs that this session created, edited, verified, or determined to be stale/obsolete. The skill updates affected entries' `last_verified` date, status, and `verified_by` based on session knowledge.

**Silent no-op cases**:
- Orientation map doesn't exist for the current project (user hasn't run `/map-orientation create` yet)
- Session touched no orientation docs (typical for pure discussion sessions, focused implementation work in already-mapped scope)

> **Why this step exists**: orientation docs change as projects evolve. Sessions that touch them should update the map so future awakenings load current information. Per the framework's automatic-vs-explicit split, this is a recurring write op invoked explicitly at wrap-up time — not a surprise scan.

### Step 3: Push Everything

Execute the [Push All Protocol](//@agent-memory/control-files/procedures/push-all.md) to commit and push both the current project and agent-memory repositories.

### Step 4: Surface Open Items

Read the just-written episodic sub-episode (newest H3 block at the top of the episodic file written in Step 1). Extract the `Tech Debts` and `Next Steps` fields from its Outcomes section.

> **Why reading the newest H3 alone is sufficient — even in delta mode**: the carry-forward review inside `/update-episodic`'s Append Sub-Episode (step 2 of that branch) ensures the newest H3 is self-contained, holding (still-open carried from prior) + (genuinely new from delta window). If carry-forward was performed correctly in Step 1, reading just the top block here surfaces everything that's still open.

Report to [USER-NAME] in a formal block — this is the carry-forward signal so [USER-NAME] knows what's left going into the next session:

```
📋 Open items going forward:

Tech debts:
- [item 1]
- [item 2]
(or "None declared")

Next steps:
- [item 1]
- [item 2]
(or "None declared")
```

If both Tech Debts and Next Steps are absent or empty in the episodic entry → report *"No open items declared from this session."*

> **Why this step exists**: per UUID a1b2c3d4 (NO TODOS LEFT BEHIND), open items must never be silent. The episodic entry has the fields; this step ensures they're surfaced at wrap-up so [USER-NAME] sees them, and they're preserved in episodic for next-session awakening to recall.

### Step 5: Summary

Report what was done:
```
Wrap-up complete (mode: [fresh / delta from CUTOFF]):
  - Memory update: [see /update-memory summary block above for full breakdown]
  - Orientation map: [refreshed N entries / no-op: no map / no-op: no orientation docs touched]
  - Push: [project: pushed/no changes] [agent memory: pushed/no changes]
  - Open items: [N tech debts, M next steps surfaced / no open items] [(delta mode: P carried forward from prior + Q new)]
```

---
