# Wrap Up Session

End-of-session orchestrator: memory update → orientation map refresh → push → final summary with open items.

**Delta-aware**: re-running `/wrap-up` after more work auto-scopes evaluations to the delta (theme match → cutoff = prior H3 timestamp). `/wrap-up fresh` forces full-session re-eval.

**Execution style**: silent. Run Steps 1-4 silently — tool calls (bash, edit, write) stay visible, but no prose narration of phases. Produce ONE summary block at Step 5 as the only user-facing output.

## Arguments

`$ARGUMENTS`

- `/wrap-up` → Default (delta vs fresh auto-detected by `/update-memory`)
- `/wrap-up fresh` → Force fresh mode (pass-through)

---

## Procedure

### Step 1: Save Memory (silent)

Execute [Update Memory Protocol](//@agent-memory/control-files/procedures/memory/update-memory.md). Pass `fresh` arg through if present. Capture results (mode, gate decisions, episodic entry, carry-forward count, promotions, emotional status) as data for Step 5. Do NOT print `/update-memory`'s own Phase 4 summary block separately — it gets folded into Step 5.

### Step 2: Refresh Orientation Map (silent)

If this session touched orientation docs (READMEs, architecture, flow diagrams, ADRs):

`/map-orientation --session-touched [path1,path2,...]`

Silent no-op if no map exists or no orientation docs touched. Capture refresh count / no-op reason for Step 5.

### Step 3: Push Everything (silent)

Execute [Push All Protocol](//@agent-memory/control-files/procedures/push-all.md). Tool calls visible (git commands); capture commit hashes / no-changes status for Step 5.

### Step 4: Extract Open Items (silent)

Read the newest H3 sub-episode block. Extract `Tech Debts` and `Next Steps` from Outcomes. Hold the full lists as data for Step 5.

### Step 5: Final Summary (only visible output)

Print ONE summary block:

```
Wrap-up complete (mode: [fresh / delta from CUTOFF]):

Memory update:
- Phase 1 — Promoted artifacts: project context: [updated/created — file / skipped] / reasoning: [added — pattern name / skipped] / knowledge: [added — entry name / skipped]
- Phase 2 — Session captured: [appended to / created] [filename] ([H3 timestamp]) — [brief theme]; carry-forward: [N items / N/A]; promotions: [N markers / none]
- Phase 3 — Feeling captured: emotional [captured — polarity + clearest criterion / skipped — brief reason]

Orientation map: [refreshed N entries / no-op: reason]

Push:
- [submodule]: [commit-hash pushed / no changes]
- [parent]: [commit-hash pushed / no changes]

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

If both Tech Debts and Next Steps are empty → replace both lists with *"No open items declared from this session."*
