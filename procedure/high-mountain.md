# High Mountain Protocol

Execute systematic creative problem-solving through structured brainstorming using multiple techniques (5 Whys, SCAMPER, Mind Mapping) and converge on the best solution through evaluation frameworks.

## Arguments

`$ARGUMENTS`

- `/high-mountain [context]` → Create High Mountain brainstorming plan for the given context
- `/high-mountain` → Will ask for context

If no arguments provided, ask: "What problem or decision needs creative brainstorming?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*

### Step 1: Read Template

Read the [High Mountain Plan Template](//@claude-agents/control-files/plans/high-mountain-plan-template.md) file

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

### Step 6: Fill Project Info + Problem Statement

Fill these sections:
- [Project Info](//@claude-agents/control-files/plans/high-mountain-plan-template.md#project-info)
- [Problem Statement](//@claude-agents/control-files/plans/high-mountain-plan-template.md#problem-statement)

### Step 7: Review Project Info + Problem Statement

Ask for review. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 8: Fill Problem Analysis

Fill the [Problem Analysis](//@claude-agents/control-files/plans/high-mountain-plan-template.md#problem-analysis) section including root cause exploration using 5 Whys technique

### Step 9: Review Problem Analysis

Ask for review. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 10: Fill Divergent Thinking Phase

Fill the [Divergent Thinking Phase](//@claude-agents/control-files/plans/high-mountain-plan-template.md#divergent-thinking-phase) section using multiple brainstorming techniques (SCAMPER, Mind Mapping, Reverse Brainstorming, etc.) to generate creative solutions

### Step 11: Review Divergent Thinking

Ask for review. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 12: Fill Convergent Thinking Phase

Fill the [Convergent Thinking Phase](//@claude-agents/control-files/plans/high-mountain-plan-template.md#convergent-thinking-phase) section evaluating and prioritizing the generated solutions

### Step 13: Review Convergent Thinking

Ask for review. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 14: Fill Selected Solution

Fill the [Selected Solution](//@claude-agents/control-files/plans/high-mountain-plan-template.md#selected-solution) section with clear rationale and technical design

### Step 15: Review Selected Solution

Ask for review. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 16: Self Final Review

Do a self final review by thinking critically, very hard and very carefully:
- a. Is the problem clearly defined and root cause identified?
- b. Did we explore enough creative solutions using multiple techniques?
- c. Is the evaluation framework clear and objective?
- d. Is the selected solution justified with clear rationale?
- e. Are there any gaps in the brainstorming or evaluation process?
- f. Is the decision rationale comprehensive and evidence-based?

### Step 17: Present Self Review

Present the self final review to Alvi. STOP. Do NOT create the ADR until confirmed to avoid rework when review findings need adjustment.

### Step 18: Create ADR Folder and Copy Template

Create the Architecture Decision Record (ADR) document in `/docs/adr/` folder:
- Check if `/docs/adr/` folder exists, if not create it:
  - **Windows**: `powershell -c "New-Item -ItemType Directory -Path './docs/adr' -Force"`
  - **Linux/macOS**: `mkdir -p ./docs/adr`
- Copy the [ADR Template](//@claude-agents/control-files/plans/adr-template.md) to `/docs/adr/`:
  - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
  - **Linux/macOS**: `cp {source} {target}`
- Rename following pattern: `[YYYY-MM-DD]-[short-descriptive-title].md`
- Determine ADR number by checking existing ADR files and using next sequential number

### Step 19: Fill ADR Document

Fill the ADR document sections:
- ADR number, title, date, and status (Accepted)
- **Problem** section - clear 2-3 sentence problem statement
- **Decision** section - what we decided, how it addresses problem, 3 key reasons why
- **What to Build (Requirements)** section - core requirements and success criteria
- **Alternatives Rejected** section - top 3 alternatives with brief rejection reasons
- **Full brainstorming context** link to the High Mountain plan file

### Step 20: Review ADR

Ask Alvi to review the ADR document. STOP. Do NOT proceed until confirmed to avoid rework when ADR need adjustment.

### Step 21: Present Documents

Present both documents to Alvi:
- Full brainstorming document: `/plans/[date]-[project]-[theme]-brainstorm.md`
- Decision summary (ADR): `/docs/adr/[date]-[title].md`

### Step 22: Inform Next Steps

Inform Alvi that the ADR document should be used as "Related Documents" reference when creating implementation plans with Deep Trench/Shallow Shore/Quick Surf protocols

---
