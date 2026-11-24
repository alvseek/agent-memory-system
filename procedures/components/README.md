# Components — Contract

A **component** is a reusable procedural fragment shared by two or more procedures. It is
**not** a slash command: it is never installed, never served on its own, and never invoked
by name. At delivery it is **expanded** into every procedure that references it, so the
delivered procedure is self-contained.

This mirrors the storage seam one folder over: logic with more than one consumer lives in
exactly one file, and every consumer composes from it.

## What belongs here

- **Component** — genuinely shared, substantial prose that would otherwise be duplicated and
  drift. Only meaningful as part of a parent procedure.
- **Not a component** — a procedure that is useful on its own (that is a command, in
  `procedures/`), fill-out data (that is a template, in `procedures/memory/resources/`), or
  the storage mechanics (those are named regions in `storage-backends/db.md` and
  `markdown.md`, selected by a storage reference).

Extract only genuinely-shared substantial content. Stable one-line repetition stays inline;
a fragment that differs per caller beyond a plugged-in value stays inline too.

## File shape

A component is one complete Markdown document with a `+++` TOML header and the body that
is delivered:

```markdown
+++
format_version = 2
id = "no-subagent-load"
kind = "component"
title = "Load into Your Own Context"
description = "The rule that memory is loaded into the agent's own context."
+++
Run the load yourself, in this context. Do **NOT** delegate it to a sub-agent.
```

The body may contain its own `@start storage` or `@start component` references. Those
expand in the same backend and cycle-checked graph as the parent.

## How a procedure references one

A converted procedure uses a paired reference with an explicit identity:

```markdown
@start component id="wrap-up.rules" ref="procedures/components/no-subagent-load.md"
@end component
```

The reference interior is empty; the component's complete body is inserted at that point.
A component that appears twice uses two distinct reference identities.

An unconverted legacy caller may still reference a component by markdown link ending in
`components/<name>.md`; the component adapter composes the same complete document for that
caller. The superseded `<!-- composed-component: -->` pointer is refused.

## Delivery

Expansion lives once in [inline.py](inline.py) and in the composer, and is imported by
every consumer:

- `procedures/setup-scripts/compile-procedures.py` → the installed slash commands
- Munnin's `ContentLoader` → the served MCP Prompts

For a legacy caller, inlining runs **before** seam substitution, so a `§ op` arriving
inside a component is counted by the seam's coverage check. A referenced component that
does not exist leaves its reference visible and is reported — `--strict` fails on it.
