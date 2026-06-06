# Map Orientation

Maintain a per-project index of orientation artifacts (READMEs, architecture docs, flow diagrams, ADRs, sub-project maps) with staleness + role tracking. Self-contained skill: handles check / load / mtime-refresh / session-touched updates in one entry point. **Creation is explicit (`create` arg), never automatic** — matches framework pattern (`/generate-readme`, `/setup-fleet`, `/setup-qa-instrument` are all user-invoked).

Called automatically by `/awaken-agent` (Step 12, load-only) and `/wrap-up` (with `--session-touched` arg). Explicitly invoked by user with `create` or `--rescan` for write operations.

The map file lives at `shared-memory/[project]/context/orientation-map.md`. Sub-project maps use flat-suffix naming in the same folder. Format template: [orientation-map-template.md](../templates/orientation-map-template.md).

---

## Arguments

`$ARGUMENTS`

- `/map-orientation` → **Load mode (default, read-only).** If map exists: load + mtime check + write only if entries flagged stale. If map missing: report "no map yet — run `/map-orientation create` to scan and create." **Never auto-creates.**
- `/map-orientation create` → **Create mode (explicit, user-invoked).** Full scan + create map + load. Use when first setting up orientation tracking for a project.
- `/map-orientation --session-touched [path1,path2,...]` → **Wrap-up mode.** Update the specified entries' `last_verified` and status based on session knowledge. If map missing: silent no-op.
- `/map-orientation --rescan` → **Force full rescan.** Only valid if map exists. For explicit refresh after major project restructure.
- `/map-orientation [project-name]` → **Specific project.** Operate on the named project (overrides cwd-based detection).

---

## Procedure

### Step 1: Determine Current Project

Identify which project the map covers:

- **From working directory**: Match cwd against known project mappings (cross-reference `shared-memory/integrations/external-integrations.md` "project ↔ task system mapping" or `shared-memory/[project]/` folder existence)
- **From argument**: If a project name is passed, use it
- **If neither matches**: Skip silently. Not all sessions are project-scoped (e.g., framework-level meta work).

Set `[PROJECT-NAME]` for subsequent steps.

### Step 2: Compute Map Path

Root map path: `//@agent-memory/shared-memory/[PROJECT-NAME]/context/orientation-map.md`

Verify the `shared-memory/[PROJECT-NAME]/context/` folder exists. If not (during `create` mode only), create it (`mkdir -p`).

### Step 3: Branch on Mode + Existence

| Mode (arg) | Map exists? | Action |
|---|---|---|
| bare (default) | Yes | **Load Mode** (Step 8) |
| bare (default) | No | **Report and exit**: "No orientation map for [PROJECT-NAME] yet. Run `/map-orientation create` to scan and create." |
| `create` | Yes | **Confirm with user**: map already exists, do you mean `--rescan`? Wait for explicit confirmation. |
| `create` | No | **Create Mode** (Step 4) |
| `--session-touched` | Yes | **Load Mode + Session-Touched Update** (Step 8 + Step 10) |
| `--session-touched` | No | **Silent no-op**. Nothing to update. |
| `--rescan` | Yes | **Create Mode** (Step 4) — full rescan, overwriting entries (preserve existing status/verified_by where path unchanged) |
| `--rescan` | No | **Report and exit**: "No map to rescan. Run `/map-orientation create` first." |

---

## Create Mode

> **Triggered only by explicit `create` or `--rescan` args.** Never runs automatically at awakening.

### Step 4: Scan for Orientation Artifacts

Discover orientation artifacts in the project root:

**File patterns** (case-insensitive):
- `README*.md` — any README variant (README.md, README-deployment.md, README-architecture.md)
- `ARCH*.md` — architecture docs (ARCH-map.md, ARCH-overview.md, ARCH-domain-*.md)
- `ADR-*.md` or `*-adr.md` — architecture decision records
- `*.mmd`, `*.mermaid` — flow diagrams in Mermaid format
- `CONTRIBUTING.md`, `GLOSSARY.md`, `CHANGELOG.md` — optional, captured as `type: other`

**Scan scope**:
- Project root (depth 1)
- `/docs/` recursive
- Optional submodule roots (depth 1 each) — for monorepos / multi-submodule projects

**Skip patterns**:
- `.git/`, `node_modules/`, `vendor/`, `build/`, `dist/`, `.next/`, `target/`, `bin/`, `obj/`
- Hidden folders starting with `.` (except `.github/` if it contains workflow docs)

### Step 4a: Detect Sub-Projects (Hierarchical Maps)

After the root scan, check for sub-project structure that warrants its own sub-map:

**Sub-map triggers** (any of):
- `.gitmodules` file at project root (git submodules detected)
- Sub-folder under common monorepo patterns (`apps/`, `services/`, `packages/`, `submodules/`) with ≥5 orientation docs

