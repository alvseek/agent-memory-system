# Fixing Rod Protocol

Execute quick straightforward bug fixes where the root cause is obvious and the fix is simple - streamlined for speed while maintaining quality.

## Arguments

`$ARGUMENTS`

- `/fixing-rod [context]` → Create Fixing Rod quick bug fix plan for the given context
- `/fixing-rod` → Will ask for context

If no arguments provided, ask: "What bug needs a quick fix?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*

### Step 1: Read Template

Read the [Fixing Rod Plan Template](//@agent-memory/control-files/plans/fixing-rod-plan-template.md) file

### Step 2: Create Plans Folder

Create `/plans` folder in the project root level (if it doesn't exist)

### Step 3: Copy Template

Copy the template file to the `/plans` folder:
- **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
- **Linux/macOS**: `cp {source} {target}`

### Step 4: Check Date

Get current date for file naming:
- **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
- **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`

### Step 5: Rename File

Rename the copied file to `[YYYY-MM-DD]-[project]-[bug-theme]-fix.md` pattern

### Step 6: Fill Sections (Hypothesis-Driven)

Fill sections in order following the hypothesis-driven process:
- [Bug Info](//@agent-memory/control-files/plans/fixing-rod-plan-template.md#bug-info) - What's broken, where, and impact
- [Quick Scaffolding Check](//@agent-memory/control-files/plans/fixing-rod-plan-template.md#quick-scaffolding-check) - Verify debugging access
- [Bug Location](//@agent-memory/control-files/plans/fixing-rod-plan-template.md#bug-location) - Find the ACTUAL code producing the bug symptom (factual, not a guess)
- [Hypothesis & Testing](//@agent-memory/control-files/plans/fixing-rod-plan-template.md#hypothesis--testing) - Sequential hypothesis testing:
  - Create Hypothesis 1 → Test it → Confirmed? → Fill Root Cause / Rejected? → Create Hypothesis 2
  - Repeat until hypothesis confirmed or escalate to Patching Ship after 3 failed hypotheses
- [Root Cause](//@agent-memory/control-files/plans/fixing-rod-plan-template.md#root-cause) - Fill ONLY after hypothesis is confirmed
- [Fix Solution](//@agent-memory/control-files/plans/fixing-rod-plan-template.md#fix-solution) - What to change and why it fixes the root cause
- [Implementation Phases](//@agent-memory/control-files/plans/fixing-rod-plan-template.md#implementation-phases) - Step-by-step fix implementation
- [Testing Checklist](//@agent-memory/control-files/plans/fixing-rod-plan-template.md#testing-checklist) - Verify fix works

### Step 7: Quick Self Review

Do a quick self review by asking:
- a. Is the bug clearly described with location identified?
- b. Did I verify access to logs, config, and test environment?
- c. Did I locate the actual code producing the bug symptom (not just a guess)?
- d. Did I test my hypothesis before declaring root cause?
- e. Is the root cause confirmed by evidence (not assumed)?
- f. Does the fix solution address the confirmed root cause?
- g. Are implementation phases clear?
- h. Is testing adequate?

### Step 8: Review Plan

Present the quick fix plan to [USER-NAME] for review and confirmation

### Step 9: Present Document

Present the completed quick fix plan document to [USER-NAME]: `/plans/[date]-[project]-[bug-theme]-fix.md`

---
