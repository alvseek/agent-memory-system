# Storage Backend — Markdown (git tree)

Concrete storage mechanics for the **native markdown-over-git** world. Each `## [procedure]` section collects the named regions that define the `§ op`s that procedure references. See the [seam contract](README.md).

> **Storage location (seam)**: paths **default to central** — `agent-[domain]/episodes/`, `agent-[domain]/knowledge-base/`, and `agent-memory-index.md`. Where a project's memory physically lives is decided by the storage-location resolver, which **defaults to central**; if a coding/environment add-on installed a **localized** resolver it overrides the resolved paths transparently — no change to the ops below.

---

## update-episodic

@start region id="update-episodic.stamp-date"
### Stamp the entry

Read the host's UTC clock (for example, `date -u '+%Y-%m-%d %H.%M UTC'`). Use it in the template's heading and use the same UTC date for the index.

@end region

@start region id="update-episodic.list-candidate-episodes"
### § list-candidate-episodes

Use `# Recent Context Episodes` in `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` to find active episode files. Match the file’s `project` frontmatter to the supplied project; for an unassigned episode, keep only files without a project value. Use the indexed names and summaries to compare themes.

@end region

@start region id="update-episodic.reopen-archived-theme"
### § reopen-archived-theme

Markdown keeps no archive flag on a record: an archived episode is one whose index line was moved into `archive/[YYYY]-archived-context.md`, while the file itself never moved. To reopen it, remove `finished` from the file's frontmatter, move its index line back from the archive file into the episode index (newest-first, under today's date group), and decrement the archive's count. Then append normally.

@end region

@start region id="update-episodic.template"
### § template

The sub-episode block format → read `[AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/episodic-entry-template.md`.

@end region

@start region id="update-episodic.append-sub-episode"
#### § append-sub-episode

1. **Open the chosen file** in `[AGENT-MEMORY-PATH]/agent-[domain]/episodes/`.
2. **Insert the sub-episode H3 block at the TOP** (newest-first within the file), above any older H3 blocks. Sub-episodes are separated by `---`.
3. **Update the index entry — MOVE-TO-TODAY rule**:
   - Locate the existing entry for this file in the index.
   - Delete it from its current date group (if the group becomes empty, remove the group header too).
   - Insert at the **top of today's date group** (`📂 YYYY-MM-DD:`); create today's group if it doesn't exist.
   - Update the summary from the new block's `**Summary**` row: carry that text verbatim, appended as `+ [new sub-topic]` when the overall theme still holds, or rewritten when the new sub-topic shifts it.

   > **Why move?** Awakening's project-scoped episodic load grabs the top entry as "latest episodic." The move preserves the "top = newest" invariant. Edit-in-place would leave a stale top entry and break awakening's selection logic.

@end region

@start region id="update-episodic.housekeeping"
#### § housekeeping

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

@end region

@start region id="update-episodic.record-theme-state"
#### § record-theme-state

Edit the episode file's frontmatter `tags:` line in place: add `finished` when this block closes the theme, remove it when it does not. Touch nothing else — the body and the other frontmatter fields stay verbatim.

When no `tags:` line exists yet, add one beneath `project:` in the same block. The importer reads episode frontmatter tags into the record, so the marker survives a later import into the DB store even though no tool here reads it.

@end region

@start region id="update-episodic.create-episode"
#### § create-episode

1. **Build filename**: `[project-name]-[context-theme].md` (no date prefix). Examples: `agent-memory-task-system-framework-rules.md`, `plko-jira-mcp-integration.md`. If a file at this name already exists (and a separate file is wanted), use an incrementing suffix: `[project-name]-[context-theme]-2.md`.
2. **Copy the file scaffold**:
   ```
   cp [AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/episodic-memory-template.md [AGENT-MEMORY-PATH]/agent-[domain]/episodes/[filename].md
   ```
