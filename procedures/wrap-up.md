+++
format_version = 2
id = "wrap-up"
kind = "procedure"
title = "Wrap Up Session"
description = "End-of-session **memory** orchestrator: update memory → persist the store → report. Capturing a session and saving it are one job here rather than two — the procedure writes the memory layers and then commits whatever the active storage backend needs committing, so a session never ends with its own record written but unsaved."
argument_name = "mode"
argument_description = "agent (default) or all; add fresh to re-evaluate the whole session"
calls = { markdown = ["update-memory", "push-memory"], db = ["update-memory"] }
+++
# Wrap Up Session

End-of-session **memory** orchestrator: update memory → persist the store → report. Capturing a session and saving it are one job here rather than two — the procedure writes the memory layers and then commits whatever the active storage backend needs committing, so a session never ends with its own record written but unsaved.

What it does not touch is the working project: no project push, no orientation map. Those belong to a coding/environment add-on, which composes a fuller project wrap-up on top of this one.

**Delta-aware**: re-running `/wrap-up` after more work auto-scopes evaluations to the delta (theme match → cutoff = prior sub-episode timestamp). `/wrap-up fresh` forces full-session re-eval.

**Execution style**: silent. Run the steps silently — tool calls stay visible, but no prose narration. Produce ONE report block at the final step as the only user-facing output.

## Arguments

**Mode:** `$ARGUMENTS` — `[all|agent] [fresh]`.

- `agent` (default) persists only this agent's memory; `all` persists the whole store.
- `fresh` tells `/update-memory` to re-evaluate the whole session. Without it, `/update-memory` detects delta vs. fresh from the session theme.
- Examples: `/wrap-up` (agent, auto-detect) · `/wrap-up all` · `/wrap-up fresh` · `/wrap-up all fresh`.

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

@start storage id="wrap-up.report" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.report" applies_to="markdown"
@end storage
@start storage id="wrap-up.report-db" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.report-db" applies_to="db"
@end storage

If both Tech Debts and Next Steps are empty → replace both lists with *"No open items declared from this session."*


---

> **Working in a repo as well?** This wrap-up saves memory and nothing else. If a coding/environment add-on is installed, use its fuller project wrap-up instead — it pushes the project's work first so a merge request can open without waiting, runs this memory update, refreshes the orientation map, and gates on both pushes together.
@start storage id="wrap-up.failure-report" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.failure-report"
@end storage
