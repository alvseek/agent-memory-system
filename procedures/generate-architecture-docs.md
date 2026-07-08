# Generate Architecture Docs

Generate an **architecture doc** — a Mermaid diagram of a project's *component/structure* lens (components, boundaries, how they connect + deploy) wrapped in a short markdown doc — by resolving a scope, synthesizing the structure from static signals, and placing the doc per the ADR-004 contract.

An architecture doc is one of the **atomic doc types** (the third + final). Its siblings: `/generate-readme` (what a unit *is*), `/generate-flow-docs` (behavior over time), `/generate-domain-docs` (data model). A future `/generate-docs` orchestrator composes them.

This skill is **fractal** (like `/generate-readme`): the scope picks the altitude —
- whole-project scope → an **architecture-map** (the system's components + how they connect)
- a subsystem scope → an **architecture-overview** (that subsystem's internal structure)

See [ADR-007](//@agent-memory/docs/adr/2026-07-08-doc-altitudes-and-three-layer-map-model.md) for the two-altitude + 3-layer model.

## Arguments

`$ARGUMENTS`

- `/generate-architecture-docs` (bare) or `/generate-architecture-docs project` → an **architecture-map** of the whole system.
- `/generate-architecture-docs [subsystem]` → an **architecture-overview** of that subsystem (a module / service / bounded area path).

One doc per run. To document several subsystems, run it per subsystem (a future `/generate-docs` orchestrator will batch this).

---

## Procedure

### Step 1: Resolve the scope + altitude

- **Bare / `project`** → altitude = **architecture-map** (whole system).
- **A subsystem path arg** → altitude = **architecture-overview** of that subsystem. If the arg is ambiguous (matches several areas), ask [USER-NAME] which one.

Filter out already-documented scopes: glob `**/docs/architecture/*.md`, read their `scope:` frontmatter / titles, and don't regenerate one that exists (update instead).

### Step 2: Synthesize the structure + readability health-check

There is **no single authoritative source** (no entrypoints, no entity classes) — synthesize from the static signals, bounded to the resolved scope:

- **Top-level folders / module boundaries** — the coarse structure (a hint, not the truth).
- **Import / dependency graph** — what actually depends on what (the *real* boundaries; prefer this over folder layout when they disagree).
- **Deployment & service config** — `docker-compose`, k8s manifests, serverless config, `Procfile` — reveals the runtime components + topology.
- **Monorepo workspaces** — `apps/`, `packages/`, workspace manifests.
- **Tech-stack manifests** — `package.json`, `*.csproj`, `requirements.txt`, `go.mod` — per-component stacks.

Identify **components** (services / modules / layers), their **responsibilities**, **boundaries**, and the **dependencies / data-flow between them** (sync vs async, which talks to which DB/queue). Mark inferred boundaries `[CONFIRM]`; missing infra `[NOT FOUND]` (no deployment config → say so, don't invent a topology).

**Readability health-check**: for an architecture-map, if the system has **more than ~15–20 top-level components**, STOP and recommend splitting into per-subsystem `architecture-overview` docs rather than one unreadable map. Judgment trigger, not a hard cap — recommend, let [USER-NAME] decide.

### Step 3: Select the diagram grammar

| Shape | Grammar |
|---|---|
| Component / dependency graph (the common case) | `flowchart` (default) |
| Formal system with clear external actors + containers | `C4Context` / `C4Container` |

Default to `flowchart` unless C4 clearly fits (Mermaid's C4 support is newer/less universal).

### Step 4: Compute placement (LCA)

- **architecture-map** → project root `docs/architecture/{project}.md` (inherently project-wide).
- **architecture-overview** → the subsystem's **LCA** `docs/architecture/{subsystem}.md` (collect the subsystem's file paths → nearest existing common ancestor).

Use the nearest *existing* ancestor — never invent a parent folder. Create `docs/architecture/` at the target if it doesn't exist.

> **Placement Contract** (see [ADR-004](//@agent-memory/docs/adr/2026-07-06-docs-placement-contract.md)): **scope = location.** The doc lives in the **project's own tree**, never in agent-memory memory (`.agents/`).

### Step 5: Fill the doc

1. Copy [architecture-doc-template.md](//@agent-memory/control-files/templates/architecture-doc-template.md) to the target path.
2. Set `doc_type` per altitude (`architecture-map` or `architecture-overview`), update `scope:` + the `# Architecture: …` heading.
3. Remove the Convention preamble block.
4. Fill from the synthesis:
   - **Altitude / Scope / Type / Components** — the altitude, boundary, chosen grammar + why, component count + names.
   - **Diagram** — the `flowchart`/C4 (label edges with *how* components talk; show boundaries).
   - **Components** — responsibility + boundary + location per component.
   - **Dependencies & Boundaries** — how they connect, deployment topology, key cross-boundary contracts (the part only this doc gives).
   - **Related** — subsystem overviews (from a map), module READMEs, relevant flow/domain docs, architecture ADRs.

**Accuracy discipline** (inherited from [generate-readme](//@agent-memory/control-files/procedures/generate-readme.md)): fill from actual structure, never invent a component or a connection. Use `[TODO]` / `[CONFIRM]` / `[NOT FOUND]`. An incomplete architecture doc is better than a fictional one.

### Step 6: Present for review

Present the architecture doc to [USER-NAME]:
- Show the diagram + prose.
- Group outstanding markers by type.
- State the placement, the **altitude** (map vs overview), and whether the health-check recommended a split.
- Ask if anything needs adjustment.

> **Vector export** (optional): extract the fenced Mermaid block to `{scope}.mmd` and run `mmdc -i {scope}.mmd -o {scope}.svg` (or `.pdf`).

---

## Integration With Other Procedures

- **[generate-flow-docs](//@agent-memory/control-files/procedures/generate-flow-docs.md) / [generate-domain-docs](//@agent-memory/control-files/procedures/generate-domain-docs.md) / [generate-readme](//@agent-memory/control-files/procedures/generate-readme.md)** — sibling atomic doc generators. Same shape: resolve → extract/synthesize → fill → review.
- **[map-orientation](//@agent-memory/control-files/procedures/map-orientation.md)** — indexes the generated doc as `architecture-map` or `architecture-overview` (via the `doc_type` frontmatter). This skill does **not** run the map — indexing is `/wrap-up` or an explicit `/map-orientation --rescan`.
- **The 3-layer model** ([ADR-007](//@agent-memory/docs/adr/2026-07-08-doc-altitudes-and-three-layer-map-model.md)): this doc is a **map-altitude content artifact** — cleanly separate from the *orientation map* (navigation), which indexes it. The orientation map maps *docs*; an architecture-map maps the *system*.
- **Future `/generate-docs` orchestrator** — composes this with the other atomic generators. See [ADR-006](//@agent-memory/docs/adr/2026-07-07-doc-generation-family-architecture.md).
- **Decision collection** — if Step 1 resolution is ambiguous, present the candidates using [wait-options](//@agent-memory/control-files/procedures/wait-options.md).

---

## Anti-Patterns

1. **Inventing components or connections.** If the structure/config doesn't show it, it doesn't go in the diagram. `[CONFIRM]` / `[NOT FOUND]`, never fabricate.
2. **Mixing altitudes.** A map with class-level internals is unreadable; an overview that's just "here's the whole system" is useless. Map = components; overview = one subsystem's internals.
3. **Listing modules instead of showing relationships.** The value is *how components connect + deploy* — a bare list is what the orientation map + READMEs already give.
4. **Trusting folders over the dependency graph.** Folder layout is a hint; actual imports + deployment are the real boundaries.
5. **Inventing a parent folder for placement.** Use the nearest *existing* common ancestor.
6. **Runtime introspection.** Synthesize from static code/config, not a running system.
7. **Auto-running the orientation map.** Generate + report only.
8. **Re-documenting an existing scope.** The scan filters out documented scopes — update, don't regenerate.