For each detected sub-project:
- Present to user: "Sub-project `apps/api/` has 8 orientation docs. Create sub-map `orientation-map-api.md`? [y/n]"
- If yes:
  - Recursive scan within sub-project boundary (using same Step 4 patterns)
  - Create sub-map at `shared-memory/[PROJECT-NAME]/context/orientation-map-[subproject].md`
  - Root map gets an `orientation-map-link` entry pointing to the sub-map (see Step 7)
- If no: docs remain entries in the root map

### Step 5: Extract Purpose Per File

For each found file, extract a 1-line purpose:

- **Markdown files**: First non-trivial paragraph after the title heading (skip "Table of Contents", "Status", or empty lines)
- **Mermaid files**: First comment block, or the diagram title if present
- If extraction fails: leave purpose as `[unverified - needs read]`

Do NOT read full file content during scan. Purpose extraction should be cheap (head -20 or first 500 chars).

### Step 6: Classify Type, Scope, and Roles (Heuristic)

Per file, assign:

**Type** (based on path + filename):

| Filename pattern | Type |
|---|---|
| `README*.md` (root or module) following 7Q structure (≥4 of 7 questions present) | `7q-readme` |
| `README*.md` without 7Q structure | `other` (with note "non-7Q README") |
| `ARCH-map.md` or `architecture-map.md` | `architecture-map` |
| `ARCH-*.md` (domain/overhead/governance overviews) | `architecture-overview` |
| `*.mmd`, `*.mermaid` | `flow-diagram` |
| `ADR-*.md` or `*-decision.md` | `adr` |
| Sub-map reference (from Step 4a) | `orientation-map-link` |
| Anything else | `other` |

**Scope + Roles** (role-blind creation, path-heuristic guess):

| Path pattern | Scope | Roles |
|---|---|---|
| Root-level docs (`README.md`, `docs/architecture/*`, `docs/decisions/*`) | `shared` | `[]` |
| `apps/api/`, `backend/`, `server/`, `api/` paths | `role-private` | `[backend]` |
| `apps/web/`, `frontend/`, `client/`, `web/` paths | `role-private` | `[frontend]` |
| `apps/mobile/`, `mobile/`, `ios/`, `android/` paths | `role-private` | `[mobile]` |
| `apps/admin/`, `admin/` paths | `role-private` | `[admin]` |
| `docs/integration-*`, `docs/contracts/`, `*-contract.md` | `cross-readable` | best guess from path (e.g., `[backend, frontend]` for FE-BE contracts) |
| Ambiguous paths | `shared` (default) with note "auto-classified — verify scope" |

User can override after scan via direct edit or future `/update-project-context` call. Default-then-edit pattern.

### Step 7: Write Initial Map (and Sub-Maps)

Copy the [orientation-map-template.md](../templates/orientation-map-template.md) to the root map path, then populate with discovered entries:

```yaml
---
project: "[PROJECT-NAME]"
description: "..."
created: "[TODAY-DATE]"
last_full_scan: "[TODAY-DATE]"
---
```

Per entry, initial values:
- **status**: `unverified` (no agent has verified yet)
- **last_verified**: empty (will be set on first verification)
- **verified_by**: empty
- **update_trigger**: empty (filled when verified)
- **notes**: the 1-line purpose extracted in Step 5
- **scope** + **roles**: from Step 6 heuristic

For each sub-map created in Step 4a:
- Write the sub-map file at `shared-memory/[PROJECT-NAME]/context/orientation-map-[subproject].md`
- Root map gets an entry of `type: orientation-map-link` with `child_map: orientation-map-[subproject].md`

Proceed to Step 13.

---

## Load Mode

### Step 8: Read Map File

Read the existing `orientation-map.md` file. Parse its entries.

This step LOADS the map into session context — that's the value of awakening-time invocation. Agent now has the orientation index available for all subsequent task work in this session.

For each `orientation-map-link` entry: if the agent's role passes the role filter for that entry (or agent is Architect/QA), ALSO load the child map.

**If child map referenced but file missing**: Flag the entry with `[child map missing — run /map-orientation --rescan when ready]`. Continue loading the rest. Do not auto-create.

### Step 9: mtime Check (Cross-Session Staleness)

For each entry in the map, compare the file's actual modification time to the entry's `last_verified` date:

```sh
stat -c %Y "[entry-path]"  # actual mtime (Unix timestamp)
```

If `file_mtime > last_verified_date`:
- Mark the entry's status as `unverified`
- Add a `staleness_reason: "mtime > last_verified"` field (optional, for audit)

If the file no longer exists at the recorded path:
- Mark the entry as `obsolete` with `notes: "file no longer exists at path"`
- Do not delete the entry — serves as breadcrumb if path is restored

### Step 10: Apply Session-Touched Updates (if `--session-touched` arg)

If called with `--session-touched [path1,path2,...]`:

