# WAIT Options Format Reference

Reusable format definition for **WAIT Options** (What Am I Thinking? Options) — the structured decision-collection pattern used across all wizard protocols and quality procedures.

This file is the single source of truth. Procedures reference it instead of defining the format inline.

---

## Core Format

### Context Grouping

Always group decisions under at least one **context heading** — a bold label + brief explanation of what area the decisions relate to. When decisions span multiple topics, use multiple context headings separated by `---`. Each heading names the area and explains *why* these decisions are needed.

### Context Depth

For each decision, provide context so [USER-NAME] can evaluate options without scrolling back to the investigation. Use this checklist — include each item that applies:

1. **Problem statement** — What is the issue or gap being decided on
2. **Evidence / code references** — What was found in the codebase, architecture, or docs that informs this
3. **Example scenario** — A concrete case showing what happens (or goes wrong) to make the impact tangible
4. **Impact** — Why this decision matters now, what it affects downstream

Not every decision needs all 4 — a simple naming choice may only need the problem statement, while a model design gap needs all of them.

### Concrete Examples & Visualizations

When words alone aren't enough to evaluate options, include a concrete example in the context or within an option. Match the example type to the domain:
- **UI/UX** → simple ASCII wireframe
- **Architecture / data model** → code snippet or schema fragment
- **Business logic** → example scenario showing behavior
- **Integration** → data flow or sequence sketch

Only when applicable — don't force examples where the text is already clear.

### Per-Decision Format

For each decision:

- Provide **2-4 options**, each on its own line
- Mark recommended default with **confidence signal**: `✓✓` (strong, clear evidence) or `✓?` (uncertain, genuine tradeoff)
- Include **per-option analysis** (pros/cons) on indented lines below each option — only when applicable (skip for self-explanatory options)
- After the options, include a **reason paragraph** explaining the recommendation and tradeoffs
- If any questions remain that don't fit into options format, collect them as **named open questions** (OQ1, OQ2, ...) to present alongside decisions

Order decisions by dependency (foundational choices first, dependent ones after).

---

## Presentation Style

These formatting rules ensure WAIT Options are scannable and readable:

1. **Context headings** in `**bold**` followed by a brief explanation paragraph
2. **Decision headers** as `**1. Decision topic:**` with a blank line before each
3. **Decision explanation** as a bullet-indented paragraph (`- text`) — gives visual indent without blockquote background
4. **Options** inside a blockquote (`> A) ...`, `> B) ...`) — each option on its own line, gray background visually separates them from surrounding text
5. **Per-option pros/cons** as indented lines under each option inside the blockquote (`> - pro/con`) — only when applicable
6. **Reason paragraph** as bullet-indented text after the options block, analyzing the recommendation
7. **Context group separators** — use `---` between different context groups
8. **Open questions** — listed after the last context group, before the reply instruction

---

## Standard Response Template

Use this template when presenting decisions to [USER-NAME]. Replace `[preamble]` with context-appropriate text (e.g., "I've investigated the codebase. Here are the decisions I need before planning", "Based on my investigation, here's what I think you want", etc.)

### Template

````
[preamble] (WAIT Options):

**Context A: [Area label]**

[Brief explanation of what area these decisions relate to and why they're needed.]

**1. [Decision topic]:**

- [Context: problem statement, evidence from codebase, example scenario showing impact.
  Include as many context depth items as the decision warrants.]

  > A) [Option] `✓✓`
  > - [Pro/con analysis — only when applicable]
  >
  > B) [Option]
  > - [Pro/con analysis]
  >
  > C) [Option]
  > - [Pro/con analysis]

  ([Reason paragraph: why A is recommended, how B/C compare, key tradeoffs.])

**2. [Decision topic]:**

- [Simpler context — not every decision needs all 4 depth items.]

  > A) [Option] `✓✓`
  > B) [Option]

  ([Reason paragraph.])

---

**Context B: [Different area label]**

[Brief explanation of this second area.]

**3. [Decision topic]:**

- [Context with concrete example — e.g., for UI/UX include a simple wireframe,
  for architecture include a code snippet, for business logic show the scenario.]

  > A) [Option] `✓?`
  > B) [Option]

  ([Reason explaining the uncertainty.])

**Open questions:** (if any)
- OQ1: [Question about ambiguous aspect that doesn't fit options]
- OQ2: [Question about missing context]

Reply with changes (e.g., "change 2 to B", "OQ1: answer") or "let's proceed" to accept all defaults.
````

---

## Quality Review Variant

Use this template when presenting code quality findings or implementation review results. Group by severity instead of context topics.

````
[preamble] (e.g., "Quality review for implementation:", "Code quality review for [scope]:"):

**Critical:**

**1. [File:line] [Issue]:**

- [What's wrong and why it matters.]

  > A) [Fix] `✓✓`
  > B) [Alternative]

  ([Why this matters.])

**Medium:**

**2. [File:line] [Issue]:**

- [What's wrong.]

  > A) [Fix] `✓✓`
  > B) [Alternative]

  ([Analysis.])

**Low:**

**3. [File:line] [Issue]:**

  > A) [Fix] `✓✓`
  > B) Skip

  ([Minor polish.])

**Summary**: X critical, Y medium, Z low

Reply with changes (e.g., "skip 3", "change 1 to B") or "fix all" to accept defaults, or "ship it" to skip all.
````

If no findings: report *"Quality looks good — no findings."* and proceed.

---

## Re-evaluation Rule

If [USER-NAME] changes a foundational decision that affects downstream decisions, re-evaluate and re-present affected decisions before continuing.

---

## Customization Guidance

- **Preamble text** is procedure-specific — customize it to match the context (planning decisions, requirements, quality findings, gap analysis, etc.)
- **Core format** (context depth + options + confidence signals + per-option analysis + reason + open questions) is fixed — do not modify per-procedure
- **Presentation style** (bullet-indented explanation, blockquoted options, bullet-indented reason) is fixed — follow the style rules for consistent readability
- **Reply instruction** is fixed — always include it so [USER-NAME] knows how to respond
- **Context grouping** can be adapted — the quality review variant groups by severity; other procedures may group by milestone, by phase, etc. as long as each group has a heading and the per-decision format is preserved
