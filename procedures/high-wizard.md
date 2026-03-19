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

Read the [High Wizard Plan Template](//@agent-memory/control-files/plan-templates/high-wizard-plan-template.md) file

### Step 2: Check Date

Get current date for file naming:
`date '+%Y-%m-%d %H:%M'`

### Step 3: Copy Template

Copy the template file to the `/plans` folder with the final name:
`cp {source} ./plans/[YYYY-MM-DD]-[project]-[theme].md`

### Step 4: Fill Project Info

Fill the [Project Info](//@agent-memory/control-files/plan-templates/high-wizard-plan-template.md#project-info) section only (Project, Date, Agent, Theme)

### Step 5: Investigate and Collect Decisions

This is where the thinking happens - NOT in the plan document. Follow the investigation checklist below IN ORDER. Each step from 3-6 produces decision items for the WAIT Options form.

**WAIT Options format** (What Am I Thinking? Options) - For each decision found:
- Provide 2-4 options
- Mark recommended default with confidence signal: `✓✓` (strong, clear evidence) or `✓?` (uncertain, genuine tradeoff)
- Include a **meaningful reason** that serves as the analysis record
- If any questions remain that don't fit into options format, collect them as **named open questions** (OQ1, OQ2, ...) to present alongside decisions

**Investigation checklist (in order):**

1. **Requirements clarity** - Is the intent already clear? Is there ambiguity within the context? If ambiguous, create decisions to clarify before proceeding
2. **Codebase scan** - Scan relevant files, modules, and architecture related to the task to understand current state
3. **Alternative approaches** - Based on the requirement, discover what ways this can be done (there's usually more than one) → offer as decisions
4. **Reusable components** - Identify existing functions, utilities, patterns that could be leveraged → offer to reuse the related/reusable ones as decisions
5. **Conflicts and constraints** - Note what could go wrong, what limits exist → if any, offer options based on pros and cons as decisions
6. **Integration points** - Check what existing code/systems will be affected → if concerning, offer options as decisions
7. **Quality standard discovery** - Search for `quality-standard.md` in the project via glob (`**/quality-standard.md`). If found, load it as additional implementation criteria to reference when writing plan steps. If not found, note it and proceed

Order collected decisions by dependency (foundational choices first, dependent ones after).

### Step 7: Present WAIT Options

Present the WAIT Options form to [USER-NAME]. STOP. Present to [USER-NAME] for review. Do NOT write any plan sections until decisions are confirmed.

**Response format:**
```
I've investigated the codebase. Here are the decisions I need before planning (WAIT Options):

1. [Decision topic]:  [A) Option ✓✓]  B) Option  C) Option  (reason with evidence)
2. [Decision topic]:  [A) Option ✓?]   B) Option             (reason explaining uncertainty)
3. ...

**Open questions:** (if any)
- OQ1: [Question about ambiguous aspect that doesn't fit options]
- OQ2: [Question about missing context]

Reply with changes (e.g., "change 2 to B", "OQ1: answer") or "let's proceed" to accept all defaults.
```

If [USER-NAME] changes a foundational decision that affects downstream decisions, re-evaluate and re-present affected decisions.

### Step 8: Fill Objectives + Success Criteria

Fill the [Objectives](//@agent-memory/control-files/plan-templates/high-wizard-plan-template.md#objectives) and [Success Criteria](//@agent-memory/control-files/plan-templates/high-wizard-plan-template.md#success-criteria) sections

### Step 9: Fill Scope

Fill the [Scope](//@agent-memory/control-files/plan-templates/high-wizard-plan-template.md#scope) section (In Scope / Out of Scope)

### Step 10: Fill Confirmed Decisions

Record all confirmed decisions (with any changes [USER-NAME] made) in the [Confirmed Decisions](//@agent-memory/control-files/plan-templates/high-wizard-plan-template.md#confirmed-decisions) section. Include the meaningful reasons - this IS the analysis record.

### Step 11: Early Review

Present objectives, scope, and confirmed decisions to [USER-NAME]. Then propose which optional plan sections to include based on investigation findings.

**Optional sections (lettered)** — propose based on task context:
- **A) Integration Architecture** — Propose when: multi-system changes, multiple components interacting
- **B) System Flow Diagrams** — Propose when: changing data/process flow, API changes, sequence changes
- **C) Technical Considerations** — Propose when: significant technical constraints, limitations, or dependencies exist
- **D) Detailed Analysis** — Propose when: investigation/analysis-focused tasks, unclear objectives needing deep examination
- **E) Bug Investigation** — Propose when: bug fix, debugging, error investigation, unexpected behavior analysis
- **F) Solution Options & Evaluation** — Propose when: brainstorming/decision tasks, multiple viable approaches need evaluation, architecture decisions
- **G) ADR Output** — Propose when: F is included AND the decision has architectural significance worth documenting separately

