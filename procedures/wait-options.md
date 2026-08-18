# WAIT Options Format Reference

Reusable format definition for **WAIT Options** (What Am I Thinking? Options) — the structured pattern for surfacing a decision to [USER-NAME] and collecting an answer. It is the single source of truth for that format, so any procedure that needs to ask something references it instead of defining the format inline.

What it defines is **how** to present a decision, never **which** decisions are yours. This file is deliberately caller-blind: it does not know who invoked it, what scope that caller works at, or what belongs in their decision set — a caller that needs to bound its own decision set declares that in its own procedure. The same blindness applies to altitude: it requires that the technical core of a decision be named, without assuming what nouns that decision is made of.

---

## What to Surface

Not every decision warrants WAIT Options. Use this taxonomy to decide which of *your* decisions to surface and which to write directly into the plan. It classifies a decision you already hold — one that is not yours at this altitude should not be zoned here at all, but handed to whoever owns it.

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

Always group decisions under at least one **context heading** — a bold label + brief explanation of what area the decisions relate to. When decisions span multiple topics, use multiple context headings separated by `---`. Each heading names the area and explains *why* these decisions are needed.

### Context Depth

For each decision, provide context so [USER-NAME] can evaluate options without scrolling back to the investigation. Use this checklist — include each item that applies:

1. **Problem statement** — What is the issue or gap being decided on
2. **Evidence / code references** — What was found in the codebase, architecture, or docs that informs this
3. **Example scenario** — A concrete case showing what happens (or goes wrong) to make the impact tangible
4. **Impact** — Why this decision matters now, what it affects downstream

Not every decision needs all 4 — a simple naming choice may only need the problem statement, while a model design gap needs all of them.

**When the decision arose in conversation, most of this is already paid.** Context depth exists because a caller usually presents decisions after work [USER-NAME] did not watch, so the evidence has to be rebuilt for them. In a live exchange it does not: they saw the investigation happen, and restating it reads as padding. Drop to the topic, the options with their confidence marks, and a one-line reason — then add depth back only for the part that genuinely was not visible.

### Critical Technical Disclosure (Mandatory)

Even when the direction is already clear to the agent, [USER-NAME] still needs visibility into the core of what is being committed to. Always name the concrete mechanism in the decision context — named, not gestured at.

**Express it at the altitude the decision lives.** The calling procedure defines that altitude; this file does not. A decision about where a milestone boundary falls and a decision about how a function is written both have a technical core, but they are not made of the same nouns — disclosing one in the vocabulary of the other either commits prematurely or invents detail.

Do not hide the mechanism just because there is no ambiguity. WAIT Options should surface it so [USER-NAME] can make informed decisions.

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

### Decisions vs Open Questions

Not everything you need from [USER-NAME] is a decision. The test is whether answering requires him to choose between alternatives you have to lay out: two to four **distinct courses of action** earn the options block above, while anything he can answer without reading one is a **named open question** (OQ1, OQ2, ...), collected after the decisions. That covers the genuinely open point the name comes from — no settled answer yet, needs discussion — and equally the plain binary, since "no" is only the absence of "yes" and rendering it as `A) yes  B) no` adds ceremony without adding information.

A binary still owes what any decision owes. Name the mechanism on its line when it commits to one, and give it the full decision shape anyway when it lands in Zone E — risky, irreversible, or depended on by others — because the cost asymmetry that justifies asking is the same asymmetry that justifies the disclosure.

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
- OQ2: [Plain binary — yes/no or do/don't, naming the mechanism if it commits to one]

Reply with changes (e.g., "change 2 to B", "OQ1: answer") or "let's proceed" to accept all defaults.
````

---

## Re-evaluation Rule

If [USER-NAME] changes a foundational decision that affects downstream decisions, re-evaluate and re-present affected decisions before continuing.

---

## Customization Guidance

The split is between **shape** and **scope**: the shape of a presented decision is fixed so every procedure looks the same to [USER-NAME]; the scope — *which* decisions belong in the set at all — is the caller's, and this file has no opinion on it.

**Fixed — do not modify per-procedure:**
- **Core format** — context depth + options + confidence signals + per-option analysis + reason + open questions
- **Presentation style** — bullet-indented explanation, blockquoted options, bullet-indented reason
- **Reply instruction** — always include it so [USER-NAME] knows how to respond

**Caller-owned — decide these in your own procedure:**
- **Scope** — which decisions belong at your altitude, and which belong to something you delegate to. This file cannot know that; do not read the fixed shape above as a claim that it can.
- **Technical disclosure vocabulary** — the mechanism you name is the one your altitude is made of (see *Critical Technical Disclosure*)
- **Preamble text** — match it to your context (planning decisions, requirements, quality findings, gap analysis, etc.)
- **Context grouping** — a findings review may group by severity, a plan by milestone or phase, as long as each group has a heading and the per-decision format is preserved
