# WAIT Options Format Reference

Reusable format definition for **WAIT Options** (What Am I Thinking? Options) — the structured pattern for surfacing a decision to [USER-NAME] and collecting an answer. It is the single source of truth for that format, so any procedure that needs to ask something references it instead of defining the format inline.

What it defines is **how** to present a decision. This file is deliberately caller-blind: it does not know who invoked it, what scope that caller works at, or what belongs in their decision set — a caller that needs to bound its own decision set declares that in its own procedure. The same blindness applies to altitude: it requires that the technical core of a decision be named, without assuming what nouns that decision is made of.

---

## What to Surface

Not every decision warrants a question to be presented in WAIT Options. Use this taxonomy to decide which of *your* decisions to surface and which to write directly into the plan. It classifies a decision you already hold — one that is not yours at this altitude should not be zoned here at all, but handed to whoever owns it.

### Zone Taxonomy

| Zone | What | Action |
|------|------|--------|
| **A — Mechanical/Obvious** | One real choice, no judgment call (e.g. only one candidate exists and it fits) | Write to plan. No surface. |
| **B — Technical Core** | The mechanism the decision commits to, at the altitude the decision lives | Write to plan **AND** disclose in WAIT (visibility, not decision) |
| **C — Genuine Uncertainty** | Agent honestly does not know which option is right | Surface in WAIT. Options + confidence + reason. |
| **D — Value-Loaded Tradeoff** | Both options valid; answer depends on [USER-NAME]'s priorities (time horizon, tech debt tolerance, risk appetite). "Quick fix vs long-term fix" lives here. | Surface in WAIT. Options + tradeoff dimensions. |
| **E — Risky/Irreversible** | Even when judgment is clear, cost of being wrong is high (destroying data, an action that cannot be undone, or changing something others already depend on) | Surface in WAIT even when confident. Cost asymmetry justifies the question. |

### How to Apply

- **Default to writing through (Zone A)** when the choice is genuinely mechanical. Over-asking trains [USER-NAME] to skim — silent decisions for non-decisions.
- **Always disclose technical core (Zone B)** even when the direction is clear. The agent should never quietly make a commitment [USER-NAME] cannot see — surface the mechanism the decision actually commits to, expressed at the altitude the decision lives.
- **Ask Zone C and D** because the agent shouldn't decide alone — C because correctness is uncertain, D because the answer depends on [USER-NAME]'s priorities the agent cannot know.
- **Always ask Zone E** even when the answer feels clear. Reversal cost asymmetry is the trigger, not uncertainty.

### Capturing Written-Through Decisions

Decisions in Zone A and Zone B (written through, not asked) still belong in the *Confirmed Decisions* table of the plan. [USER-NAME] can spot-check during plan review without round-tripping each decision. The discipline is: *did you write the reasoning down?* — not *did you ask?*

---

## Core Format

### Context Grouping

Always group decisions under at least one **context heading** — a bold label plus a brief explanation of what area the decisions relate to and *why* they are needed. When decisions span multiple topics, use multiple context headings separated by `---`.

What the groups are organized *by* is the caller's to choose: a findings review may group by severity, a plan by milestone or phase. Any axis works, as long as each group carries a heading and the per-decision format below is preserved.

### Context Depth

For each decision, provide a short clean, slim, lean, effective, and in plain words context so [USER-NAME] can evaluate options without scrolling back to the investigation. Use this checklist — include each item that applies:

1. **Problem statement** — What is the issue or gap being decided on
2. **Evidence / code references** — What was found in the codebase, architecture, or docs that informs this
3. **Example scenario** — A concrete case showing what happens (or goes wrong) to make the impact tangible
4. **Impact** — Why this decision matters now, what it affects downstream

Not every decision needs all 4 — a simple naming choice may only need the problem statement, while a model design gap needs all of them.

