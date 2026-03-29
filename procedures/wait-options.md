# WAIT Options Format Reference

Reusable format definition for **WAIT Options** (What Am I Thinking? Options) — the structured decision-collection pattern used across all wizard protocols and quality procedures.

This file is the single source of truth. Procedures reference it instead of defining the format inline.

---

## Core Format

For each decision or finding to present:

- Provide **context** so [USER-NAME] understands what was discovered and why this decision matters — use **inline context** for simple decisions (1-2 lines) or **before-question context** for decisions that need more background
- Provide **2-4 options**
- Mark recommended default with **confidence signal**: `✓✓` (strong, clear evidence) or `✓?` (uncertain, genuine tradeoff)
- Include a **meaningful reason** that serves as the analysis record
- If any questions remain that don't fit into options format, collect them as **named open questions** (OQ1, OQ2, ...) to present alongside decisions

Order decisions by dependency (foundational choices first, dependent ones after).

---

## Standard Response Template

Use this template when presenting decisions to [USER-NAME]. Replace `[preamble]` with context-appropriate text (e.g., "I've investigated the codebase. Here are the decisions I need before planning", "Based on my investigation, here's what I think you want", etc.)

```
[preamble] (WAIT Options):

1. [Decision topic] ([inline context — what was found, why it matters]):
   [A) Option ✓✓]  B) Option  C) Option  (reason with evidence)

2. [Decision topic]:
   [Before-question context — longer explanation of what was discovered,
   current state, tradeoffs, or constraints that inform this decision.]
   [A) Option ✓?]  B) Option  (reason explaining uncertainty)

3. [Decision topic] ([short context]):  [A) Option ✓✓]  B) Option  (reason)

**Open questions:** (if any)
- OQ1: [Question about ambiguous aspect that doesn't fit options]
- OQ2: [Question about missing context]

Reply with changes (e.g., "change 2 to B", "OQ1: answer") or "let's proceed" to accept all defaults.
```

**Context placement rule**: Use inline `([context])` when the context is a short phrase or single line. Use before-question context (indented block before the options) when [USER-NAME] needs more background to make an informed decision.

---

## Quality Review Variant

Use this template when presenting code quality findings or implementation review results. Group by severity instead of numbering sequentially.

```
[preamble] (e.g., "Quality review for implementation:", "Code quality review for [scope]:"):

**Critical:**
1. [File:line] [Issue]:  [A) Fix ✓✓]  B) Alternative  (why this matters)

**Medium:**
2. [File:line] [Issue]:  [A) Fix ✓✓]  B) Alternative  (why this matters)

**Low:**
3. [File:line] [Issue]:  [A) Fix ✓✓]  B) Skip  (minor polish)

**Summary**: X critical, Y medium, Z low

Reply with changes (e.g., "skip 3", "change 1 to B") or "fix all" to accept defaults, or "ship it" to skip all.
```

If no findings: report *"Quality looks good — no findings."* and proceed.

---

## Re-evaluation Rule

If [USER-NAME] changes a foundational decision that affects downstream decisions, re-evaluate and re-present affected decisions before continuing.

---

## Customization Guidance

- **Preamble text** is procedure-specific — customize it to match the context (planning decisions, requirements, quality findings, gap analysis, etc.)
- **Core format** (options + confidence signals + reasons + open questions) is fixed — do not modify per-procedure
- **Reply instruction** is fixed — always include it so [USER-NAME] knows how to respond
- **Grouping** can be adapted — the quality review variant groups by severity; other procedures may group by milestone, by phase, etc. as long as the core format per item is preserved
