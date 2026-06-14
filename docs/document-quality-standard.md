# Document Quality Standard

## Scope

Applies to all written prose in this framework: procedures, templates, control files, READMEs, knowledge entries, project context docs, and standards (including this one).

## Core Principle

Documents must be **lean, clear, precise, and self-contained**.

Reading cold (no prior context), the executing agent has everything needed: actions, formats, and any referenced concepts stated in-place.

## The Four Properties

### 1. Lean

Every word pulls weight. Cut:

- Rationale blockquotes ("Why X exists") when behavior is already clear
- Phase narrative intros that duplicate the top bullet list
- Expanded examples that don't change behavior
- Hollow name-drops (mentioning a concept without using it)

### 2. Clear

Understandable on first read at the doc's abstraction level. A procedure that says "use the standard pattern" must either define the pattern or link to it with a one-line stated summary.

### 3. Precise

Every phrase carries specific meaning. Avoid:

- Vague verbs ("handle", "manage", "process") when a specific verb fits
- Adjective hedging ("typically", "usually", "generally") when the rule is actually deterministic
- Name-drops without using or explaining the named concept

### 4. Self-Contained or Stated

Keep context within the doc OR briefly state what referenced concepts mean in-place.

- ❌ "follow Phase 0 of /update-memory" — leaky; Phase 0 may shift, and the reader has to load `/update-memory` just to understand the line
- ✅ "before writing, detect whether this is a delta wrap-up (Phase 0 of /update-memory)" — stated in-place; the reader knows what's happening even if they don't follow the link

## Sub-Rules

### No Cross-Procedure Step-Number References

When procedure A references procedure B, describe B's **behavior**, not B's **internal numbering**.

- ❌ "after Step 6 of awakening" — fragile; step numbers shift when B is edited
- ✅ "after awakening loads identity" — describes behavior; survives edits to B

Step numbers within the *same* doc are fine. Cross-doc step references are leaky abstractions.

## Review Checklist

When editing or reviewing a doc, scan for:

- [ ] Any rationale blockquote that could be cut? ("Why X exists" → trim if behavior is already clear)
- [ ] Any phase intro narrative that duplicates the step list? → cut the narrative
- [ ] Any cross-procedure reference using step numbers? → restate as behavior
- [ ] Any name-drop without inline explanation? → add stated context or remove
- [ ] Any vague verb where a precise one fits? → swap

## Origin

Session 2026-06-09 — multiple iterations on `/wrap-up` and `/update-memory` leanness. Refined after fixing a heuristic-threshold drop (deterministic data should be used directly, not fuzzed with a window), a leaky Phase 0 step-number reference, and a hollow `/update-episodic` name-drop. Track record: applied across `/awaken-agent`, `/refresh-memory`, `/map-orientation`, `core-instruction-control-files.md`, `2-core-ras-memory.md`.
