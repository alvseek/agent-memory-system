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
- **last_verified**: "2026-08-20"
- **verified_by**: "meta"
- **update_trigger**: "when framework procedures, slash commands, wizard hierarchy, or setup steps change"
- **notes**: "Top-level framework README. 7Q-style: What Is This / How Do I Set It Up / How Do I Use It / How Does It Work Inside / What Decisions Were Made. First read for new contributors and agents. 2026-08-18: the Core Operational Commands table had drifted — it listed neither `/list-agents` nor `/wait-options`; all three (with the new `/create-agent`) are now present, core command set 15 -> 16. 2026-08-20: added a pointer note in the setup section warning that awakening's large identity file can be silently truncated by the Read cap, linking to the SETUP.md read-limit section."

### `ARCHITECTURE.md`

- **type**: architecture-overview
- **scope**: shared
- **roles**: []
- **status**: useful
- **tags**: [architecture, file-structure, loading-flow, memory-layers, wizard-hierarchy, core-memory-config]
- **last_verified**: "2026-08-17"
- **verified_by**: "meta"
- **update_trigger**: "when file structure changes, awakening flow changes, 5-layer memory layout changes, or wizard hierarchy changes"
- **notes**: "Single-deep architecture doc: file structure, agent + shared-memory directory layouts, awakening flow, 5-layer memory system, write procedures table, wizard protocol hierarchy. Core-memory section now documents the three split configurators (profile / env / orchestrator) and the single-writer rule for runtime files."

### `SETUP.md`

- **type**: other
- **scope**: shared
- **roles**: []
- **status**: useful
- **tags**: [setup, installation, environment, claude-code, codex, new-agent, remote-control]
- **last_verified**: "2026-08-20"
- **verified_by**: "meta"
- **update_trigger**: "when setup scripts change, supported environments change, or agent creation procedure changes"
- **notes**: "Step-by-step setup guide for Claude Code and Codex; includes environment setup, tool output token limits, Remote Control, manual setup, and creating new agents. 2026-08-18: the Creating New Agents section was rewritten around `/create-agent` — it previously gave a three-step manual recipe whose `cp -r new-agent-template agent-[DOMAIN]` wrongly copied the fleet-wide `shared-memory/` into the agent; the manual steps are now demoted to a recovery path pointing at the two storage-backend files. 2026-08-20: a Remote Control section was added covering `remoteControlAtStartup: false`, the project-level override that wins in the disabling direction, and the fact that the Claude Code settings step now writes the key itself. 2026-08-20: the Claude Code Read Tool Limit subsection was rewritten to lead with the stable `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` env var (keeping the `tengu_amber_wren` Statsig flag as the automated alternative) and open with the silent-truncation-hits-awakening rationale. 2026-08-20 (later): the same subsection was corrected once the setup script actually gained the env var — the Statsig flag is now labelled a **fallback** rather than the automated route, with the limitation that the script can only raise a flag that already exists and never create one; the step summary was updated to name both levers."

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

### `procedures/components/core-instruction-control-files.md`

- **type**: other
- **scope**: shared
- **roles**: []
- **status**: useful
- **tags**: [awakening, component, inlined, user-profile, shared-memory]
- **last_verified**: "2026-08-15"
- **verified_by**: "meta"
- **update_trigger**: "when awakening protocol changes, phase structure changes, or user profile schema changes"
- **notes**: "The phased awakening protocol (Phase 1 identity + Phase 2 central context & report) and the user-profile precondition. A **component**, not a file agents load: inlined into /awaken-agent and /refresh-memory at compile time, which is why the awakening set is 4 memory files rather than 5. Moved here from the repo root 2026-08-15."

### `procedures/components/README.md`

- **type**: other
- **scope**: shared
- **roles**: []
- **status**: useful
- **tags**: [components, contract, inlining, compile, dry]
- **last_verified**: "2026-08-15"
- **verified_by**: "meta"
- **update_trigger**: "when the component model changes (what qualifies, file shape, reference form, or delivery)"
- **notes**: "Component contract: what qualifies as a component vs a command/template/seam section, the header + `---` + body file shape, the `components/<name>.md` link form, and delivery (inlined before seam substitution by inline.py, imported by both compile-procedures.py and Munnin's ContentLoader)."

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
