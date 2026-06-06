# Wrap Up Session

End-of-session orchestrator: comprehensive memory update + push + surface open items. Three active steps + summary.

## Arguments

`$ARGUMENTS`

- `/wrap-up` → Fire-and-forget session wrap-up (all steps automatic)

---

## Procedure

### Step 1: Save Memory (Comprehensive)

Execute the [Update Memory Protocol](//@agent-memory/control-files/procedures/memory/update-memory.md) using default mode. This orchestrates everything memory-related:
- Project context auto-eval (gated → conditional write via concrete checklist)
- Cross-layer promotion-marker pre-scan (project context / knowledge / reasoning)
- Episodic capture via `/update-episodic` (populates promotion markers in the sub-episode)
- Emotional auto-capture if the 5-criteria gate passes (silent skip otherwise)

### Step 2: Push Everything

Execute the [Push All Protocol](//@agent-memory/control-files/procedures/push-all.md) to commit and push both the current project and agent-memory repositories.

### Step 3: Surface Open Items

Read the just-written episodic sub-episode (newest H3 block at the top of the episodic file written in Step 1). Extract the `Tech Debts` and `Next Steps` fields from its Outcomes section.

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

### Step 4: Summary

Report what was done:
```
Wrap-up complete:
  - Memory update: [see /update-memory summary block above for full breakdown]
  - Push: [project: pushed/no changes] [agent memory: pushed/no changes]
  - Open items: [N tech debts, M next steps surfaced / no open items]
```

---
