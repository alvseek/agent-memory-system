# Shallow Shore Protocol

Execute iterative planning when solution is NOT clear yet but objectives ARE clear - explore and design solutions through iterative analysis.

## Arguments

`$ARGUMENTS`

- `/shallow-shore [context]` → Create Shallow Shore plan for the given context
- `/shallow-shore` → Will ask for context

If no arguments provided, ask: "What feature or task should I create a Shallow Shore plan for?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*

### Step 1: Read Template

Read the [Shallow Shore Plan Template](//@agent-memory/control-files/plans/shallow-shore-plan-template.md) file

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

Rename the copied file to `[YYYY-MM-DD]-[project]-[theme].md` pattern

### Step 6: Fill Core Sections

Fill these sections:
- [Project Info](//@agent-memory/control-files/plans/shallow-shore-plan-template.md#project-info)
- [Objective and Success Criteria](//@agent-memory/control-files/plans/shallow-shore-plan-template.md#-objective)
- [Analysis](//@agent-memory/control-files/plans/shallow-shore-plan-template.md#analysis)

### Step 7: Review Core Sections

Ask for review of project info, objective, and analysis. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 8: Fill Solution

Fill the [Solution](//@agent-memory/control-files/plans/shallow-shore-plan-template.md#solution) section

### Step 9: Review Solution

Ask for review of solution section. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 10: Fill Implementation Phases

Fill the [Implementation Phases](//@agent-memory/control-files/plans/shallow-shore-plan-template.md#implementation-phases) section

### Step 11: Review Implementation Phases

Ask for review of implementation phases. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 12: Self Final Review

Do a self final review by thinking critically, very hard and very carefully, as if this is another person's work:
- a. Is there anything missing that should be in scope?
- b. Is there anything in implementation that actually should be out of scope?
- c. Is there anything that needs to be detailed further to avoid confusion?
- d. Is there anything that is conflicting within the plan?
- e. Is there anything that is redundant in the plan?
- f. Is there anything in implementation phase that is not in order and should be reordered?

### Step 13: Present Self Review

Present the self final review to Alvi. STOP. Do NOT create the log file until confirmed to avoid rework when review findings need adjustment.

### Step 14: Copy Implementation Log Template

Copy the [Implementation Log Template](//@agent-memory/control-files/plans/implementation-log-template.md) to the `/plans` folder, named like the plan file but with '-log' suffix:
- **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
- **Linux/macOS**: `cp {source} {target}`
- Example plan file: `/plans/2025-10-12-simple-bug-fix.md`
- Example log file: `/plans/2025-10-12-simple-bug-fix-log.md`

### Step 15: Fill Plan File Reference

Fill the **Plan File** placeholder with the original plan file anchor link in the implementation log file

### Step 16: Choose Log Placeholder

Choose the [Shallow Shore Log Placeholder](//@agent-memory/control-files/plans/shallow-shore-log-placeholder.md) in the **Execution Protocol for AI** section and remove the others

### Step 17: Fill Anchor Links

Fill the `{add reference to the original Step *.* plan section using anchor link}` placeholder for each substep

### Step 18: Present Log File

Present the Implementation Log file link to Alvi and wait for instruction

### Step 19: Start Implementation

After Alvi instructs to start implementing, start implementing following the **Execution Protocol for AI** in the newly created Implementation Log file

---
