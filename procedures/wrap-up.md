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

### Step 3: Push Everything (silent) — MANDATORY

Execute [Push All Protocol](//@agent-memory/control-files/procedures/push-all.md). Invoking `/wrap-up` IS the authorization to commit + push — The whole point of `/wrap-up` is to persist everything before the user walks away / shuts down.

⚠️ **Not every repo should be pushed.** Some are **vendored / third-party / read-only** dependencies  — pushing them is wrong, and their being dirty must NOT fail the wrap-up. **Before pushing, consult the project's push-exclude list** at `shared-memory/[project]/context/push-policy.md` (if present). Push every repo EXCEPT the excluded ones; excluded repos are reported as `skipped (excluded)`, never pushed, never counted against completion.

Tool calls visible (git commands); capture commit hashes for Step 5.

**Then verify (drives the Step 5 completion gate)**: run `git status --short` in every repo (project + submodules + agent-memory) and confirm each branch is pushed (not ahead of its remote). Record, per repo, whether the tree is **clean AND pushed** — **excluded repos are exempt** (report them as `skipped (excluded)`, not as failures). Do NOT attempt elaborate recovery — if a push of an *in-scope* repo fails or anything in-scope remains, that is simply carried to Step 5, where the wrap-up fails loudly.

### Step 4: Extract Open Items (silent)

Read the newest H3 sub-episode block. Extract `Tech Debts` and `Next Steps` from Outcomes. Hold the full lists as data for Step 5.

### Step 5: Final Summary (only visible output)

**Completion gate (per NO TODOS LEFT BEHIND, UUID a1b2c3d4)**: using the Step 3 verification, check every **in-scope** repo (repos on the project's push-exclude list are exempt). The wrap-up is **complete ONLY if EVERY in-scope repo is clean AND pushed**. If ANY in-scope repo has uncommitted changes, a branch ahead of its remote, or a failed push → **the wrap-up is NOT complete**: print the *WRAP-UP INCOMPLETE* block (at the bottom of this step) instead, and never claim completion. (Excluded repos never trigger this — they are reported as `skipped (excluded)`.)

**On success (every repo clean + pushed)**, print this block:

```
Wrap-up complete (mode: [fresh / delta from CUTOFF]):

Memory update:
- Phase 1 — Promoted artifacts: project context: [updated/created — file / skipped] / reasoning: [added — pattern name / skipped] / knowledge: [added — entry name / skipped]
- Phase 2 — Session captured: [appended to / created] [filename] ([H3 timestamp]) — [brief theme]; carry-forward: [N items / N/A]; promotions: [N markers / none]
- Phase 3 — Feeling captured: emotional [captured — polarity + clearest criterion / skipped — brief reason]

Orientation map: [refreshed N entries / no-op: reason]

Push (every in-scope repo must be ✅):
- [submodule]: ✅ [commit-hash] pushed / no changes
- [parent]: ✅ [commit-hash] pushed / no changes
- [excluded repo]: ⏭️ skipped (excluded — vendored/read-only)   ← only if the project has exclusions

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

---

**On failure (ANY repo not clean + pushed)** — do NOT print "Wrap-up complete". Print this block instead:

```
🚨 WRAP-UP INCOMPLETE — UNPUSHED WORK. NEED CONFIRMATION.

[Memory update / Orientation map / Open items sections — same as above]

Push — FAILED / INCOMPLETE:
- [repo]: ⚠️ [uncommitted N files / branch ahead by N / push error: <reason>]
- [repo]: ✅ [commit-hash] pushed

⚠️ Your work is NOT fully saved to the remote. What remains, and where:
- [repo → what's uncommitted/unpushed]

Retry the push (or resolve the blocker) before leaving — the wrap-up is only complete when every repo is clean AND pushed.
```
