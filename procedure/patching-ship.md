# Patching Ship Protocol

Execute systematic bug investigation and root cause analysis through structured debugging workflow - analyze bugs comprehensively using platform scaffolding checks, issue replication, root cause investigation, and solution synthesis.

## Arguments

`$ARGUMENTS`

- `/patching-ship [context]` → Create Patching Ship comprehensive bug investigation plan for the given context
- `/patching-ship` → Will ask for context

If no arguments provided, ask: "What bug needs comprehensive investigation?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*

### Step 1: Read Template

Read the [Patching Ship Plan Template](//@agent-memory/control-files/plans/patching-ship-plan-template.md) file

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

Rename the copied file to `[YYYY-MM-DD]-[project]-[bug-theme]-debug.md` pattern

### Step 6: Fill Project Info + Bug Analysis

Fill these sections:
- [Project Info](//@agent-memory/control-files/plans/patching-ship-plan-template.md#project-info)
- [Bug Analysis & Context](//@agent-memory/control-files/plans/patching-ship-plan-template.md#bug-analysis--context)

### Step 7: Review Project Info + Bug Analysis

Ask for review. STOP. Present to [USER-NAME] for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 8: Fill Platform Scaffolding Check

Fill the [Platform Scaffolding Check](//@agent-memory/control-files/plans/patching-ship-plan-template.md#platform-scaffolding-check) section including verification of log locations, debug logging capabilities, database access, monitoring tools, and diagnostic access

### Step 9: Review Platform Scaffolding Check

Ask for review. STOP. Present to [USER-NAME] for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 10: Fill Issue Replication

Fill the [Issue Replication](//@agent-memory/control-files/plans/patching-ship-plan-template.md#issue-replication) section with detailed reproduction steps, test environment setup, success criteria for reproduction, and edge case identification

### Step 11: Review Issue Replication

Ask for review. STOP. Present to [USER-NAME] for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 12: Fill Bug Location

Fill the [Bug Location](//@agent-memory/control-files/plans/patching-ship-plan-template.md#bug-location) section - identify the ACTUAL code producing the bug symptom (factual based on stack traces, logs, or debugger - NOT a guess)

### Step 13: Review Bug Location

Ask for review. STOP. Present to [USER-NAME] for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 14: Fill Root Cause Investigation

Fill the [Root Cause Investigation](//@agent-memory/control-files/plans/patching-ship-plan-template.md#root-cause-investigation) section using the hypothesis-driven process:
- Fill Log Analysis, Code Flow Analysis, and Database State Examination first (data gathering)
- Then fill [Hypothesis & Testing](//@agent-memory/control-files/plans/patching-ship-plan-template.md#4-hypothesis--testing) section SEQUENTIALLY:
  - Create Hypothesis 1 → Test it → Confirmed? → Fill Root Cause Conclusion / Rejected? → Create Hypothesis 2
  - Repeat until hypothesis confirmed
- Fill [Root Cause Conclusion](//@agent-memory/control-files/plans/patching-ship-plan-template.md#root-cause-conclusion) ONLY after a hypothesis is confirmed

### Step 15: Review Root Cause Investigation

Ask for review. STOP. Present to [USER-NAME] for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 16: Fill Solution Synthesis

Fill the [Solution Synthesis](//@agent-memory/control-files/plans/patching-ship-plan-template.md#solution-synthesis) section evaluating fix approach options (quick patch vs proper fix), risk assessment, testing strategy, and rollback plan

### Step 17: Review Solution Synthesis

Ask for review. STOP. Present to [USER-NAME] for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 18: Fill Selected Fix

Fill the [Selected Fix](//@agent-memory/control-files/plans/patching-ship-plan-template.md#selected-fix) section with clear rationale, technical implementation details, and implementation phases

### Step 19: Review Selected Fix

Ask for review. STOP. Present to [USER-NAME] for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 20: Self Final Review

Do a self final review by thinking critically, very hard and very carefully:
- a. Is the bug clearly described with impact assessment?
- b. Did we verify all platform scaffolding is accessible (logs, debug, database)?
- c. Can we reliably reproduce the issue with documented steps?
- d. Did we identify the ACTUAL bug location (factual, not a guess)?
- e. Did we test hypotheses sequentially before declaring root cause?
- f. Is the root cause confirmed by evidence from hypothesis testing (not assumed)?
- g. Did we evaluate multiple fix approaches with proper risk assessment?
- h. Is the selected fix justified with clear rationale and rollback plan?
- i. Are implementation phases clear and executable?

### Step 21: Present Self Review

Present the self final review to [USER-NAME]. STOP. Do NOT proceed until confirmed to avoid rework when review findings need adjustment.

### Step 22: Present Document

Present the completed bug investigation and fix plan document to [USER-NAME]: `/plans/[date]-[project]-[bug-theme]-debug.md`

---
