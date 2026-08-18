# Storage Backend — Markdown (git tree)

Concrete storage mechanics for the **native markdown-over-git** world. Each `## [procedure]` section defines the `§ op`s that procedure references. See the [seam contract](README.md).

> **Storage location (seam)**: paths **default to central** — `agent-[domain]/episodes/`, `agent-[domain]/knowledge-base/`, and `agent-memory-index.md`. Where a project's memory physically lives is decided by the storage-location resolver, which **defaults to central**; if a coding/environment add-on installed a **localized** resolver it overrides the resolved paths transparently — no change to the ops below.

---

## update-episodic

### § stamp-date

ALWAYS CHECK DATE TIME FIRST for the sub-episode H3 header and index entry placement:
`date '+%Y-%m-%d %H:%M'`

### § list-candidate-episodes

Read `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` and locate `# Recent Context Episodes`. Collect all entries where the filename or summary contains the **project name**. These are scan candidates. (Archived entries live in `archive/` and are intentionally out of reach.)

### § append-sub-episode

1. **Open the chosen file** in `[AGENT-MEMORY-PATH]/agent-[domain]/episodes/`.
2. **Insert the sub-episode H3 block at the TOP** (newest-first within the file), above any older H3 blocks. Sub-episodes are separated by `---`.
3. **Update the index entry — MOVE-TO-TODAY rule**:
   - Locate the existing entry for this file in the index.
   - Delete it from its current date group (if the group becomes empty, remove the group header too).
   - Insert at the **top of today's date group** (`📂 YYYY-MM-DD:`); create today's group if it doesn't exist.
   - Update the summary by appending `+ [new sub-topic]` (or rewriting it if the new sub-topic shifts the overall theme).

   > **Why move?** Awakening's project-scoped episodic load grabs the top entry as "latest episodic." The move preserves the "top = newest" invariant. Edit-in-place would leave a stale top entry and break awakening's selection logic.

### § create-episode

1. **Build filename**: `[project-name]-[context-theme].md` (no date prefix). Examples: `agent-memory-task-system-framework-rules.md`, `plko-jira-mcp-integration.md`. If a file at this name already exists (and a separate file is wanted), use an incrementing suffix: `[project-name]-[context-theme]-2.md`.
2. **Copy the file scaffold**:
   ```
   cp [AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/episodic-memory-template.md [AGENT-MEMORY-PATH]/agent-[domain]/episodes/[filename].md
   ```
3. **Replace the template placeholder** at the top with the composed sub-episode block.
4. **Add index entry**:
   - Insert at the **top of today's date group** (`📂 YYYY-MM-DD:`); create today's group if it doesn't exist.
   - Entry format: `- [filename.md](episodes/filename.md) - [one-line summary]`.

### § housekeeping

1. **Check line limit** after an append:
   - **> 500 lines**: warn — *"[filename] over 500 lines, consider splitting on next merge"*.
   - **> 1000 lines**: split — move the *just-added* sub-episode into `[project]-[theme]-2.md` (next incrementing suffix if `-2` exists). Add `> Continues from [original-filename]` at the top of the new file. Add a new index entry for the split file under today's date group.
2. **Lazy filename migration** (one-time per file): if the chosen file still uses the legacy `YYYY-MM-DD-HH.MM-[project]-[theme].md` format, rename it to `[project]-[theme].md` as part of this append and update the index entry's filename reference. If a file at the new name already exists (rare collision), use the line-limit `-{n}` suffix rule.

> **Episodes folder structure**:
> ```
> episodes/
> ├── [project-name]-[context-theme].md        # Active episode file (rolling per theme)
> ├── [project-name]-[context-theme]-2.md      # Split file when 1000-line cap hit
> ├── YYYY-MM-DD-HH.MM-[project]-[theme].md    # Legacy dated files (lazy migration)
> └── archive/                                  # Archived old episodes (via /archive-old-memories)
>     └── YYYY-archived-context.md
> ```
> Legacy filenames are migrated lazily — only renamed when the file gets its next merge-append. No bulk sweep.

### § template

The sub-episode block format → read `[AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/episodic-entry-template.md`.

---

## add-reasoning

### § read-reasoning-store

Read the `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` reasoning memory section (`# DOMAIN REASONING MEMORY`).

### § generate-uuid

Generate a unique identifier:
- **Windows**: `powershell -c "[guid]::NewGuid().ToString()"`
- **Linux/macOS**: `uuidgen` or `cat /proc/sys/kernel/random/uuid`

### § persist-reasoning

Write the completed pattern into the `# DOMAIN REASONING MEMORY` section of `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md`.

### § template

The reasoning-pattern block format → read `[AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/reasoning-pattern-template.md`.

---

## update-emotional

### § stamp-date

ALWAYS verify current date before writing:
`date '+%Y-%m-%d %H:%M'`

### § persist-emotional

Write the moment to `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` (in the `# DOMAIN EMOTIONAL MEMORY` section). **Order: NEWEST FIRST** — most recent entries at the TOP.

### § template

The emotional-moment block format (happy / sad / frustrated / bonding) → read `[AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/emotional-moment-template.md`.

---

