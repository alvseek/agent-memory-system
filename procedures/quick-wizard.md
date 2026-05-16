# Quick Wizard Protocol

Execute lightweight smart planning with decision collection and direct execution — same decision-collection discipline as High Wizard but without a custom plan template file. Uses the IDE's built-in plan mode for structured execution tracking. Includes a scope gate that auto-escalates to /high-wizard when the task is too complex for direct execution.

## Arguments

`$ARGUMENTS`

- `/quick-wizard [context]` → Create Quick Wizard plan for the given context
- `/quick-wizard` → Will ask for context

If no arguments provided, ask: "What feature or task should I create a Quick Wizard plan for?"

---

## Procedure

*IMPORTANT: This procedure structurally enforces UUID f3a8b2c1 (VERIFY FIRST) - the agent MUST collect and confirm decisions BEFORE executing. Jumping directly into implementation is prohibited.*

### Step 1: Investigate and Collect Decisions

This is where the thinking happens. Follow the investigation checklist below IN ORDER. Each step from 3-7 produces decision items for the WAIT Options form.

Read and follow the [WAIT Options format](//@agent-memory/control-files/procedures/wait-options.md) for collecting decisions.

**Investigation checklist (in order):**

1. **Requirements clarity** - Is the intent already clear? Is there ambiguity within the context? If ambiguous, create decisions to clarify before proceeding
2. **Codebase scan** - Scan relevant files, modules, and architecture related to the task to understand current state
3. **Critical technical points disclosure** - Identify the main function/module entrypoints, core engine algorithm/logic pattern, and key execution flow touchpoints. Surface these in WAIT Options even when the implementation direction is already clear
4. **Alternative approaches** - Based on the requirement, discover what ways this can be done (there's usually more than one) → offer as decisions
5. **Reusable components** - Identify existing functions, utilities, patterns that could be leveraged → offer to reuse the related/reusable ones as decisions
6. **Conflicts and constraints** - Note what could go wrong, what limits exist → if any, offer options based on pros and cons as decisions
7. **Integration points** - Check what existing code/systems will be affected → if concerning, offer options as decisions
8. **Quality standard discovery** - Search for `quality-standard.md` in the project via glob (`**/quality-standard.md`). If found, load it as additional implementation criteria to reference during execution. If not found, note it and proceed

### Step 2: Scope Gate Assessment

After investigation, assess whether this task is suitable for Quick Wizard (direct execution) or needs to escalate to /high-wizard (file-based planning).

**Escalate to /high-wizard when ANY of these apply:**
- Task likely spans multiple sessions or risks context compaction
- Multiple files with complex interdependencies need modification
- Task requires production deployment with audit trail
- Implementation has irreversible consequences requiring careful tracking
- You feel uncertain about completing within the current session
- Task involves bug investigation requiring hypothesis-driven debugging (high-wizard section E)
- Task requires evaluating multiple solution approaches with formal comparison (high-wizard section F)
- Task produces an architecture decision record (high-wizard sections F+G)

**If escalating**: Tell [USER-NAME] "This task is complex enough to benefit from /high-wizard — escalating with the decisions I've already collected." Then execute [High Wizard Protocol](//@agent-memory/control-files/procedures/high-wizard.md) starting from Step 7 (decisions already collected). STOP HERE — do not continue with Quick Wizard steps.

**If suitable for Quick Wizard**: Continue to Step 3.

### Step 3: Present WAIT Options

Present the WAIT Options form to [USER-NAME] using the [WAIT Options format](//@agent-memory/control-files/procedures/wait-options.md).
Preamble: "I've investigated the codebase. Here are the decisions I need before proceeding"

STOP. Present to [USER-NAME] for review. Do NOT proceed until decisions are confirmed.

### Step 4: Create Execution Plan

Enter plan mode if available. If plan mode is not available, present the plan directly in conversation for [USER-NAME]'s approval.

Write the execution plan using the [Quick Wizard Plan Content Template](#quick-wizard-plan-content-template) structure:
- Objective (1-2 sentences)
- Confirmed decisions table
- Numbered execution steps with clear actions

### Step 5: Get Approval

Present the plan for [USER-NAME]'s approval. STOP. Do NOT execute until [USER-NAME] confirms.

### Step 6: Execute

Execute the steps from the plan in order. After each step, briefly report what was done before moving to the next.

**CRITICAL**: If any NEW decision is discovered during execution that was not covered in Step 3, STOP immediately. Present the new decision to [USER-NAME] with the same format (options + confidence + reason) before continuing. Do NOT execute ahead on assumptions.

### Step 7: Quality Review

After all steps are executed, review the implementation for craftsmanship quality before reporting completion.

1. **Collect scope**: Identify all files created or modified during execution
2. **Load quality standard**: If a `quality-standard.md` was found during investigation (Step 1, item 7), re-read it now. If not found, note: *"No quality-standard.md found — reviewing against built-in dimensions only."*
3. **Read and analyze**: Read all files in scope. Review using the [Code Quality Analysis Template](//@agent-memory/control-files/plan-templates/code-quality-analysis-template.md) as a reference — walk through each quality dimension that applies, check items against the implementation. Do NOT copy the template — use it as a read-only checklist.
4. **Present findings**: If findings exist, present using the [WAIT Options Quality Review variant](//@agent-memory/control-files/procedures/wait-options.md#quality-review-variant).
Preamble: "Quality review for implementation:"

STOP. Wait for [USER-NAME]'s response.

5. **Fix approved items**: Apply approved fixes in one batch. Briefly report what was changed.

### Step 8: Report Completion

After all steps are executed and quality review is resolved, present a brief completion summary to [USER-NAME]:
- What was done
- Any issues encountered
- Any tech debts or follow-up items

---

## Templates

### Quick Wizard Plan Content Template

Use this structure when writing the plan in plan mode (or presenting in conversation):

```markdown
# Quick Wizard Plan: [Theme]

## Objective
[1-2 sentence description of what we're doing and why]

## Confirmed Decisions
| # | Decision | Chosen | Reason |
|---|----------|--------|--------|
| 1 | [Topic] | [Choice] | [Why] |

## Success Criteria
- [ ] [How we know it's done]
- [ ] Quality review completed (Step 7)

## Execution Steps
1. **[Step name]**: [What to do] → [How to verify]
2. **[Step name]**: [What to do] → [How to verify]
3. **[Step name]**: [What to do] → [How to verify]
```

---
