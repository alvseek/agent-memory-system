# Storage-Backend Seam — Contract

Memory procedures share their *judgment* (gates, heuristics, templates, WAIT confirms)
while selecting their *storage mechanics* for Markdown or DB delivery. Converted
procedures and components are complete Markdown documents: one readable file owns the
generic prose, and visible references select named regions of the consolidated
`db.md` or `markdown.md` beside the steps that use them. Unconverted procedures retain
the legacy storage seam described below.

The canonical implementation is the independently installable
[procedure-composer package](../../../packages/procedure-composer/README.md). The
compiler and Munnin call the same package. `seam.py` remains the adapter for legacy
procedures and heading-based backend sections.

## Converted procedures and components

A procedure document lives at `procedures/<name>.md` or
`procedures/memory/<name>.md`; a component lives at
`procedures/components/<name>.md`. Each opens with a `+++` TOML header (format version 2,
ID, kind, title, description, optional arguments and explicit backend-scoped calls) and
then the complete generic body.

A storage reference names the selected backend document and one region:

```markdown
@start storage id="wrap-up.persist-store" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.persist-store"
@end storage
```

In each consolidated backend document the target is an authored region:

```markdown
@start region id="wrap-up.persist-store"
The actual instructions for this backend live here.
@end region
```

- The only substitution is one `{backend}`, restricted to `db` or `markdown`. Component
  references use `procedures/components/<name>.md` and take no substitution.
- Reference interiors are empty. Composed text is never cached in the source.
- A reference may carry `applies_to="db"` or `applies_to="markdown"` when it exists on
  only one backend. Omitted means both. A region may carry `ending="none"` when its
  authored body deliberately has no final newline; the structural line break before
  `@end region` is then not content.
- Directives are recognized outside fenced code. A normal `@start` inside a fence stays
  literal; `@@start` is the explicit fenced reference used where a printed code block
  contains a backend-specific line.
- Regions, references and document identities are unique and validated. Missing
  targets, cycles, unsafe paths, unsupported versions and the superseded fragmented
  assemblies fail explicitly; there is no fallback renderer.

Common backend context is a single named target (`caller-context`) reused by every
converted procedure. DB-only context can be gated with `applies_to="db"` without
appearing in Markdown delivery.

## The legacy seam (unconverted procedures)

1. **Marker**: an unconverted memory procedure has one `## Storage Mechanics` section —
   the swap point. It sits after the procedure body and before `## Templates` / `## Notes`
   if present.
2. **Reference by name**: the procedure body calls storage operations abstractly as
   **`§ op-name`** (e.g. *"list candidate episodes (§ list-candidates)"*). It never spells
   out files or tools inline.
3. **Native (markdown) resolution**: the `## Storage Mechanics` body points to
   `[STORAGE-BACKENDS-PATH]/markdown.md → ## [procedure-name]`, where each `§ op` is
   defined concretely.
4. **Served (db) resolution**: Munnin's `ContentLoader` substitutes the
   `## Storage Mechanics` body with `[STORAGE-BACKENDS-PATH]/db.md → ## [procedure-name]`
   when serving the procedure as an MCP Prompt.

The marker and substitution rule are unchanged. `seam.py::extract_section` now also
expands named regions inside a heading, so a heading shared by a legacy consumer and the
converted documents delivers the same prose and never the directive lines. A superseded
`<!-- composed-source: ... -->` include is refused rather than read.

## Substitution rule (for tooling)

Replace everything from the line **after** the `## Storage Mechanics` header up to (but
not including) the next `## ` header or end-of-file. This is the single, unique swap
region — see `seam.py::substitute_storage_mechanics` (this folder).

## Backend file structure

Converted regions are organized under the procedure or component heading that owns them:

```
## wrap-up

@start region id="wrap-up.persist-store"
<concrete store mechanics>
@end region

@start region id="wrap-up.persistence-report"
<concrete report mechanics>
@end region
```

Unconverted procedures keep their inline heading sections:

```
## load-episodic

### § list-episodes
<concrete steps for this backend>
### § load-episode-body
...
```

The op names are defined by each procedure's own core (they are procedure-scoped, not a
global namespace). Both backends MUST implement the same `§ op` set a procedure references
— `markdown.md` with the git/file mechanics, `db.md` with the tool calls (or an explicit
no-op + reason where the operation dissolves).

### Sections named after a component

A heading may be named after a **component** (`procedures/components/*.md`) rather than a
procedure — e.g. `## core-instruction-control-files`. Use this when a shared fragment
references storage ops of its own: the ops are then defined **once**, instead of being
restated under every procedure that inlines that fragment.

When compiling a legacy procedure `P`, the swapped-in body is `## P` **plus** a
`## C` section for each component `P` inlines (`seam.py::compose_backend_section`).
Either part may be absent. Component regions are expanded before delivery.

### The section every procedure gets

A backend may define one `## all-procedures` section. Its body opens **every** legacy
procedure that backend composes, ahead of `## P` and the component sections — for prose
the backend owes each procedure once rather than restated under each, such as what a
placeholder its ops use (`<domain>`) means to the caller. In the converted format each
procedure references the same `caller-context` region explicitly instead. A backend
without the section composes legacy procedures exactly as before.

## Fidelity invariant

The **markdown** composition (`core + markdown.md §proc`) must preserve **every
behavioral mechanic** of the pre-seam procedure — the fleet's markdown pathway must not
change. Enforced by `tests/content/test_markdown_fidelity.py` plus a per-procedure
before→after instruction map. Converted compositions are additionally compared with the
recorded current-review baseline on both backends.
