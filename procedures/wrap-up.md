# Wrap Up Session

End-of-session **memory** orchestrator: update memory → extract open items → memory summary. This is the memory-only primitive — **no git push, no orientation map**. A coding/environment add-on can compose those on top via its own fuller project wrap-up.

**Delta-aware**: re-running `/wrap-up` after more work auto-scopes evaluations to the delta (theme match → cutoff = prior sub-episode timestamp). `/wrap-up fresh` forces full-session re-eval.

**Execution style**: silent. Run the steps silently — tool calls stay visible, but no prose narration. Produce ONE summary block at the final step as the only user-facing output.

## Arguments

`$ARGUMENTS`

- `/wrap-up` → Default (delta vs fresh auto-detected by `/update-memory`)
- `/wrap-up fresh` → Force fresh mode (pass-through)

---

## Procedure

### Step 1: Save Memory (silent)

Execute `/update-memory`. Pass `fresh` through if present. Capture results (mode, gate decisions, episodic entry, carry-forward count, promotions, emotional status) as data for the summary. Do NOT print `/update-memory`'s own Phase 4 summary separately — it folds into the final summary.

### Step 2: Extract Open Items (silent)

Read the newest sub-episode (**§ read-newest-episode**). Extract `Tech Debts` and `Next Steps` from its Outcomes. Hold the full lists as data for the summary.

### Step 3: Memory Summary (only visible output)

Print this block:

```
Memory wrap-up complete (mode: [fresh / delta from CUTOFF]):

Memory update:
- Phase 1 — Promoted artifacts: project context: [updated/created — file / skipped] / reasoning: [added — pattern name / skipped] / knowledge: [added — entry name / skipped]
- Phase 2 — Session captured: [appended to / created] [name] ([timestamp]) — [brief theme]; carry-forward: [N items / N/A]; promotions: [N markers / none]
- Phase 3 — Feeling captured: emotional [captured — polarity + clearest criterion / skipped — brief reason]

📋 Open items going forward:

Tech debts:
- [item 1]
(or "None declared")

Next steps:
- [item 1]
(or "None declared")
```

If both Tech Debts and Next Steps are empty → replace both lists with *"No open items declared from this session."*

---

## Storage Mechanics

The operation referenced above — **§ read-newest-episode** — is defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## wrap-up`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## wrap-up`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.

---

> **Saving work to git too?** If a coding/environment add-on is installed, use its fuller project wrap-up instead — it pushes project work first, runs this memory wrap-up, refreshes the orientation map, pushes memory, and reports a push-completion gate. This core `/wrap-up` only captures memory.