**Response format:**
```
[Present objectives, scope, and confirmed decisions as before]

Based on the task, I'll include these optional plan sections:
[x] A) Integration Architecture (reason: ...)
[ ] B) System Flow Diagrams (reason: not needed because ...)
[x] C) Technical Considerations (reason: ...)
[ ] D) Detailed Analysis (reason: not needed because ...)
[ ] E) Bug Investigation (reason: not needed because ...)
[ ] F) Solution Options & Evaluation (reason: not needed because ...)
[ ] G) ADR Output (reason: not needed because ...)

Add or remove any? Or proceed.
```

STOP. Present to [USER-NAME] for review. Do NOT write the solution until confirmed to avoid cascading changes when this section needs adjustment.

### Step 12: Fill Solution

Fill the [Solution](//@agent-memory/control-files/plan-templates/high-wizard-plan-template.md#solution) section. Build directly from confirmed decisions.

**Optional sections**: Only fill the optional sections (A-G) that were confirmed in Step 11. Remove unconfirmed optional section markers and their placeholder content from the plan file — do not leave empty optional sections.

**ADR file creation**: If section G is confirmed, after filling all plan sections:
1. Copy the [ADR Template](//@agent-memory/control-files/templates/adr-template.md) to the project's ADR location
2. Fill it using content from section F (Solution Options & Evaluation) and the Confirmed Decisions table
3. Link the ADR back to this plan file
4. Update the plan's section G with the ADR file path

**CRITICAL**: If any NEW decision is discovered during writing that was not covered in Step 7, STOP immediately. Present the new decision to [USER-NAME] with the same format (options + confidence + reason) before continuing. Do NOT write ahead on assumptions.

### Step 13: Fill Implementation Phases

Fill the [Implementation Phases](//@agent-memory/control-files/plan-templates/high-wizard-plan-template.md#implementation-phases) section.

**CRITICAL**: Same rule - if any NEW decision is discovered during writing, STOP immediately and present it before continuing.

### Step 14: Self-Review + Auto-Fix

Do a self-review by thinking critically:
- a. Is there anything missing that should be in scope?
- b. Is there anything that should be out of scope?
- c. Is there any conflict between confirmed decisions and the solution/implementation?
- d. Is there anything redundant?
- e. Are implementation phases in the right order?

**If issues are found**: Auto-fix consistency issues (conflicts, redundancies, ordering) directly in the plan file. For issues that require a NEW decision (scope changes, missing requirements), STOP and present to [USER-NAME] using the WAIT Options format before continuing.

**Report**: Briefly list any auto-fixes made. If no issues found, proceed silently to Step 15.

### Step 15: Final Review

Before presenting the plan, double check: are there any unresolved decisions, assumptions, or new concerns that surfaced during writing (Steps 12-13) or self-review (Step 14) that need [USER-NAME]'s input? If yes, present them now with the same decision format (options + confidence + reason).

Present the complete plan file link to [USER-NAME] for final review. STOP. Wait for instruction.

### Step 16: Start Implementation

After [USER-NAME] instructs to start implementing, start implementing following the **Execution Protocol for AI** from the plan file.

### Step 17: Quality Review

After all implementation phases are done and logged, review the implementation for craftsmanship quality before closing the plan.

1. **Collect scope**: Identify all files created or modified during implementation (from the Execution Log)
2. **Load quality standard**: If a `quality-standard.md` was found during investigation (Step 5, item 7), re-read it now. If not found, note: *"No quality-standard.md found — reviewing against built-in dimensions only."*
3. **Read and analyze**: Read all files in scope. Review using the [Code Quality Analysis Template](//@agent-memory/control-files/plan-templates/code-quality-analysis-template.md) as a reference — walk through each quality dimension that applies, check items against the implementation. Do NOT copy the template — use it as a read-only checklist.
4. **Present findings**: If findings exist, present as WAIT Options grouped by severity:

```
Quality review for implementation:

**Critical:**
1. [File:line] [Issue]:  [A) Fix ✓✓]  B) Alternative  (why this matters)

**Medium:**
2. [File:line] [Issue]:  [A) Fix ✓✓]  B) Alternative  (why this matters)

**Low:**
3. [File:line] [Issue]:  [A) Fix ✓✓]  B) Skip  (minor polish)

**Summary**: X critical, Y medium, Z low

Reply with changes (e.g., "skip 3", "change 1 to B") or "fix all" to accept defaults, or "ship it" to skip all.
```

STOP. Wait for [USER-NAME]'s response.

If no findings: report *"Quality looks good — no findings."* and proceed to Step 18.

5. **Fix approved items**: Apply approved fixes in one batch. Briefly report what was changed.

### Step 18: Move Plan to Completed

After all implementation phases are done, logged, and quality review is resolved, move the plan file to `/plans/completed/`:
`mkdir -p ./plans/completed && mv ./plans/[plan-file].md ./plans/completed/[plan-file].md`

**Note**: Episodic memory links to the plan will break after moving. This is accepted — completed plans are archival.

---