For each path in the argument:
- Find the matching entry in the map (or add new entry if not present)
- Update `last_verified` to today's date
- Update `verified_by` to `[current-agent-role] / [session context]`
- Prompt the agent (or auto-set if obvious) to confirm status (useful / stale-but-valuable / obsolete)
- Update `notes` if session generated relevant info

### Step 11: Write Updated Map (if changed)

If any entries changed in Step 9 or Step 10:
- Write the updated map back to disk
- Update `last_full_scan` ONLY if a full rescan occurred (not for mtime checks or session-touched updates)

If no changes: skip the write. No-op is the goal.

### Step 12: Confirm Loaded

Confirm the map is now in session context. Subsequent task work in this project can reference entries by path without re-reading.

---

## Step 13: Report to User

Brief report regardless of mode:

```
Orientation map [created/loaded/updated]: shared-memory/[PROJECT-NAME]/context/orientation-map.md
  - N entries total
  - M unverified (need agent verification on next relevant task)
  - K stale-but-valuable | L obsolete
  - P sub-map links: [list of sub-map filenames]
```

If created from scratch, also note: "First-time map. Entries will be verified as future tasks touch their scope."

If load-mode found missing map: "No map yet for [PROJECT-NAME]. Run `/map-orientation create` when ready to scan + create."

---

## Templates

### Orientation Map File Template

See [orientation-map-template.md](../templates/orientation-map-template.md) — defines the frontmatter + entry schema with all type/scope/role combinations.

---

## Integration With Other Procedures

- **[awaken-agent](awaken-agent.md)** Step 12 (Aware Current Project): after project detection, call `/map-orientation` (bare). Map loads into session context if it exists. If missing, report and proceed (no auto-create).
- **[wrap-up](wrap-up.md)**: after episodic capture, call `/map-orientation --session-touched [paths]` with the orientation docs this session touched or referenced. Silent no-op if map doesn't exist.
- **[update-project-context](memory/update-project-context.md)**: if a session DISCOVERED that an orientation doc's status is wrong (e.g., a "useful" doc is actually obsolete), prefer direct edit via this procedure over `/map-orientation` arg — the map will pick up the change via mtime check on next awakening.

### Framework Pattern Compliance

This skill follows the framework's automatic-vs-explicit split:

| Op | Pattern | This skill |
|---|---|---|
| First creation | Explicit (`/generate-readme`, `/setup-fleet`, `/setup-qa-instrument`) | `/map-orientation create` |
| Recurring read | Automatic (awakening loads memory files) | Bare `/map-orientation` at awakening (load only) |
| Recurring write | Explicit (`/update-project-context`, `/update-episodic`) | `/map-orientation --session-touched` at wrap-up |

No surprise scans. Creation is always intentional.

---

## Role Filter Rules (Load Mode)

When loading the map, apply role filter per entry:

- `scope: shared` → load (everyone)
- `scope: role-private` → load if current agent's role ∈ `roles`, else skip
- `scope: cross-readable` → load if current agent's role ∈ `roles` OR current agent is Architect or QA (cross-cutting roles always)

**Architect and QA exception**: Both cross-read all entries regardless of scope (per May 29 3-zone project memory model). Their job is cross-cutting; restricting their view defeats the purpose of their role.

**Single-role projects** (undanganaku, tradingdata, agent-memory framework): all entries get `scope: shared, roles: []`. Role filter becomes a no-op. Same skill, same behavior — just simpler data.

---

## Re-evaluation Rules

- **mtime check is mandatory** on every Load Mode run. Skip risks the agent operating on stale assumptions.
- **Full rescan is rare**. Only via explicit `--rescan` after major project restructure (folders moved, conventions changed).
- **Status changes require evidence**. An entry shouldn't move from `unverified` to `useful` without an agent having actually read it during real task work — verification by inspection only, not by assumption.

---

## Anti-Patterns

1. **Auto-creating maps at awakening.** Violates framework pattern. Creation = explicit user action via `create` arg. Awakening loads only.
2. **Calling `/map-orientation` to "freshen things up" without specific session-touched paths.** That's a full mtime sweep — fine — but don't expect status changes without verification.
3. **Marking entries `useful` because they exist.** Useful means "verified accurate and future tasks will rely on it." Existence alone is not verification.
4. **Skipping the map at awakening because the agent feels confident.** The map also catches cross-session edits the agent doesn't know about.
5. **Bloating the map with every markdown file in the project.** Map covers ORIENTATION artifacts (README/architecture/flow/ADR/cross-cutting). Implementation docs, change logs, meeting notes don't belong here.
6. **Flattening submodule docs into the root map when sub-map makes sense.** If a sub-project has ≥5 docs, create a sub-map and link from root via `orientation-map-link` entry. Keeps root map navigable.
7. **Auto-creating child maps when parent's `orientation-map-link` points to missing file.** Flag and let user trigger `--rescan` when ready. Don't fire scans unexpectedly during task work.
