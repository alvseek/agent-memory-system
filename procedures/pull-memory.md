# Pull Agent Memory

Pull the latest changes for the agent-memory repository and update the control-files submodule.

## Arguments

`$ARGUMENTS`

- `/pull-memory` → Pull agent memory + update control-files submodule

---

## Procedure

### Step 1: Pull Agent Memory

1. Run `git pull` in the agent-memory repo (`[AGENT-MEMORY-PATH]/`)
2. Report result: "Agent memory pulled: [result summary]"

If pull fails (e.g., merge conflict), report the error and stop.

### Step 2: Update All of Its Submodule

1. Run `git submodule update --remote --merge` in the repo
2. Report result: "Submodules updated: [result summary]"

If submodule update fails (e.g., merge conflict), report the error.

---
