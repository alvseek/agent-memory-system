# ADR-017: Composed Instruction Artifacts — Inline by Default, Separate When Materialized

**Date**: 2026-08-25

**Status**: Accepted

---

## Problem

A procedure is authored against files it does not contain: shared prose in `components/`, and templates in `resources/`. Before that procedure can be handed to an agent — as an installed command, or as a served Prompt — each reference must be resolved one of two ways: the referenced text is **inlined** into the delivered document, or it is **left as a reference** the agent is expected to fetch separately.

The two compilers in this framework already answer that question differently for templates, each for a defensible reason, and **neither answer was ever recorded as a decision**. It survives only in two docstrings. That makes the split indistinguishable from drift: a reader cannot tell whether the difference is intended, and an agent editing either compiler has nothing to check its change against.

The cost of getting it wrong is asymmetric and quiet. A reference left dangling produces a delivered instruction that points at a path the agent cannot reach — it does not error, it simply degrades, and the agent proceeds without the content. An artifact inlined when it should have stayed separate wastes budget in a payload that ships on every call.

---

## Decision

**We decided to**: inline by default, and keep an artifact separate only for a stated reason.

Composition resolves a reference by **inlining it**, unless one of two conditions holds:

1. **The artifact must be materialized.** The agent will write it to disk as a file or execute it as a script — a plan template copied into a project, a decision-record template written into a repo, an executable helper. What the agent needs is the artifact itself, not a description of it, and the delivered instruction is not the right carrier for something that has to exist as a file.
2. **A server owns its format.** Where content travels back to the memory server, the format is the server's to define and enforce, so the procedure should not carry a second copy of it. The record format is the server's contract, not the instruction's.

**Why we chose this:**
- A reference that cannot be resolved by its reader is worse than a payload that is larger than necessary — the first fails silently, the second is merely expensive.
- Both exceptions name a **capability the reader has** (it will write a file; it will call a server that owns the format), so each can be checked rather than argued.
- It leaves one rule with two stated exceptions, instead of two compilers with two undocumented habits.

**Token budget is a reason to defer inlining, not a reason to separate.** Where full content currently lives in `resources/` because inlining it would push a payload past a client limit, that is a **concession to a limit**, not an application of the rule above. It is recorded as such so it can be revisited: when the payload limit stops binding, those artifacts inline like everything else, and no decision has to be reopened to allow it.

---

## What to Build (Requirements)

**Core Requirements:**
- The core compiler continues to leave `§ template` as a reference, and its docstring states which of the two conditions it is invoking rather than only stating the behaviour.
- Any artifact kept separate carries a one-line reason naming condition 1, condition 2, or the token concession. An artifact separate for no stated reason is a defect.
- Materialized artifacts are reachable by the agent that is told to write them. Keeping an artifact separate without a fetch channel is not condition 1 — it is a dangling reference, and inlining is the correct answer until a channel exists.
- The rule is stated once here and referenced, not restated per compiler.

**Success Criteria:**
- Every separately-held artifact in the core can be traced to one of the three reasons above.
- A compiler change that alters inlining behaviour can be checked against this document rather than against another compiler's habits.
- No delivered instruction — installed command or served Prompt — references a path its reader cannot reach.

---

## Alternatives Rejected

- **Inline everything, unconditionally**: breaks materialized artifacts, whose whole purpose is to become a file, and duplicates a format the server already owns and enforces.
- **Keep everything a reference**: the failure mode is silent. A delivered instruction pointing at an unreachable path degrades without erroring, and the agent proceeds having never read the content.
- **Let each compiler decide for itself**: this is the current state, and it is precisely what makes a deliberate difference unreadable as anything but drift.
- **Make token budget a first-class rule**: it is a property of a client limit, not of the artifact. Encoding it as a rule would make a temporary constraint permanent and require reopening this decision to lift it.

---

**Scope**: this ADR states the general rule. A consumer of the memory core with different reachability constraints may reach the opposite conclusion for its own artifacts; it records that as its own decision extending this one.
