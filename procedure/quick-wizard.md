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

This is where the thinking happens. Follow the investigation checklist below IN ORDER. Each step from 3-6 produces decision items for the decision form.

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

### Step 2: Scope Gate Assessment

After investigation, assess whether this task is suitable for Quick Wizard (direct execution) or needs to escalate to /high-wizard (file-based planning).

**Escalate to /high-wizard when ANY of these apply:**
- Task likely spans multiple sessions or risks context compaction
- Multiple files with complex interdependencies need modification
- Task requires production deployment with audit trail
- Implementation has irreversible consequences requiring careful tracking
- You feel uncertain about completing within the current session

**If escalating**: Tell [USER-NAME] "This task is complex enough to benefit from /high-wizard — escalating with the decisions I've already collected." Then execute [High Wizard Protocol](//@agent-memory/control-files/procedure/high-wizard.md) starting from Step 7 (decisions already collected). STOP HERE — do not continue with Quick Wizard steps.

**If suitable for Quick Wizard**: Continue to Step 3.

### Step 3: Present Decisions

Present the decision form to [USER-NAME]. STOP. Present to [USER-NAME] for review. Do NOT proceed until decisions are confirmed.

**Response format:**
```
I've investigated the codebase. Here are the decisions I need before proceeding:

1. [Decision topic]:  [A) Option ✓✓]  B) Option  C) Option  (reason with evidence)
2. [Decision topic]:  [A) Option ✓?]   B) Option             (reason explaining uncertainty)
3. ...

Reply with changes (e.g., "change 2 to B") or "let's proceed" to accept all defaults.
```

If [USER-NAME] changes a foundational decision that affects downstream decisions, re-evaluate and re-present affected decisions.

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

### Step 7: Report Completion

After all steps are executed, present a brief completion summary to [USER-NAME]:
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

## Execution Steps
1. **[Step name]**: [What to do] → [How to verify]
2. **[Step name]**: [What to do] → [How to verify]
3. **[Step name]**: [What to do] → [How to verify]
```

---