3. **Set the frontmatter `project`** to the supplied name, or omit that field and the filename’s project prefix for an unassigned episode. Replace the template placeholder with the composed sub-episode block. The importer reads the project from frontmatter, not the filename.
4. **Add index entry**:
   - Insert at the **top of today's date group** (`📂 YYYY-MM-DD:`); create today's group if it doesn't exist.
   - Entry format: `- [filename.md](episodes/filename.md) - [one-line summary]`, where the summary is the new block's `**Summary**` row copied verbatim. This entry is the record's listed description, so it and the block must not diverge.

@end region


## update-reasoning

@start region id="update-reasoning.read-reasoning-store"
### § read-reasoning-store

Reuse the rules loaded at awakening. If needed, read `# DOMAIN REASONING MEMORY` in `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` and `shared-memory/core-reasoning-memory.md` under the same memory root. For coding work, include `shared-memory/coding-reasoning-memory.md` when present.

@end region

@start region id="update-reasoning.save"
### § save

- **Add:** Read `[AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/reasoning-pattern-template.md`. Generate a new UUID (`uuidgen` or PowerShell `[guid]::NewGuid()`) and add the completed rule to the acting agent’s `# DOMAIN REASONING MEMORY` section.
- **Refine:** Find the existing rule by UUID in its owning file and edit that block in place. Keep its UUID and the surrounding rules unchanged.

@end region

## update-emotional

@start region id="update-emotional.template"
### § template

Read `[AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/emotional-moment-template.md`.

@end region

@start region id="update-emotional.persist-emotional"
### § persist-emotional

Write the moment to `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` (in the `# DOMAIN EMOTIONAL MEMORY` section). **Order: NEWEST FIRST** — most recent entries at the TOP.

@end region


## update-knowledge

@start region id="update-knowledge.template"
### § template

The knowledge-file format → read `[AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/knowledge-file-template.md`.

@end region

@start region id="update-knowledge.persist-knowledge"
### § persist-knowledge

Create in `[AGENT-MEMORY-PATH]/agent-[domain]/knowledge-base/research/` (domain expertise and research). Name the file `[date]-[descriptive-theme].md` or `[domain-area].md` — examples: `2025-09-11-nestjs-patterns.md` (dated research), `typescript-best-practices.md` (timeless domain knowledge). Create the file with the template structure, filling the frontmatter `tags` — the importer reads them into the record's `tags`.

@end region

@start region id="update-knowledge.update-knowledge-index"
### § update-knowledge-index

Update `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` knowledge directory - add an entry to the knowledge index for discoverability, of the form `- **[{Title}]({path})** - [one-line summary]`. Copy the summary from the entry's `**Summary**` row verbatim: this line is the record's listed description on the markdown backend and the `content_summary` on the DB one, so the two must not diverge.

@end region


## load-episodic

@start region id="load-episodic.mechanics"
### § list-episodes

Read `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` and locate `# Recent Context Episodes`. Parse entries — each `📂 YYYY-MM-DD:` group holds `- [filename.md](episodes/filename.md) - summary`, newest-first. File path = `episodes/[filename.md]`.

### § load-episode-body

Read the selected episode file(s) from `[AGENT-MEMORY-PATH]/agent-[domain]/episodes/` using the Read tool.
@end region

---

## load-knowledge

@start region id="load-knowledge.mechanics"
### § list-knowledge

Read `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` and locate `# Core Knowledge Base`. Parse entries — `### **[Topic Group]**` headers over `- **[Title](path)** - description`. File path from the markdown link. Exclude any "Project Context Files" subsection (overlay concern).

### § load-knowledge-body

Read the selected file(s) from `[AGENT-MEMORY-PATH]/agent-[domain]/knowledge-base/` using the Read tool.
@end region

---

## archive-old-memories

@start region id="archive-old-memories.mechanics"
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
@end region

---

## wrap-up

@start region id="wrap-up.finish"
## Finish wrap-up

`$ARGUMENTS` — `[agent|all]`. Use `agent` (default) to commit and push only this agent's memory, or `all` for the whole memory store.

