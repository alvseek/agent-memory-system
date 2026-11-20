+++
format_version = 2
id = "wrap-up"
kind = "procedure"
title = "Wrap Up Session"
description = "End-of-session **memory** orchestrator: update memory → persist the store → report. Capturing a session and saving it are one job here rather than two — the procedure writes the memory layers and then commits whatever the active storage backend needs committing, so a session never ends with its own record written but unsaved."
argument_name = "mode"
argument_description = "Input described in the procedure's Arguments section"
calls = { markdown = ["update-memory", "push-memory"], db = ["update-memory"] }
+++
@start storage id="caller-context" ref="procedures/memory/storage-backends/{backend}.md" target="caller-context"
@end storage
# Wrap Up Session

End-of-session **memory** orchestrator: update memory → persist the store → report. Capturing a session and saving it are one job here rather than two — the procedure writes the memory layers and then commits whatever the active storage backend needs committing, so a session never ends with its own record written but unsaved.

What it does not touch is the working project: no project push, no orientation map. Those belong to a coding/environment add-on, which composes a fuller project wrap-up on top of this one.

**Delta-aware**: re-running `/wrap-up` after more work auto-scopes evaluations to the delta (theme match → cutoff = prior sub-episode timestamp). `/wrap-up fresh` forces full-session re-eval.

**Execution style**: silent. Run the steps silently — tool calls stay visible, but no prose narration. Produce ONE report block at the final step as the only user-facing output.

## Arguments

`$ARGUMENTS` = `[all|agent] [fresh]`

- **Mode** (optional): `agent` (default) persists only this agent's own memory, leaving a concurrently-running agent's in-flight work untouched; `all` persists the whole store. The default is the conservative one because `/wrap-up` runs at session end, when nobody is watching what else in the store happens to be dirty.
- **`fresh`** (optional): force fresh mode for the memory update (pass-through to `/update-memory`); default auto-detects delta vs fresh.
- Examples: `/wrap-up` (agent + delta) · `/wrap-up all` · `/wrap-up fresh` · `/wrap-up all fresh`.

---

## Procedure

**Resolve args first**: `<mode>` = `all` if `$ARGUMENTS` contains the token `all`, else `agent` (the default). Pass `fresh` through to the memory update if present.

### Step 1: Save Memory (silent)

Execute `/update-memory`. Pass `fresh` through if present. Capture as data for the report: mode, gate decisions, episodic entry, carry-forward count, promotions, emotional status — and the **`Tech Debts` + `Next Steps`** it hands up from the sub-episode just written (see `/update-episodic`'s `## Returns`). Do NOT print `/update-memory`'s own Phase 4 summary separately — it folds into the final report.

> The open items arrive with the write instead of being read back out of the store afterwards. The agent that composed that block is the one being asked, so there is no second read to go stale.

### Step 2: Persist the Store (silent)

Save what Step 1 just wrote (**§ persist-store**). What that costs depends on the backend — a git-backed store needs a commit and a push, a database-backed one is already durable the moment the write lands — so this step reports an **outcome** rather than assuming an operation happened.

Capture that outcome for Step 3: whether everything in scope is committed AND pushed (per repo, where the backend has repos), plus any failure reason.

@start storage id="wrap-up.persist-store" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.persist-store"
@end storage
### Step 3: Wrap-Up Report (only visible output)

**Completion gate** (UUID a1b2c3d4): report completion only when Step 2 confirms this session's memory is persisted. Apply the selected backend's persistence and failure rules below.

**On success**, print this block:

```
Wrap-up complete (mode: [agent / all] · [fresh / delta from CUTOFF]):

Memory update:
- Phase 1 — Promoted artifacts: project context: [updated/created — file / skipped] / reasoning: [added — pattern name / skipped] / knowledge: [added — entry name / skipped]
- Phase 2 — Session captured: [appended to / created] [name] ([timestamp]) — [brief theme]; carry-forward: [N items / N/A]; promotions: [N markers / none]
- Phase 3 — Feeling captured: emotional [captured — polarity + clearest criterion / skipped — brief reason]

@@start storage id="wrap-up.persistence-report" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.persistence-report"
@@end storage
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

> **Working in a repo as well?** This wrap-up saves memory and nothing else. If a coding/environment add-on is installed, use its fuller project wrap-up instead — it pushes the project's work first so a merge request can open without waiting, runs this memory update, refreshes the orientation map, and gates on both pushes together.
@start storage id="wrap-up.failure-report" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.failure-report"
@end storage