**When the decision arose in conversation, most of this is already paid.** Context depth exists because a caller usually presents decisions after work [USER-NAME] did not watch, so the evidence has to be rebuilt for them. In a live exchange it does not: they saw the investigation happen, and restating it reads as padding. Drop to the topic, the options with their confidence marks, and a one-line reason — then add depth back only for the part that genuinely was not visible.

### Critical Technical Disclosure (Mandatory)

Even when the direction is already clear to the agent, [USER-NAME] still needs visibility into the core of what is being committed to. Always name the concrete mechanism in the decision context — named, not gestured at.

Do not hide the mechanism, jargon, and project specific terms just because there is no ambiguity. WAIT Options should surface it so [USER-NAME] can make informed decisions.

### Concrete Examples & Visualizations

When words alone aren't enough to evaluate options, include a concrete example in the context or within an option, matched to the kind of thing being decided — but only where it earns its place, since forcing an example onto already-clear text just adds bulk.

### Per-Decision Format

For each decision:

- Provide **2-4 options**, each on its own line
- Mark recommended default with **confidence signal**: `✓✓` (strong, clear evidence) or `✓?` (uncertain, genuine tradeoff)
- Include **per-option analysis** (pros/cons) on indented lines below each option — only when applicable (skip for self-explanatory options)
- After the options, include a **reason paragraph** explaining the recommendation and tradeoffs
- Include the mandatory technical disclosure in the decision context whenever the decision commits to a mechanism — expressed at the altitude that decision lives

Order decisions by dependency (foundational choices first, dependent ones after).

### Open Questions

Not everything you need from [USER-NAME] is a decision, and the two blur because both
arrive on the page as a question. What separates them is whether you can write the
answers down. A decision is a choice between courses of action you have already worked
out: you did the investigation, you hold the alternatives, and what remains is the
judgment only he can apply. A yes/no or do/don't is one of these — two courses of action
is two, and presenting it as a decision gives him the confidence mark and the reason that
a bare question would drop. An open question asks for something that was never yours to
work out — how the app is really used, how much a feature matters to him, what he intends
by something you have no way to derive. There is nothing to enumerate because the answer
lives with him.

So the test, run before you write either shape: **can I set out the answers?** Two to four
real courses of action means you have a decision and owe him the options block above. An
answer he would have to tell you — a fact about his world, a priority, an intent — means
you owe him a plain question instead.

Open questions are collected as `OQ1, OQ2, ...` after the decisions, each a plain line: no
blockquote, no confidence mark, no options. The absence of an options block is what tells
him at a glance which shape he is looking at, and there is nothing to be confident *about*
when you are asking him to tell you something only he knows.

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
8. **Open questions** — plain lines after the last context group, before the reply instruction; no blockquote and no confidence marks, since the absence of an options block is what distinguishes them from decisions

---

## Standard Response Template

Use this template when presenting decisions to [USER-NAME]. Replace `[preamble]` with context-appropriate text (e.g., "I've investigated the codebase. Here are the decisions I need before planning", "Based on my investigation, here's what I think you want", etc.)

### Template

````
[preamble] (WAIT Options):

**Context A: [Area label]**

[Brief explanation of what area these decisions relate to and why they're needed.]

**1. [Decision topic]:**

- [Context: problem statement, evidence found, example scenario showing impact.
  Include as many context depth items as the decision warrants. Name the mechanism this decision
  commits to, at the altitude the decision lives.]

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

- [Context with a concrete example — a sketch, a snippet, or a worked scenario,
  whichever makes this particular choice tangible.]

  > A) [Option] `✓?`
  > B) [Option]

  ([Reason explaining the uncertainty.])

**Open questions:** (if any)
- OQ1: [Open point with no settled answer yet — needs discussion, not a choice]
- OQ2: [Something only he can tell you — how this is used in practice, how much it matters to him]

Reply with changes (e.g., "change 2 to B", "OQ1: answer") or "let's proceed" to accept all defaults.
````

---

## Re-evaluation Rule

If [USER-NAME] changes a foundational decision that affects downstream decisions, re-evaluate and re-present affected decisions before continuing.
