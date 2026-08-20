# Push Agent Memory

Commit and push changes in the agent-memory repository — either the **whole store** (`all`) or **only this agent's own memory** (`agent`).

## Arguments

`$ARGUMENTS` = `[all|agent] [message]`

- **Mode** (first token, optional): `all` (default) stages the whole agent-memory repo; `agent` stages **only the memory this agent authored this session**, leaving other agents' in-flight memory untouched (safe when multiple agents share the store concurrently).
- **Message** (remainder, optional): commit message. If omitted, auto-generate from the staged changes.
- If the first token is not literally `all` or `agent`, mode defaults to `all` and the **entire** `$ARGUMENTS` is treated as the message (backward-compatible).

Examples: `/push-memory` (all, auto-msg) · `/push-memory agent` · `/push-memory "update: reasoning patterns"` (all) · `/push-memory agent "chore: wrap-up session memory"`.

---

## Procedure

> **In-scope.** The agent-memory repo (`[AGENT-MEMORY-PATH]/`) and its owned submodules (e.g. `control-files/`). A superproject's `git status` shows a dirty submodule only as a one-line gitlink — enter each owned submodule and commit/push **inside it first**, then bump the pointer. Process submodules **before** the superproject.

### Step 1: Resolve Mode + Check for Changes

Parse `$ARGUMENTS`: first token `all`/`agent` → mode (default `all`); remainder → message. Run `git status` in the agent-memory repo (`[AGENT-MEMORY-PATH]/`). If nothing in scope is dirty AND no branch is ahead of its remote, inform the user *"No agent memory changes to push."* and stop.

### Step 2: Stage per Mode

**Mode `all`** — whole store: `git add -A` in the agent-memory repo (+ owned submodules, submodules-first).

**Mode `agent`** — only this agent's own memory. The agent-memory repo is shared across agents (`agent-<domain>/` per agent, plus `shared-memory/` and `control-files/`), so a blanket `git add -A` would sweep up a **concurrently-running agent's** uncommitted work. Stage **ONLY**:
- `agent-<my-domain>/**` — your own agent folder (the domain you awakened as).
- shared files you created/edited **this session** — under `shared-memory/**`, repo-root files, and the `control-files/` submodule — cross-check the newest episode's `Deliverables` / `Outcomes` plus your own Write/Edit history.
- 🚨 **NEVER `git add -A` in `agent` mode.** Stage your paths explicitly. Any other dirty file belongs to **another agent** (or an earlier unrelated write) — leave it untouched, report it as `left untouched (other agents)`, never commit it.
- ⚠️ **When the set is uncertain** (long or context-compacted session): do NOT silently drop a dirty file under `agent-<my-domain>/` or a shared path you may have touched. Surface the ambiguous paths and confirm before finishing — the gate catches an *unpushed* path but not an *under-inclusive* set.

### Step 3: Commit & Push (submodules before superproject)

Innermost submodule first:

1. **Stage** per Step 2 (`all` → `git add -A`; `agent` → `git add <your paths>`, never `-A`).
2. `git diff --cached --stat` to confirm. **If nothing staged AND branch not ahead** (`git status -sb` shows no `[ahead N]`), this repo/submodule is already done → skip silently.
3. Otherwise **commit** (provided message, or auto-generate — e.g. `update: episodic memories + reasoning patterns`), then **`git push`**.

> **Message style — self-contained.** Describe *what changed + why* in plain prose. Never reference plan-internal or process artifacts — decision letters (`A1`, `OQ2`), ADR numbers (`ADR-10`), or plan step/phase numbers. A `git log` reader won't have the plan open.

4. After pushing the **`control-files/` submodule**, stage + commit its updated pointer in the agent-memory superproject.
5. Treat a **non-zero `git push` exit** as a failure — carry it to Step 4.

### Step 4: Verify & Report

Run **`git status -sb`** in the repo (and each owned submodule) — the branch header surfaces `[ahead N]`, i.e. committed-but-**unpushed** work that `git status --short` hides. Done only when nothing in scope is dirty AND no branch is ahead. In `agent` mode, other agents' dirty files are expected — report, never fail.

```
Push memory (mode: [all|agent]):
- agent-memory: [pushed — commit-hash / no changes] [— agent mode: other agents' files left untouched]
- control-files: [pushed — commit-hash / no changes]
```

---
