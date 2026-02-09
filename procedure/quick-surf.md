# Quick Surf Protocol

Execute scope validation and implementation step logging when both objectives AND solution are clear.

## Arguments

`$ARGUMENTS`

- `/quick-surf [context]` → Create Quick Surf plan for the given context
- `/quick-surf` → Will ask for context

If no arguments provided, ask: "What feature or task should I create a Quick Surf plan for?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*

### Step 1: Read Template

Read the [Quick Surf Plan Template](//@claude-agents/control-files/plans/quick-surf-plan-template.md) file

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
- [Project Info](//@claude-agents/control-files/plans/quick-surf-plan-template.md#project-info)
- [Objective and Success Criteria](//@claude-agents/control-files/plans/quick-surf-plan-template.md#-objective)
- [Analysis](//@claude-agents/control-files/plans/quick-surf-plan-template.md#analysis)
- [Solution](//@claude-agents/control-files/plans/quick-surf-plan-template.md#solution)

### Step 7: Review Core Sections

Ask for review of project info, objective, analysis, and solution sections. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 8: Fill Implementation Phases

Fill the [Implementation Phases](//@claude-agents/control-files/plans/quick-surf-plan-template.md#implementation-phases) section

### Step 9: Review Implementation Phases

Ask for review of implementation phases. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 10: Self Final Review

Do a self final review by thinking critically, very hard and very carefully, as if this is another person's work:
- a. Is there anything missing that should be in scope?
- b. Is there anything in implementation that actually should be out of scope?
- c. Is there anything that needs to be detailed further to avoid confusion?
- d. Is there anything that is conflicting within the plan?
- e. Is there anything that is redundant in the plan?
- f. Is there anything in implementation phase that is not in order and should be reordered?

### Step 11: Present Self Review

Present the self final review to Alvi. STOP. Do NOT create the log file until confirmed to avoid rework when review findings need adjustment.

### Step 12: Fill Anchor Links

Fill the `{add reference to the original Step *.* plan section using anchor link}` placeholder for each substep in the log file

### Step 13: Present Log File

Present the Implementation Log file link to Alvi and wait for instruction

### Step 14: Start Implementation

After Alvi instructs to start implementing, start implementing following the **Execution Protocol for AI** from the newly created plan file

---
