# Wide Ocean Protocol

Execute master coordination when a feature requires 3-5 separate sub-plans - the "conductor's score" that orchestrates multiple protocol plans (Deep Trench, Shallow Shore, Quick Surf, etc.) into a cohesive feature delivery.

## Arguments

`$ARGUMENTS`

- `/wide-ocean [context]` → Create Wide Ocean master coordination plan for the given feature
- `/wide-ocean` → Will ask for context

If no arguments provided, ask: "What feature needs multi-plan coordination?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited.*

### Step 1: Read Template

Read the [Wide Ocean Plan Template](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md) file

### Step 2: Create Feature Folder

Create plan folder with naming: `plans/[YYYY-MM-DD]-[feature-name]/`
- Get current date:
  - **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd'"`
  - **Linux/macOS**: `date '+%Y-%m-%d'`
- Create folder:
  - **Windows**: `powershell -c "New-Item -ItemType Directory -Force -Path 'plans/[YYYY-MM-DD]-[feature-name]'"`
  - **Linux/macOS**: `mkdir -p plans/[YYYY-MM-DD]-[feature-name]`

### Step 3: Copy Template

Copy the template file to the new folder as `master.md`:
- **Windows**: `powershell -c "Copy-Item {source} -Destination {target}/master.md -Force"`
- **Linux/macOS**: `cp {source} {target}/master.md`

### Step 4: Fill Feature Info

Fill the [Feature Info](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#feature-info) section

### Step 5: Fill Objectives and Success Criteria

Fill the [Objectives and Success Criteria](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#objectives) section

### Step 6: Investigate and Fill Analysis

Investigate the codebase and fill the [Analysis](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#analysis) section

### Step 7: Review Feature Info + Objectives + Analysis

Ask for review. STOP. Present to [USER-NAME] for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 8: Fill Sub-Plans Listing

Fill the [Sub-Plans Listing](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#sub-plans-listing) section

### Step 9: Review Sub-Plans

Ask for review. STOP. Present to [USER-NAME] for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 10: Fill Execution Order

Fill the [Execution Order](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#execution-order) section

### Step 11: Fill Dependency Graph

Fill the [Dependency Graph](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#dependency-graph) section

### Step 12: Review Execution Order + Dependency Graph

Ask for review. STOP. Present to [USER-NAME] for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 13: Fill Integration Points

Fill the [Integration Points](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#integration-points) section

### Step 14: Fill Handoff Checklists

Fill the [Handoff Checklists](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#handoff-checklists) section

### Step 15: Fill Agent Assignment Matrix

Fill the [Agent Assignment Matrix](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#agent-assignment-matrix) section

### Step 16: Review Integration + Handoffs + Agent Assignment

Ask for review. STOP. Present to [USER-NAME] for review. Do NOT write the next section until confirmed to avoid cascading changes when this section need adjustment.

### Step 17: Fill Related Documents

Fill the [Related Documents](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#related-documents) section

### Step 18: Fill Notes & Decisions Log

Fill the [Notes & Decisions Log](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#notes--decisions-log) section

### Step 19: Fill Status Tracking

Fill the [Status Tracking](//@agent-memory/control-files/plan-templates/wide-ocean-plan-template.md#status-tracking) section (mirror Sub-Plans with NOT STARTED status)

### Step 20: Self Final Review

Do a self final review by thinking critically, very hard and very carefully:
- a. Are all sub-plans necessary? Any missing?
- b. Is the execution order correct? Any dependency issues?
- c. Are handoff checklists complete for each transition?
- d. Are agent assignments appropriate?
- e. Is there anything conflicting or redundant?

### Step 21: Present Master Plan

Present the complete master plan to [USER-NAME] with self-review findings. STOP. Do NOT proceed until confirmed to avoid rework when master plan need adjustment.

### Step 22: Ready for Sub-Plan Execution

After confirmation, the master plan is ready. Sub-plans will be created and executed using their respective protocols (Deep Trench, Shallow Shore, etc.)

---

## Templates

### Execution Workflow (After Master Plan Approved)

When executing sub-plans:
1. Check STATUS TRACKING for next `NOT STARTED` plan
2. Create sub-plan file using appropriate protocol (Deep Trench, Shallow Shore, etc.)
3. Execute sub-plan using its own protocol
4. After sub-plan completion, update master plan:
   - STATUS TRACKING: Set status to `DONE`, progress to `100%`
   - Complete relevant HANDOFF CHECKLIST
   - Update PHASE SUMMARY if phase complete
5. Repeat until all sub-plans are `DONE`
6. Complete FEATURE COMPLETION CHECKLIST
7. Set Feature Status to `DONE`

---
