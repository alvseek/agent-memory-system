# Short Hill Protocol

Execute quick decision-making through rapid brainstorming - generate 5-8 solution options quickly, evaluate them simply, and make a decision fast.

## Arguments

`$ARGUMENTS`

- `/short-hill [context]` → Create Short Hill quick decision plan for the given context
- `/short-hill` → Will ask for context

If no arguments provided, ask: "What decision needs quick brainstorming?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*

### Step 1: Read Template

Read the [Short Hill Plan Template](//@agent-memory/control-files/plans/short-hill-plan-template.md) file

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

Rename the copied file to `[YYYY-MM-DD]-[project]-[decision-name]-shorthill.md` pattern

### Step 6: Fill Project Info + Problem

Fill these sections:
- [Project Info](//@agent-memory/control-files/plans/short-hill-plan-template.md#project-info)
- [Problem](//@agent-memory/control-files/plans/short-hill-plan-template.md#problem)

### Step 7: Review Project Info + Problem

Ask for review. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 8: Fill Current State Analysis

Fill the [Current State Analysis](//@agent-memory/control-files/plans/short-hill-plan-template.md#current-state-analysis) section - brief analysis of what exists now

### Step 9: Review Current State Analysis

Ask for review. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 10: Fill Quick Solution Generation

Fill the [Quick Solution Generation](//@agent-memory/control-files/plans/short-hill-plan-template.md#quick-solution-generation) section - use ONE rapid technique to generate 5-8 solution options

### Step 11: Review Generated Solutions

Ask for review and if user needs more options. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 12: Fill Quick Evaluation

Fill the [Quick Evaluation](//@agent-memory/control-files/plans/short-hill-plan-template.md#quick-evaluation) section - simple Pros/Cons comparison of the 5-8 options

### Step 13: Review Evaluation + Offer Multi-Agent Voting

Ask for review, AND proactively ask: "Do you want multi-agent voting? (5 AI agents vote independently to reduce bias - optional but recommended for important decisions)". STOP. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

- **If YES to multi-agent voting**, execute steps 13a-13d:
  - 13a. Fill my own Quick Evaluation assessment + vote for one option, add "### Evaluator 1: [Agent Name] ([Model])" section with my assessment and vote
  - 13b. Spawn 4 Haiku agents in parallel using Task tool with `model: "haiku"`: each agent reads the Short Hill document, independently evaluates all options, adds their assessment in "### Evaluator [2-5]: Haiku Agent [1-4]" section, and votes for one option
  - 13c. After all agents complete, update the Vote Summary table with all 5 votes
  - 13d. Calculate Final Tally and present results to Alvi for review before moving to Selected Solution
- **If NO to multi-agent voting**, proceed directly to step 14

### Step 14: Fill Selected Solution

Fill the [Selected Solution](//@agent-memory/control-files/plans/short-hill-plan-template.md#selected-solution) section with decision and rationale

### Step 15: Review Selected Solution

Ask for review. STOP. Present to Alvi for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 16: Create ADR Folder and Copy Template

Create the Architecture Decision Record (ADR) document in `/docs/adr/` folder:
- Check if `/docs/adr/` folder exists, if not create it:
  - **Windows**: `powershell -c "New-Item -ItemType Directory -Path './docs/adr' -Force"`
  - **Linux/macOS**: `mkdir -p ./docs/adr`
- Copy the [ADR Template](//@agent-memory/control-files/plans/adr-template.md) to `/docs/adr/`:
  - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
  - **Linux/macOS**: `cp {source} {target}`
- Rename following pattern: `[YYYY-MM-DD]-[short-descriptive-title].md`
- Determine ADR number by checking existing ADR files and using next sequential number

### Step 17: Fill ADR Document

Fill the ADR document sections:
- ADR number, title, date, and status (Accepted)
- **Problem** section - clear 2-3 sentence problem statement
- **Decision** section - what we decided, how it addresses problem, 3 key reasons why
- **What to Build (Requirements)** section - core requirements and success criteria
- **Alternatives Rejected** section - the 1-2 other options with brief rejection reasons
- **Full brainstorming context** link to the Short Hill plan file

### Step 18: Review ADR

Ask Alvi to review the ADR document. STOP. Do NOT proceed until confirmed to avoid rework when ADR need adjustment.

### Step 19: Present Documents

Present both documents to Alvi:
- Quick brainstorming document: `/plans/[date]-[project]-[decision]-shorthill.md`
- Decision summary (ADR): `/docs/adr/[date]-[title].md`

### Step 20: Inform Next Steps

Inform Alvi that the ADR document should be used as "Related Documents" reference when continuing the main implementation plan (Shallow Shore/Deep Trench/Quick Surf)

---
