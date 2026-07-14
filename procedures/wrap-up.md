# Wrap Up Session

End-of-session orchestrator: memory update → orientation map refresh → push the agent's work → final summary with open items.

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

### Step 3: Push the Agent's Work (silent) — MANDATORY

Execute [Push Agent Work Protocol](//@agent-memory/control-files/procedures/push-agent-work.md). Invoking `/wrap-up` IS the authorization to commit + push — but an **automatic** wrap-up pushes **only the agent's own work** (agent-memory repo + agent-produced paths in the project), never a blanket `git add -A` on the working project. (Explicit `/push-all` / `/push-project` stay full-tree — that is a deliberate user choice.)

Tool calls visible (git commands); capture per-repo commit hashes, agent-work-pushed status, and user-files-left counts for Step 5.

**Then verify (drives the Step 5 completion gate)**: from Push Agent Work's Step 3 verification, record per repo whether **every agent-work path is committed AND pushed** (branch not ahead of remote) + a count of user files left. **Excluded repos are exempt** (report as `skipped (excluded)`). Do NOT attempt elaborate recovery — if an *agent-work* push fails or any agent-work path remains, that is carried to Step 5, where the wrap-up fails loudly.

### Step 4: Extract Open Items (silent)

Read the newest H3 sub-episode block. Extract `Tech Debts` and `Next Steps` from Outcomes. Hold the full lists as data for Step 5.

### Step 5: Final Summary (only visible output)

**Completion gate (per NO TODOS LEFT BEHIND, UUID a1b2c3d4)**: using the Step 3 verification, the wrap-up is **complete ONLY if every agent-work path is committed AND pushed** in every in-scope repo. A project repo that still holds the **user's own** uncommitted changes is still complete — leftover user files are expected and exempt (so are push-excluded repos). The wrap-up is **NOT complete** only if an **agent-work** path is uncommitted, a branch carrying agent commits is ahead of its remote, or an agent-work push failed → print the *WRAP-UP INCOMPLETE* block (at the bottom of this step) instead, and never claim completion.

**On success (every agent-work path committed + pushed)**, print this block:

```
Wrap-up complete (mode: [fresh / delta from CUTOFF]):

Memory update:
- Phase 1 — Promoted artifacts: project context: [updated/created — file / skipped] / reasoning: [added — pattern name / skipped] / knowledge: [added — entry name / skipped]
- Phase 2 — Session captured: [appended to / created] [filename] ([H3 timestamp]) — [brief theme]; carry-forward: [N items / N/A]; promotions: [N markers / none]
- Phase 3 — Feeling captured: emotional [captured — polarity + clearest criterion / skipped — brief reason]

Orientation map: [refreshed N entries / no-op: reason]

Push — agent work only (every agent-work path must be ✅):
- agent-memory: ✅ [commit-hash] pushed / no changes
- [project/submodule]: ✅ [commit-hash] pushed — [N user file(s) left for user (not agent's work) / no user files left]
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

**On failure (ANY agent-work path not committed + pushed)** — do NOT print "Wrap-up complete". Print this block instead:

```
🚨 WRAP-UP INCOMPLETE — UNPUSHED AGENT WORK. NEED CONFIRMATION.

[Memory update / Orientation map / Open items sections — same as above]

Push — FAILED / INCOMPLETE (agent work not fully saved):
- [repo]: ⚠️ agent-work [uncommitted N files / branch ahead by N / push error: <reason>]
- [repo]: ✅ [commit-hash] pushed

⚠️ The agent's work is NOT fully saved to the remote. What remains, and where:
- [repo → which agent-work path is uncommitted/unpushed]
(User's own uncommitted files are expected and NOT listed here — only agent work blocks completion.)

Retry the push (or resolve the blocker) before leaving — the wrap-up is only complete when every agent-work path is committed AND pushed.
```
