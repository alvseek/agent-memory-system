# Deep Trench Protocol

Execute comprehensive planning when objectives are NOT clear yet - discover and clarify objectives through systematic analysis.

## Arguments

`$ARGUMENTS`

- `/deep-trench [context]` → Create Deep Trench plan for the given context
- `/deep-trench` → Will ask for context

If no arguments provided, ask: "What feature or task should I create a Deep Trench plan for?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*

### Step 1: Read Template

Read the [Deep Trench Plan Template](//@agent-memory/control-files/plans/deep-trench-plan-template.md) file

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

### Step 6: Fill Project Info + Objective

Fill these sections:
- [Project Info](//@agent-memory/control-files/plans/deep-trench-plan-template.md#project-info)
- [Objective and Success Criteria](//@agent-memory/control-files/plans/deep-trench-plan-template.md#-objective)

### Step 7: Review Project Info + Objective

Ask for review of project info and objective. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 8: Fill Analysis

Fill the [Analysis](//@agent-memory/control-files/plans/deep-trench-plan-template.md#analysis) section

### Step 9: Review Analysis

Ask for review of analysis section. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 10: Fill Solution

Fill the [Solution](//@agent-memory/control-files/plans/deep-trench-plan-template.md#solution) section

### Step 11: Review Solution

Ask for review of solution section. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 12: Fill Implementation Phases

Fill the [Implementation Phases](//@agent-memory/control-files/plans/deep-trench-plan-template.md#implementation-phases) section

### Step 13: Review Implementation Phases

Ask for review of implementation phases. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 14: Self Final Review

Do a self final review by thinking critically, very hard and very carefully, as if this is another person's work:
- a. Is there anything missing that should be in scope?
- b. Is there anything that is actually should be out of scope?
- c. Is there anything that needs to be detailed further to avoid confusion?
- d. Is there anything that is conflicting within the plan?
- e. Is there anything that is redundant in the plan?
- f. Is there anything in implementation phase that is not in order and should be reordered?

### Step 15: Present Self Review

Present the self final review to Alvi. STOP. Do NOT create the log file until confirmed to avoid rework when review findings need adjustment.

### Step 16: Copy Implementation Log Template

Copy the [Implementation Log Template](//@agent-memory/control-files/plans/implementation-log-template.md) to the `/plans` folder, named like the plan file but with '-log' suffix:
- **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
- **Linux/macOS**: `cp {source} {target}`
- Example plan file: `/plans/2025-10-06-ocx-new-catalog-feature.md`
- Example log file: `/plans/2025-10-06-ocx-new-catalog-feature-log.md`

### Step 17: Fill Plan File Reference

Fill the **Plan File** placeholder with the original plan file anchor link in the implementation log file

### Step 18: Choose Log Placeholder

Choose the [Deep Trench Log Placeholder](//@agent-memory/control-files/plans/deep-trench-log-placeholder.md) in the **Execution Protocol for AI** section and remove the others

### Step 19: Fill Anchor Links

Fill the `{add reference to the original Step *.* plan section using anchor link}` placeholder for each substep

### Step 20: Present Log File

Present the Implementation Log file link to Alvi and wait for instruction

### Step 21: Start Implementation

After Alvi instructs to start implementing, start implementing following the **Execution Protocol for AI** in the newly created Implementation Log file

---