## update-knowledge

### § persist-knowledge

Create in `[AGENT-MEMORY-PATH]/agent-[domain]/knowledge-base/research/` (domain expertise and research). Name the file `[date]-[descriptive-theme].md` or `[domain-area].md` — examples: `2025-09-11-nestjs-patterns.md` (dated research), `typescript-best-practices.md` (timeless domain knowledge). Create the file with the template structure.

### § update-knowledge-index

Update `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` knowledge directory — add an entry to the knowledge index for discoverability.

### § template

The knowledge-file format → read `[AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/knowledge-file-template.md`.

---

## load-episodic

### § list-episodes

Read `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` and locate `# Recent Context Episodes`. Parse entries — each `📂 YYYY-MM-DD:` group holds `- [filename.md](episodes/filename.md) - summary`, newest-first. File path = `episodes/[filename.md]`.

### § load-episode-body

Read the selected episode file(s) from `[AGENT-MEMORY-PATH]/agent-[domain]/episodes/` using the Read tool.

---

## load-knowledge

### § list-knowledge

Read `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` and locate `# Core Knowledge Base`. Parse entries — `### **[Topic Group]**` headers over `- **[Title](path)** - description`. File path from the markdown link. Exclude any "Project Context Files" subsection (overlay concern).

### § load-knowledge-body

Read the selected file(s) from `[AGENT-MEMORY-PATH]/agent-[domain]/knowledge-base/` using the Read tool.

---

## archive-old-memories

### § stamp-date

`date '+%Y-%m-%d %H:%M'`

### § archive-episodes

Operate on `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` → `# Recent Context Episodes`. For episodes past the cutoff: create/update `archive/[YYYY]-archived-context.md` (with the archive header), copy the episode references there (newest-first), **keep** the actual episode `.md` files in `episodes/` (don't delete), and remove the archived references from `agent-memory-index.md`. Update the archive's "Last Updated" date + archived count.

### § archive-emotional-apply

Operate on `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` (`# DOMAIN EMOTIONAL MEMORY`) + `archive/[YYYY]-archived-moments.md`. Prepend a new dated pass (Rationale + Moments) to the archive file, newest-first. Apply the three operations preserving kept/archived blocks **VERBATIM** (never retype — extract, per **Copy-Paste, Don't Regenerate**):
- **Archive full (Tier 2 + Tier 3)**: extract each block verbatim → append into the new archive pass.
- **Shorten (Tier 2)**: replace the block in `agent-core-memory.md` with its compact stub.
- **Remove (Tier 3)**: delete the block from `agent-core-memory.md`.
- **Mechanic**: for an all-delete pass, `copy-lines.sh` + **bottom-first** `sed` deletion works. For a mixed pass, a small block-parse script (split on `^### \[`, keep/stub/drop by datetime token) is safest. **Back up first**; clean up `*.backup.*`; verify no CRLF introduced.

> Dated pass format: `## 🗂️ Archiving Rationale ([DATE] pass)` (tier + reason lines) then `## 📅 Archived Moments ([DATE] pass)` (full blocks, newest-first).

---

## update-memory

### § detect-mode-scan

Read the central episodic index `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` → `# Recent Context Episodes` for the theme-match scan.

### § scan-promotion-markers

Identify cross-layer files written this session, by path:

| Layer | Path |
|-------|------|
| Project context (shared) | `shared-memory/[project]/context/*.md` |
| Project context (private) | `knowledge-base/[project]/*.md` |
| Knowledge | `knowledge-base/[topic].md`, `knowledge-base/core-domain-knowledge.md` |
| Reasoning (shared) | `shared-memory/core-reasoning-memory.md` |
| Reasoning (per-agent) | `agent-core-memory.md` → `# DOMAIN REASONING MEMORY` |

---

## wrap-up

### § read-newest-episode

Read the newest sub-episode: the top H3 block of the top episode file in `[AGENT-MEMORY-PATH]/agent-[domain]/episodes/` (per the episodic index ordering).

---

## core-instruction-control-files

### § load-agent-memory

Use the **Read tool directly** and read all 4 files in parallel:

- `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` (Identity — agent identity, core knowledge, RAS triggers)
- `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` (Context + knowledge index)
- `[AGENT-MEMORY-PATH]/shared-memory/core-reasoning-memory.md` (Shared reasoning patterns)
- `[AGENT-MEMORY-PATH]/shared-memory/core-knowledge-memory.md` (Shared knowledge fundamentals)

### § recover-missing-foundations

The `shared-memory/` directory was not found on disk. Ask [USER-NAME]:

"shared-memory/ not found. Would you like me to:
A) Copy blank templates from `[AGENT-MEMORY-PATH]/control-files/new-agent-template/shared-memory/`
B) Create empty shared-memory/ files with section headers only"

### § load-latest-episode

Read the episode file named by the index entry from `[AGENT-MEMORY-PATH]/agent-[domain]/episodes/`.

### § oversized-memory-warning

A file that exceeded the single-Read limit came back partial. Name it and warn: *"⚠️ `[filename]` exceeded the read limit during loading — consider `/archive-old-memories` to reduce its size."*

---

