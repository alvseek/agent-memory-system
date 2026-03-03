# Wrap Up Session

End-of-session orchestrator: save episodic memory, optionally capture project context, then commit and push everything.

## Arguments

`$ARGUMENTS`

- `/wrap-up` → Fire-and-forget session wrap-up (all steps automatic)

---

## Procedure

### Step 1: Save Episodic Memory

Execute the [Update Episodic Protocol](//@agent-memory/control-files/procedures/memory/update-episodic.md) using default mode (update existing episode, or create new if theme is unrelated).

### Step 2: Evaluate Project Context

Auto-evaluate whether this session produced **project-specific context** worth preserving for future sessions. Ask yourself:

- Were there project-specific conventions, setup steps, deployment procedures, or environment details discussed?
- Were there workarounds, configurations, or technical decisions specific to the current project?
- Were there new access credentials, URLs, API endpoints, or infrastructure details shared?

**If yes**: Execute the [Update Project Context Protocol](//@agent-memory/control-files/procedures/memory/update-project-context.md) with the relevant context. No user prompt needed — auto-detect the theme and create/update the file.

**If no**: Skip silently.

### Step 3: Push Everything

Execute the [Push All Protocol](//@agent-memory/control-files/procedures/push-all.md) to commit and push both the current project and agent-memory repositories.

### Step 4: Summary

Report what was done:
```
Wrap-up complete:
  - Episodic memory: [updated/created] — [episode file name]
  - Project context: [updated/created/skipped] — [file name if applicable]
  - Push: [project: pushed/no changes] [agent memory: pushed/no changes]
```

---
