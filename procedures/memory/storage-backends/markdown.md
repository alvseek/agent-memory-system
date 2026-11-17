# Storage Backend — Markdown (git tree)

Concrete storage mechanics for the **native markdown-over-git** world. Each `## [procedure]` section defines the `§ op`s that procedure references. See the [seam contract](README.md).

> **Storage location (seam)**: paths **default to central** — `agent-[domain]/episodes/`, `agent-[domain]/knowledge-base/`, and `agent-memory-index.md`. Where a project's memory physically lives is decided by the storage-location resolver, which **defaults to central**; if a coding/environment add-on installed a **localized** resolver it overrides the resolved paths transparently — no change to the ops below.

---

## update-episodic

<!-- composed-source: procedures/sections/markdown/update-episodic.stamp-date.md -->
<!-- composed-source: procedures/sections/markdown/update-episodic.list-candidate-episodes.md -->
<!-- composed-source: procedures/sections/markdown/update-episodic.reopen-archived-theme.md -->
<!-- composed-source: procedures/sections/markdown/update-episodic.template.md -->
<!-- composed-source: procedures/sections/markdown/update-episodic.append-sub-episode.md -->
<!-- composed-source: procedures/sections/markdown/update-episodic.housekeeping.md -->
<!-- composed-source: procedures/sections/markdown/update-episodic.record-theme-state.md -->
<!-- composed-source: procedures/sections/markdown/update-episodic.create-episode.md -->

## add-reasoning

<!-- composed-source: procedures/sections/markdown/add-reasoning.read-reasoning-store.md -->
<!-- composed-source: procedures/sections/markdown/add-reasoning.template.md -->
<!-- composed-source: procedures/sections/markdown/add-reasoning.generate-uuid.md -->
<!-- composed-source: procedures/sections/markdown/add-reasoning.persist-reasoning.md -->

## update-emotional

<!-- composed-source: procedures/sections/markdown/update-emotional.stamp-date.md -->
<!-- composed-source: procedures/sections/markdown/update-emotional.template.md -->
<!-- composed-source: procedures/sections/markdown/update-emotional.persist-emotional.md -->

## update-knowledge

<!-- composed-source: procedures/sections/markdown/update-knowledge.template.md -->
<!-- composed-source: procedures/sections/markdown/update-knowledge.persist-knowledge.md -->
<!-- composed-source: procedures/sections/markdown/update-knowledge.update-knowledge-index.md -->

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

### § propose-archive-candidates

**No tool on this backend.** List the candidates from the index yourself: read `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` → `# Recent Context Episodes`, and for each entry read the episode file's frontmatter `tags:` and the top sub-episode's date. `auto` is an entry whose file carries `finished` and is not the newest for its project; `ask` is an entry with no marker whose top sub-episode is older than 30 days; `protected` is the newest entry per project, the newest overall, and any file with no usable date. Report the sets; write nothing yet.

### § apply-archive-candidates

**No tool on this backend, and no bulk write.** On markdown the archive is an index move (see `§ archive-selected`), so apply the `auto` set exactly as if the user had chosen each of those entries.

### § archive-selected

Operate on `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` → `# Recent Context Episodes`. For each selected episode: create or update `archive/[YYYY]-archived-context.md` (with the archive header), copy the episode reference there (newest-first), **keep** the episode `.md` file in `episodes/` (never delete it), remove the reference from `agent-memory-index.md`, and update the archive's "Last Updated" date and count.

### § recover-archived

Remove `finished` from the episode file's frontmatter, then move its reference back from the archive file into the episode index (newest-first, under today's date group) and decrement the archive's count. The file itself never moved, so there is nothing to restore.

### § archive-emotional-apply

Operate on `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` (`# DOMAIN EMOTIONAL MEMORY`) + `archive/[YYYY]-archived-moments.md`. Prepend a new dated pass (Rationale + Moments) to the archive file, newest-first. Apply the two operations preserving kept/archived blocks **VERBATIM** (never retype — extract, per **Copy-Paste, Don't Regenerate**):
- **Archive**: extract the block verbatim → append into the new archive pass, then delete it from `agent-core-memory.md`.
- **Keep**: leave the block in `agent-core-memory.md` untouched. There is no shorten/stub step.
- **Mechanic**: for an all-archive pass, `copy-lines.sh` + **bottom-first** `sed` deletion works. For a mixed pass, a small block-parse script (split on the moment headings, keep/archive by datetime token) is safest. **Back up first**; clean up `*.backup.*`; verify no CRLF introduced.

> Dated pass format: `## 🗂️ Archiving Rationale ([DATE] pass)` (reason lines) then `## 📅 Archived Moments ([DATE] pass)` (full blocks, newest-first).

---

## update-memory

<!-- composed-source: procedures/sections/markdown/update-memory.detect-mode-scan.md -->
<!-- composed-source: procedures/sections/markdown/update-memory.scan-promotion-markers.md -->

## wrap-up

<!-- composed-source: procedures/sections/markdown/wrap-up.persist-store.md -->
<!-- composed-source: procedures/sections/markdown/wrap-up.persistence-report.md -->
<!-- composed-source: procedures/sections/markdown/wrap-up.failure-report.md -->

## core-instruction-control-files

<!-- composed-source: procedures/sections/markdown/core-instruction-control-files.load-agent-memory.md -->
<!-- composed-source: procedures/sections/markdown/core-instruction-control-files.load-user-profile.md -->
<!-- composed-source: procedures/sections/markdown/core-instruction-control-files.persist-user-profile.md -->
<!-- composed-source: procedures/sections/markdown/core-instruction-control-files.recover-missing-foundations.md -->
<!-- composed-source: procedures/sections/markdown/core-instruction-control-files.load-latest-episode.md -->
<!-- composed-source: procedures/sections/markdown/core-instruction-control-files.oversized-memory-warning.md -->

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

---

## anchor-memory

**No action on the markdown backend** — the permanent layer here *is* the compiled global
instructions file. `core-memory/compile-scripts/compile.sh` folds `0`–`3-core-memory` into
`output/core-memory-compiled.md`, and `write-to-<harness>.sh` writes that to the harness's
global instructions file; the profile and environment blocks travel with it, so there is no
separate content file and nothing to point at.

To refresh it, run the installer pair — the core write step, then the coding overlay
installer **last** (it re-adds the overlay path line the core write drops).

### § fetch-permanent-layer

**No action.** The block is already in `[GLOBAL-INSTRUCTIONS-FILE]` for this backend.

### § write-permanent-file

**No action.**

### § install-pointer

**No action.**

---

## register-core-access

The declarations travel with the compiled core. `core-memory/compile-scripts/compile.sh` folds
the core memory into `output/core-memory-compiled.md`, each `write-to-<harness>.sh` writes that
into the harness's global instructions file, and the same script stamps `[CORE-ACCESS]` /
`[CORE-MCP-URL]` from `CORE_ACCESS` / `CORE_MCP_URL` through `set-core-access.sh`. On this
backend the form in force is therefore `markdown`: the client has the installed commands.

### § read-access-pair

**`markdown`**, with the machine's configured `CORE_MCP_URL` (default `<unset>`). Nothing to
fetch — the value is this backend, and the URL is whatever the installer was given.

### § write-access-lines

**No action needed.** The installer pair writes both lines, and a markdown client has both. To
re-stamp a value, run `core-memory/compile-scripts/set-core-access.sh <instructions-file> markdown <url>`:
it rewrites the two lines in place and exits non-zero when either is missing, which is the
correct loud failure here because the installer always wrote them.
