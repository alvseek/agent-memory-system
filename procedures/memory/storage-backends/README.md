# Storage-Backend Seam — Contract

Memory procedures are **storage-agnostic**: each one carries its *judgment* (gates, heuristics, templates, WAIT confirms) in its body, and delegates its *storage mechanics* (how memory is physically read/written) to a swappable **backend**. This is the prose-layer mirror of the code's `MemoryRepository` Protocol — one procedure "core", two concrete backends.

## The two backends

- **[markdown.md](markdown.md)** — memory lives as a markdown tree over git (the native fleet world): files under `agent-[domain]/`, a hand-maintained `agent-memory-index.md`, `cp` from templates, `date` for timestamps.
- **[db.md](db.md)** — memory lives in Valaskjalf via **Munnin**: the 8 generic data tools (`awaken`·`get`·`query`·`search`·`insert`·`edit`·`archive`·`soft_delete`). The index is a derived `SELECT`, so index/housekeeping steps become explicit no-ops.

## The seam (how a procedure connects to a backend)

1. **Marker**: every memory procedure has exactly **one** `## Storage Mechanics` section — the swap point. It sits after the procedure body (after `## Procedure` / the phase sections) and before `## Templates` / `## Notes` if present.
2. **Reference by name**: the procedure body calls storage operations abstractly as **`§ op-name`** (e.g. *"list candidate episodes (§ list-candidates)"*, *"persist the sub-episode (§ append-sub-episode)"*). It never spells out files or tools inline.
3. **Native (markdown) resolution**: in this submodule, the `## Storage Mechanics` body simply **points** to `storage-backends/markdown.md → ## [procedure-name]`, where each `§ op` is defined concretely. A markdown-era agent reads the core, then follows that pointer.
4. **Served (db) resolution**: Munnin's `ContentLoader` **substitutes** the `## Storage Mechanics` body with `storage-backends/db.md → ## [procedure-name]` when serving the procedure as an MCP Prompt. The agent gets the same core, DB mechanics.

## Substitution rule (for tooling)

Replace everything from the line **after** the `## Storage Mechanics` header up to (but not including) the next `## ` header or end-of-file. This is the single, unique swap region — see `src/munnin/content/compose.py::substitute_storage_mechanics`.

## Backend file structure

Each backend file is organized by procedure:

```
## [procedure-name]              e.g. ## update-episodic
### § op-name                    e.g. ### § append-sub-episode
<concrete steps for this backend>
### § op-name
...
```

The op names are defined by each procedure's own core (they are procedure-scoped, not a global namespace). Both backends MUST implement the same `§ op` set a procedure references — `markdown.md` with the git/file mechanics, `db.md` with the tool calls (or an explicit no-op + reason where the operation dissolves).

## Fidelity invariant

The **markdown** composition (`core + markdown.md §proc`) must preserve **every behavioral mechanic** of the pre-seam procedure — the fleet's markdown pathway must not change. Enforced by `tests/content/test_markdown_fidelity.py` (strict git-HEAD mechanic-line accounting) + a per-procedure before→after instruction map.