## list-agents

### § list-agent-domains

Discover every agent in the ecosystem by scanning the memory-store root for `agent-[domain]/` folders that hold an identity file (`agent-core-memory.md`):

- **Windows**: `Get-ChildItem -Path "[AGENT-MEMORY-PATH]" -Directory -Filter "agent-*" | Where-Object { Test-Path (Join-Path $_.FullName "agent-core-memory.md") } | ForEach-Object { $_.Name -replace '^agent-','' }`
- **Linux/macOS**: `for d in [AGENT-MEMORY-PATH]/agent-*/; do [ -f "$d/agent-core-memory.md" ] && basename "$d" | sed 's/^agent-//'; done`

The domain is the folder name with the `agent-` prefix stripped (`agent-software-architect` → `software-architect`). Scan **only** direct children of the store root — do not descend into `control-files/` (its `new-agent-template/` is a scaffold, not an agent).

### § read-agent-identity

For each domain, read the identity header at the top of `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` (the `# DOMAIN AGENT IDENTITY` / `## 🤖 Agent Identity` block) and extract:
- **Name** — the `**Name**:` line value.
- **Role** — the `**Role**:` line value; if absent, fall back to the first line of `**Main Purpose**:`.

Read only the header region (roughly the first 15 lines) rather than the whole file — the scan spans ~30 agents, so keep each read cheap.

---

## create-agent

### § check-agent-exists

Check for an identity file at the agent's home:

- **Windows**: `Test-Path "[AGENT-MEMORY-PATH]\agent-[domain]\agent-core-memory.md"`
- **Linux/macOS**: `test -f "[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md"`

A directory that exists but holds no identity file is a **partial creation**, not an agent — report it rather than silently completing it.

### § generate-uuid

Generate a unique identifier:
- **Windows**: `powershell -c "[guid]::NewGuid().ToString()"`
- **Linux/macOS**: `uuidgen` or `cat /proc/sys/kernel/random/uuid`

### § create-agent-store

Seed the home by copying the **two per-agent files** out of the template, then creating the two memory directories:

- **Windows**:
  ```
  New-Item -ItemType Directory -Force "[AGENT-MEMORY-PATH]\agent-[domain]\episodes", "[AGENT-MEMORY-PATH]\agent-[domain]\knowledge-base"
  Copy-Item "[AGENT-MEMORY-PATH]\control-files\new-agent-template\agent-core-memory.md" "[AGENT-MEMORY-PATH]\agent-[domain]\"
  Copy-Item "[AGENT-MEMORY-PATH]\control-files\new-agent-template\agent-memory-index.md" "[AGENT-MEMORY-PATH]\agent-[domain]\"
  ```
- **Linux/macOS**:
  ```
  mkdir -p "[AGENT-MEMORY-PATH]/agent-[domain]/episodes" "[AGENT-MEMORY-PATH]/agent-[domain]/knowledge-base"
  cp "[AGENT-MEMORY-PATH]/control-files/new-agent-template/agent-core-memory.md" "[AGENT-MEMORY-PATH]/agent-[domain]/"
  cp "[AGENT-MEMORY-PATH]/control-files/new-agent-template/agent-memory-index.md" "[AGENT-MEMORY-PATH]/agent-[domain]/"
  ```

Copy those two files **only**. `new-agent-template/shared-memory/` is a virgin-store seed for a fleet that has no shared memory yet (see `§ recover-missing-foundations`) — shared memory is fleet-wide, lives once at the store root, and must never be copied into an agent's folder.

### § persist-identity

Substitute the drafted values throughout the two seeded files:

- `[DOMAIN]` → the domain in display form (`frontend-react` → `Frontend React`)
- `[domain]` on the **Folder** line → the domain slug
- `[USER-NAME]` → the user's name, matching the rest of the fleet
- `[DATE]` → today's date, `date '+%Y-%m-%d'`
- `[CLEAR MISSION STATEMENT - What specific value this agent provides]` → the Main Purpose
- `[Key responsibility 1]` / `[Key responsibility 2]` / `[Key responsibility 3]` → the three responsibilities
- `[GENERATE-NEW-UUID]` → the UUID from **§ generate-uuid**

Leave the `<!-- content here -->` markers and the RAS / emotional example blocks in place — they are the shape the agent grows into, not unfinished work.

### § initialize-index

Nothing beyond the copy: `agent-memory-index.md` arrives from the template with both index sections (`# Recent Context Episodes`, `# Core Knowledge Base`) present and empty. Its `[DOMAIN]` placeholders are replaced as part of **§ persist-identity**.

### § verify-agent

Read `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` back and confirm:

- the `**Name**:`, `**Role**:` and `**UUID**:` lines carry real values;
- the UUID matches 8-4-4-4-12;
- **no placeholder survives** in either file — `grep -n '\[DOMAIN\]\|\[domain\]\|\[GENERATE-NEW-UUID\]\|\[DATE\]\|\[USER-NAME\]'` returns nothing;
- `episodes/` and `knowledge-base/` both exist.

Report any failure precisely. A partially-created agent is worse than none, because the next **§ check-agent-exists** will treat it as already existing.
