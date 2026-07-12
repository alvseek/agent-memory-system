# Localize Context

Graduate a **consenting** project's orientation map + *structural* project-context OUT of the central `@agent-memory` store and INTO the project's own repository (`docs/`). One-time, forward-only. See [ADR-005](//@agent-memory/docs/adr/2026-07-06-project-local-memory-externalization.md).

**The load-bearing rule**: only **code-describing** artifacts localize. Episodic, emotional, relationship, business/strategy, and role-private domain memory **stay fleet-private and central, always**. Leaking those into a (client) repo is the failure this procedure exists to prevent.

---

## Arguments

`$ARGUMENTS`

- `/localize-context` — Localize the **current** project (detect from cwd).
- `/localize-context [project-name]` — Target the named project instead of cwd detection.
- `/localize-context --status` — Report whether the current project is localized (read-only). No move.

---

## What Localizes (safety boundary)

| Localizes → `docs/` | Stays central (fleet-private) |
|---|---|
| Orientation map (`orientation-map.md`) | Episodic memory (`agent-[domain]/episodes/`) |
| Structural project-context: architecture overviews, module docs, conventions, flow descriptions, ADR indexes | Emotional / relationship memory |
| | Business / strategy / commercialization context |
| | Role-private domain knowledge (`agent-[domain]/knowledge-base/[project]/`) |
| | Any context file holding secrets, OAuth, credentials, or internal fleet design |

**Ambiguous → ASK.** Never auto-move a file whose classification isn't obviously code-describing.

---

## Step 1: Identify project + guard

1. **Identify project** — from `[project-name]` arg, else infer from cwd (same detection as `/map-orientation` Prelude).
2. **Resolve central paths**:
   - Central map: `//@agent-memory/shared-memory/[PROJECT-NAME]/context/orientation-map.md`
   - Central context dir: `//@agent-memory/shared-memory/[PROJECT-NAME]/context/`
   - Project root: the project's working directory on disk (cwd for the active project).
3. **Guards** (STOP + report if any fail):
   - Central map missing → *"No orientation map for [PROJECT] yet — run `/map-orientation create` first, then localize."*
   - Central map already has `home: project` → *"[PROJECT] is already localized (`docs/orientation-map.md`)."* Exit.

> `--status` mode stops here: report localized (map `home: project`) or central-only, then exit.

## Step 2: Consent gate + `AGENTS.md`

1. **Confirm consent** — one explicit confirmation from [USER-NAME]: *"Localize [PROJECT] into its own repo? This moves the map + structural context into `<project-root>/docs/` and leaves a central stub. Confirm the project is agreed to host AI artifacts."* Wait.
2. **Root `AGENTS.md`**:
   - Present at `<project-root>/AGENTS.md` → will **append** the pointer section (skip if already present — idempotent).
   - Missing → create a minimal `AGENTS.md` (house-rules stub + the pointer section). Confirm creation.
3. **Append the prose pointer** (never a boolean flag — the standard is prose sections):

   ```markdown
   ## Agent Orientation
   This repo maintains a structured orientation map at `docs/orientation-map.md`.
   Load it before starting work for architecture and navigation context.
   ```

## Step 3: Classify central context files

1. List `*.md` in the central context dir (exclude `orientation-map.md` and `context-index.md` — handled separately).
2. Classify each per [What Localizes](#what-localizes-safety-boundary): **localize** (code-describing) vs **stay** (fleet-private).
3. **Present the full classification for confirmation BEFORE any move** — this is the safety pause:

   ```
   Localization plan for [PROJECT]:
     MOVE → docs/:   [file] — [why structural]
     STAY central (private):    [file] — [why fleet-private]
     AMBIGUOUS (confirm):       [file] — [both readings]
   ```
   Wait for [USER-NAME] to confirm / reclassify. Do NOT move anything until confirmed.

## Step 4: Create `docs/` layout

- `mkdir -p <project-root>/docs`

## Step 5: Move + rebase the orientation map

1. **Copy** central map → `<project-root>/docs/orientation-map.md`.
2. **Frontmatter**: keep `project` / `description` / `created` / `last_full_scan`; add `source_of_truth: project`.
3. **Rebase paths** (two different bases — don't conflate):
   - **Doc `path` references** stay **project-root-relative** — the agent resolves them from the repo root (cwd), exactly as the central map already did (a central map's `README.md` entry never meant `shared-memory/.../context/README.md`). → unchanged.
   - **`child_map` sub-links** are relative to the **map file's folder**. The map now lives at `docs/`, so rewrite the old central-context form (`../../../[sub]/orientation-map.md`) to `docs/`-relative: `../[sub]/orientation-map.md` (one `..` climbs from `docs/` to the repo root, then descends into the sub-project). This keeps `/map-orientation` Load Mode L2 (which follows `child_map` relative to the parent map's location) working unchanged.
4. **Delete** the central map only after the copy is verified (it's replaced by the stub in Step 7).

## Step 6: Move classified context + indexes

1. For each **localize**-classified file: copy → `<project-root>/docs/[file]`, then delete the central original.
2. **In-project index**: create `<project-root>/docs/context-index.md` (header `# [PROJECT] Project Context`) with the moved entries.
3. **Central index**: remove moved entries from the central `context-index.md`. Files classified **stay** remain listed centrally and physically in place.

> **Atomicity**: this move is not atomic across the two repos. If interrupted, report partial state (which files copied vs deleted) and finish manually — same discipline as `/update-project-context` Move-to-Shared.

## Step 7: Write the central stub

Replace the central `orientation-map.md` with a **stub** (breadcrumb + machine-branch signal — NOT the real entries):

```yaml
---
project: "[PROJECT-NAME]"
home: project
localized_path: docs/orientation-map.md
created: "[original created]"
localized_on: "[TODAY-DATE]"
---

# Orientation Map — [PROJECT-NAME] (localized)

This project's orientation map + structural context live **in the project repo** at
`docs/orientation-map.md` (source of truth). This central file is a stub;
resolution keys off the project root (cwd) — see Localized Home Resolution.

### `docs/orientation-map.md` (in-project)
- **type**: orientation-map-link
- **home**: project
- **child_map**: (resolved at project root, not relative to this store)
- **notes**: "Localized [TODAY-DATE]. Load via /map-orientation (home: project resolution)."
```

## Step 8: Report

Summarize: files moved vs stayed (with reasons), `AGENTS.md` updated/created, stub written. Remind [USER-NAME]:
- Commit `docs/` + `AGENTS.md` in the **project** repo.
- Commit the stub + index changes in the **`@agent-memory`** repo.

---

## Localized Home Resolution

**The canonical rule** — defined here once, consumed by `/map-orientation` (all modes) and `/update-project-context` (shared scope). Never applies to private domain knowledge, episodic, or emotional memory (always central).

Given a project:

1. Detect project; compute central map path `shared-memory/[project]/context/orientation-map.md`.
2. **Central map missing** → not localized → central-only defaults.
3. **Read central map frontmatter**:
   - `home: project` present →
     - `project_root` = the project's working directory (cwd for the active project)
     - `map_path` = `<project_root>/<localized_path>` (default `docs/orientation-map.md`)
     - `context_home` = `<project_root>/docs/`
     - `source_of_truth` = `project`
   - else →
     - `map_path` = `shared-memory/[project]/context/orientation-map.md`
     - `context_home` = `shared-memory/[project]/context/`
     - `source_of_truth` = `central`
4. Consumers operate on `(map_path, context_home)`. Resolution keys off **cwd**, never an absolute or cross-store relative path — this is what makes localization machine-portable across the different filesystem locations of the fleet store vs a client repo.

---

## Non-Goals (this iteration)

- **De-localization / reversal** — forward-only. Add a reverse flow only if a real engagement needs it.
- **Localizing episodic / emotional / relationship / business memory** — the safety boundary; these never localize.
- **Sub-map fractal localization** — the root map + its context localize; existing sub-maps keep their placement.

## Integration With Other Procedures

- **[map-orientation](map-orientation.md)** — consumes Localized Home Resolution in its Prelude (all modes read/write the resolved paths).
- **[update-project-context](memory/update-project-context.md)** — shared scope consumes the resolution; private scope is never localized.
- **[wrap-up](wrap-up.md)** — inherits via `/map-orientation --session-touched` (no direct change).
- **[awaken-agent](awaken-agent.md)** — Phase 2 resolves the localized **shared context-index** via Localized Home Resolution (reads `<project-root>/docs/context-index.md` when `home: project`); the orientation map is resolved separately by `/map-orientation` (bare) at load.

## Anti-Patterns

1. **Moving fleet-private memory into a repo** — episodic/emotional/business/strategy/role-private never localize.
2. **Dual home** — leaving a full central map AND an in-project map. Central must become a stub.
3. **Boolean consent flag in `AGENTS.md`** — use presence + a prose pointer; a boolean duplicates filesystem state and can lie.
4. **Absolute or cross-store relative paths in the stub** — breaks portability; resolution keys off cwd.
5. **Auto-moving ambiguous files** — classification pauses for confirmation; never move on assumption.
