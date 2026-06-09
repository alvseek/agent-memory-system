# Wrap Up Session

End-of-session orchestrator: memory update → orientation map refresh → push → surface open items → summary.

**Delta-aware**: re-running `/wrap-up` after more work auto-scopes evaluations to the delta (theme match → cutoff = prior H3 timestamp). `/wrap-up fresh` forces full-session re-eval.

## Arguments

`$ARGUMENTS`

- `/wrap-up` → Default (delta vs fresh auto-detected by `/update-memory`)
- `/wrap-up fresh` → Force fresh mode (pass-through)

---

## Procedure

### Step 1: Save Memory

Execute [Update Memory Protocol](//@agent-memory/control-files/procedures/memory/update-memory.md). Pass `fresh` arg through if present.

### Step 2: Refresh Orientation Map

If this session touched orientation docs (READMEs, architecture, flow diagrams, ADRs):

`/map-orientation --session-touched [path1,path2,...]`

Silent no-op if no map exists or no orientation docs touched.

### Step 3: Push Everything

Execute [Push All Protocol](//@agent-memory/control-files/procedures/push-all.md).

### Step 4: Surface Open Items

Read the newest H3 sub-episode block. Extract `Tech Debts` and `Next Steps` from Outcomes.

Report:
```
📋 Open items going forward:

Tech debts:
- [item]
(or "None declared")

Next steps:
- [item]
(or "None declared")
```

If both empty → *"No open items declared from this session."*

### Step 5: Summary

```
Wrap-up complete (mode: [fresh / delta from CUTOFF]):
  - Memory update: [see /update-memory summary above]
  - Orientation map: [refreshed N entries / no-op]
  - Push: [project: pushed/no changes] [agent memory: pushed/no changes]
  - Open items: [N tech debts, M next steps surfaced / no open items] [(delta: P carried + Q new)]
```
