# High Wizard Protocol

Execute smart planning with structural decision collection - forces "ask before assuming" by collecting ALL implementation decisions upfront with recommended defaults before writing any plan content.

## Arguments

`$ARGUMENTS`

- `/high-wizard [context]` → Create High Wizard plan for the given context
- `/high-wizard` → Will ask for context

If no arguments provided, ask: "What feature or task should I create a High Wizard plan for?"

---

## Procedure

*IMPORTANT: This procedure structurally enforces UUID f3a8b2c1 (VERIFY FIRST) - the agent MUST collect and confirm decisions BEFORE writing any plan sections. Writing ahead on assumptions is prohibited.*

### Step 1: Read Template

Read the [High Wizard Plan Template](//@claude-agents/control-files/plans/high-wizard-plan-template.md) file

### Step 2: Check Date

Get current date for file naming:
- **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
- **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`

### Step 3: Copy Template

Copy the template file to the `/plans` folder with the final name:
- **Windows**: `powershell -c "Copy-Item {source} -Destination ./plans/[YYYY-MM-DD]-[project]-[theme].md -Force"`
- **Linux/macOS**: `cp {source} ./plans/[YYYY-MM-DD]-[project]-[theme].md`

### Step 4: Fill Project Info

Fill the [Project Info](//@claude-agents/control-files/plans/high-wizard-plan-template.md#project-info) section only (Project, Date, Agent, Theme)

### Step 5: Investigate and Collect Decisions

This is where the thinking happens - NOT in the plan document. Follow the investigation checklist below IN ORDER. Each step from 3-6 produces decision items for the decision form.

**Decision format** - For each decision found:
- Provide 2-4 options
- Mark recommended default with confidence signal: `✓✓` (strong, clear evidence) or `✓?` (uncertain, genuine tradeoff)
- Include a **meaningful reason** that serves as the analysis record

**Investigation checklist (in order):**

1. **Requirements clarity** - Is the intent already clear? Is there ambiguity within the context? If ambiguous, create decisions to clarify before proceeding
2. **Codebase scan** - Scan relevant files, modules, and architecture related to the task to understand current state
3. **Alternative approaches** - Based on the requirement, discover what ways this can be done (there's usually more than one) → offer as decisions
4. **Reusable components** - Identify existing functions, utilities, patterns that could be leveraged → offer to reuse the related/reusable ones as decisions
5. **Conflicts and constraints** - Note what could go wrong, what limits exist → if any, offer options based on pros and cons as decisions
6. **Integration points** - Check what existing code/systems will be affected → if concerning, offer options as decisions

Order collected decisions by dependency (foundational choices first, dependent ones after).

### Step 7: Present Decisions

Present the decision form to Alvi. STOP. Present to Alvi for review. Do NOT write any plan sections until decisions are confirmed.

**Response format:**
```
I've investigated the codebase. Here are the decisions I need before planning:

1. [Decision topic]:  [A) Option ✓✓]  B) Option  C) Option  (reason with evidence)
2. [Decision topic]:  [A) Option ✓?]   B) Option             (reason explaining uncertainty)
3. ...

Reply with changes (e.g., "change 2 to B") or "let's proceed" to accept all defaults.
```

If Alvi changes a foundational decision that affects downstream decisions, re-evaluate and re-present affected decisions.

### Step 8: Fill Objectives + Success Criteria

Fill the [Objectives](//@claude-agents/control-files/plans/high-wizard-plan-template.md#objectives) and [Success Criteria](//@claude-agents/control-files/plans/high-wizard-plan-template.md#success-criteria) sections

### Step 9: Fill Scope

Fill the [Scope](//@claude-agents/control-files/plans/high-wizard-plan-template.md#scope) section (In Scope / Out of Scope)

### Step 10: Fill Confirmed Decisions

Record all confirmed decisions (with any changes Alvi made) in the [Confirmed Decisions](//@claude-agents/control-files/plans/high-wizard-plan-template.md#confirmed-decisions) section. Include the meaningful reasons - this IS the analysis record.

### Step 11: Early Review

Present objectives, scope, and confirmed decisions to Alvi. STOP. Present to Alvi for review. Do NOT write the solution until confirmed to avoid cascading changes when this section need adjustment.

### Step 12: Fill Solution

Fill the [Solution](//@claude-agents/control-files/plans/high-wizard-plan-template.md#solution) section. Build directly from confirmed decisions.

**CRITICAL**: If any NEW decision is discovered during writing that was not covered in Step 7, STOP immediately. Present the new decision to Alvi with the same format (options + confidence + reason) before continuing. Do NOT write ahead on assumptions.

### Step 13: Fill Implementation Phases

Fill the [Implementation Phases](//@claude-agents/control-files/plans/high-wizard-plan-template.md#implementation-phases) section.

**CRITICAL**: Same rule - if any NEW decision is discovered during writing, STOP immediately and present it before continuing.

### Step 14: Silent Self-Review

Do a self-review internally by thinking critically:
- a. Is there anything missing that should be in scope?
- b. Is there anything that should be out of scope?
- c. Is there any conflict between confirmed decisions and the solution/implementation?
- d. Is there anything redundant?
- e. Are implementation phases in the right order?

**Only present findings to Alvi if actual issues are found.** If no issues, proceed silently to Step 15.

### Step 15: Final Review

Before presenting the plan, double check: are there any unresolved decisions, assumptions, or new concerns that surfaced during writing (Steps 12-13) or self-review (Step 14) that need Alvi's input? If yes, present them now with the same decision format (options + confidence + reason).

Present the complete plan file link to Alvi for final review. STOP. Wait for instruction.

### Step 16: Start Implementation

After Alvi instructs to start implementing, start implementing following the **Execution Protocol for AI** from the plan file.

---
