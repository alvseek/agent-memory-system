---
project: "agent-memory-system"
description: "Orientation map for the agent-memory-system framework — index of READMEs, architecture, setup, MCP, contributing, the shared control-instruction dispatcher, and framework standards."
created: "2026-06-15"
last_full_scan: "2026-06-15"
---

# Orientation Map — agent-memory-system

Index of orientation artifacts in this framework submodule. Used by agents at awakening (load into session context) and wrap-up (refresh entries the session touched) via the `/map-orientation` skill.

## Status Legend

- **useful** — current, accurate, future tasks will rely on it. Update when scope changes.
- **stale-but-valuable** — could be useful if updated. Repair on demand when next task hits its scope.
- **obsolete** — neither current nor valuable. Ignore. Optional: archive or delete.
- **unverified** — mtime changed since `last_verified`, or never verified. Next task touching its scope verifies and updates status.

## Scope Legend

- **shared** — relevant to every role on this project. Always loaded.
- **role-private** — relevant only to roles listed in `roles`. Other roles skip.
- **cross-readable** — relevant to roles listed in `roles`, PLUS Architect and QA always (cross-cutting roles read everything).

## Type Legend

- **7q-readme** — 7 Questions Framework README (any scope: root, module, sub-component)
- **architecture-map** — project-wide architecture navigation doc (ARCH-map.md style)
- **architecture-overview** — single-section architecture deep-dive (ARCH-overview, ARCH-domain-*, etc.)
- **flow-diagram** — Mermaid or similar diagram showing data/control flow (`.mmd`, `.mermaid`)
- **adr** — Architecture Decision Record (single decision document)
- **orientation-map-link** — pointer to a child orientation map for a sub-project (fractal scaling). The `child_map` field names the sub-map file.
- **other** — orientation artifact that doesn't fit above categories (CONTRIBUTING.md, GLOSSARY.md, etc.)

## Note on Creation

The agent who runs `/map-orientation create` for the first time scans ALL orientation docs in the project regardless of its own role. Creation is role-blind by necessity — the map must be complete for future agents of every role to filter against it. Role filtering applies at CONSUMPTION (which target docs each role actually reads), not creation.

---

## Entries

### `README.md`

- **type**: 7q-readme
- **scope**: shared
- **roles**: []
- **status**: useful
- **tags**: [overview, entry-point, framework]
- **last_verified**: "2026-08-14"
- **verified_by**: "meta"
- **update_trigger**: "when framework procedures, slash commands, wizard hierarchy, or setup steps change"
- **notes**: "Top-level framework README. 7Q-style: What Is This / How Do I Set It Up / How Do I Use It / How Does It Work Inside / What Decisions Were Made. First read for new contributors and agents."

### `ARCHITECTURE.md`

- **type**: architecture-overview
- **scope**: shared
- **roles**: []
- **status**: useful
- **tags**: [architecture, file-structure, loading-flow, memory-layers, wizard-hierarchy, core-memory-config]
- **last_verified**: "2026-08-15"
- **verified_by**: "meta"
- **update_trigger**: "when file structure changes, awakening flow changes, 5-layer memory layout changes, or wizard hierarchy changes"
- **notes**: "Single-deep architecture doc: file structure, agent + shared-memory directory layouts, awakening flow, 5-layer memory system, write procedures table, wizard protocol hierarchy. Core-memory section now documents the three split configurators (profile / env / orchestrator) and the single-writer rule for runtime files."

### `SETUP.md`

- **type**: other
- **scope**: shared
- **roles**: []
- **status**: useful
- **tags**: [setup, installation, environment, claude-code, codex, new-agent]
- **last_verified**: "2026-08-14"
- **verified_by**: "meta"
- **update_trigger**: "when setup scripts change, supported environments change, or agent creation procedure changes"
- **notes**: "Step-by-step setup guide for Claude Code and Codex; includes environment setup, tool output token limits, manual setup, and creating new agents."

### `MCP.md`

- **type**: other
- **scope**: shared
- **roles**: []
- **status**: unverified
- **tags**: [mcp, integrations, database, postgres, google-toolbox]
- **last_verified**: ""
- **verified_by**: ""
- **update_trigger**: "when MCP server recommendations change or new integration patterns emerge"
- **notes**: "MCP setup guide: gives agents direct access to databases, APIs, and tools. Documents Google's MCP Toolbox for Databases as the recommended Postgres server."

### `CONTRIBUTING.md`

- **type**: other
- **scope**: shared
- **roles**: []
- **status**: unverified
- **tags**: [contributing, guidelines, scope, license]
- **last_verified**: ""
- **verified_by**: ""
- **update_trigger**: "when contribution rules, scope, or license change"
- **notes**: "Contribution guide for the public agent-memory-system framework: ways to contribute, guidelines, scope, license."

### `core-instruction-control-files.md`

- **type**: other
- **scope**: shared
- **roles**: []
- **status**: unverified
- **tags**: [awakening, dispatcher, user-profile, shared-memory]
- **last_verified**: ""
- **verified_by**: ""
- **update_trigger**: "when awakening protocol changes, phase structure changes, or user profile schema changes"
- **notes**: "Shared dispatcher loaded by every agent at awakening. Holds the phased awakening instructions and the user profile section; dispatches to shared-memory/core-reasoning-memory.md and shared-memory/core-knowledge-memory.md."

### `docs/document-quality-standard.md`

- **type**: other
- **scope**: shared
- **roles**: []
- **status**: unverified
- **tags**: [standard, document-quality, lean, clear, precise, self-contained]
- **last_verified**: ""
- **verified_by**: ""
- **update_trigger**: "when writing or reviewing framework prose; when new sub-rules emerge (e.g., new leaky-abstraction patterns)"
- **notes**: "Document Quality Standard: lean / clear / precise / self-contained rules for all framework prose, plus the no-cross-procedure-step-numbers sub-rule and a review checklist."

---

## How to Use This File

**Agents at awakening**: Loaded into session context automatically by `/map-orientation` (bare call). Reference entries by `path` when consulting orientation docs for a task. The role-filter rules:

- Architect / QA → load + consult ALL entries (cross-cutting roles)
- Other roles → load + consult `scope: shared` + `scope: role-private/cross-readable` where your role is in the `roles` array

For `type: orientation-map-link` entries: if the entry passes the role filter, ALSO load the child map.

**Agents at wrap-up**: If your session updated any orientation doc, `/map-orientation --session-touched [paths]` updates its `last_verified` date and status. If your session DISCOVERED that an entry's status is wrong (useful doc is actually stale, obsolete doc is actually still valuable), update the entry directly via `/update-project-context`.

**Humans reviewing**: Spot-check `verified_by` and `update_trigger` fields. Spot-check `scope` and `roles` assignments — auto-guess from path heuristic may need correction.