Execute `/push-memory <mode>` with the selected `agent` or `all` scope. Record each repository's result: pushed (with commit hash), no changes, or failed (with reason).

**Completion gate:** Report success only when the required memory updates succeeded, nothing in scope is dirty, and no branch carrying this session's commits is ahead of its remote. In `agent` mode, report other agents' dirty files without treating them as a failure.

On success:

```
Wrap-up complete (mode: [agent / all] · [fresh / delta from CUTOFF]):

Memory update:
- Phase 1 — Reusable lessons: reasoning: [added — pattern name / skipped] / knowledge: [added — entry name / skipped]
- Phase 2 — Session captured: [appended to / created] [name] ([timestamp]) — [brief theme]; carry-forward: [N items / N/A]
- Phase 3 — Feeling captured: emotional [captured — polarity + clearest criterion / skipped — brief reason]

Memory persisted:
- (git-backed store) [repo]: ✅ [commit-hash] pushed / no changes [— agent mode: other agents' files left untouched]

📋 Open items going forward:

Tech debts:
- [item 1]
(or "None declared")

Next steps:
- [item 1]
(or "None declared")
```

**On failure:** Report the failed update or outstanding commit or push instead of reporting completion:

```
🚨 WRAP-UP INCOMPLETE — MEMORY NOT SAVED. NEED CONFIRMATION.

[Memory update / Open items sections — same as above]

Memory persisted — FAILED / INCOMPLETE:
- [repo]: ⚠️ [failed memory update / uncommitted files / unpushed commits / push error: <reason>]

What remains unsaved, and where:
- [repo → which path is uncommitted or unpushed]
(In `agent` mode another agent's dirty files are expected and are NOT listed here.)

Resolve the failed update or push before reporting completion.
```
@end region


## core-instruction-control-files

@start region id="core-instruction-control-files.load-agent-memory"
### § load-agent-memory

Use the **Read tool directly** and read all 4 files in parallel:

- `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` (Identity — agent identity, core knowledge, RAS triggers)
- `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` (Context + knowledge index)
- `[AGENT-MEMORY-PATH]/shared-memory/core-reasoning-memory.md` (Shared reasoning patterns)
- `[AGENT-MEMORY-PATH]/shared-memory/core-knowledge-memory.md` (Shared knowledge fundamentals)

@end region

@start region id="core-instruction-control-files.load-user-profile"
### § load-user-profile

Use the `## AI Agent - User Profile` section already in the global instructions file. If the section is absent or all its fields are empty, follow the first-run instructions. Otherwise, leave blank fields as they are.

@end region

@start region id="core-instruction-control-files.persist-user-profile"
### § persist-user-profile

Write the three values to `[AGENT-MEMORY-PATH]/shared-memory/user-profile.md`, keeping the existing bullet form — `- **[USER-NAME]** = …` and its two siblings — because `user-profile-claude.sh` reads those exact markers by line. Then tell [USER-NAME] that the compiled instructions file picks them up on the next `user-config-claude.sh` run: the markdown file is the source, the compiled copy is downstream of it.

@end region

@start region id="core-instruction-control-files.recover-missing-foundations"
### § recover-missing-foundations

If the `shared-memory/` directory is missing, ask [USER-NAME]:

"shared-memory/ not found. Would you like me to:
A) Copy blank templates from `[AGENT-MEMORY-PATH]/control-files/new-agent-template/shared-memory/`
B) Create empty shared-memory/ files with section headers only"

@end region

@start region id="core-instruction-control-files.load-latest-episode"
### § load-latest-episode

Read the episode file named by the newest index entry from `[AGENT-MEMORY-PATH]/agent-[domain]/episodes/`. If a different entry matches the project you need, read that file instead.

@end region


## list-agents

@start region id="list-agents.mechanics"
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
@end region

---

## create-agent

@start region id="create-agent.mechanics"
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
@end region

---

## anchor-memory

@start region id="anchor-memory.mechanics"
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
@end region

---

## register-core-access

@start region id="register-core-access.mechanics"
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
@end region
