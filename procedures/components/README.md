# Components — Contract

A **component** is a reusable procedural fragment shared by two or more procedures. It is
**not** a slash command: it is never installed, never served on its own, and never invoked
by name. At delivery it is **inlined** into every procedure that references it, so the
delivered procedure is self-contained.

This mirrors the storage seam one folder over: logic with more than one consumer lives in
exactly one file, and every consumer composes from it.

## What belongs here

- **Component** — genuinely shared, substantial prose that would otherwise be duplicated and
  drift. Only meaningful as part of a parent procedure.
- **Not a component** — a procedure that is useful on its own (that is a command, in
  `procedures/`), fill-out data (that is a template, in `procedures/memory/resources/`), or
  the `## Storage Mechanics` section (that is the **seam**, already swapped by `seam.py` —
  extracting it would collide with the mechanism that owns it).

Extract only genuinely-shared substantial content. Stable one-line repetition stays inline;
a fragment that differs per caller beyond a plugged-in value stays inline too.

## File shape

A header block, a standalone `---` rule, then the body. **Only the body is inlined.**

```markdown
# Component Title (component)

One line on what this is and who consumes it. **This is a component, not a standalone
command** — callers reference it by link and it is inlined at compile time.

---

<the body that gets inlined>
```

## How a procedure references one

By markdown link ending in `components/<name>.md`. The path prefix is free — use a relative
path so the link is clickable while editing:

```markdown
[🚨 **Load-into-own-context rule**](components/no-subagent-load.md)
```

At compile the link becomes its **label text** and the body is inserted directly after, so
the label carries any caller-specific wording. Pick a label that reads correctly on its own,
because that is what ships.

## Delivery

Inlining lives once in [inline.py](inline.py) and is imported by every consumer:

- `procedures/setup-scripts/compile-procedures.py` → the installed slash commands
- Munnin's `ContentLoader` → the served MCP Prompts

It runs **before** seam substitution, so a `§ op` arriving inside a component is counted by
the seam's coverage check. A referenced component that does not exist leaves its link
visible and is reported — `--strict` fails on it.
