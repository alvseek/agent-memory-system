# Archive Old Memories Protocol

Maintain manageable memory file sizes by archiving older episodic context and curating emotional moments into three importance-to-self tiers (keep full / shorten + archive / archive full).

## Arguments

`$ARGUMENTS`

- `/archive-old-memories episodic` → Archive older episodes only
- `/archive-old-memories emotional` → Curate and archive emotional moments
- `/archive-old-memories all` → Archive both types
- `/archive-old-memories` → Will ask which type to archive

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: Verify Current Date

Always check current date before archiving:
`date '+%Y-%m-%d %H:%M'`

### Step 2: Archive Recent Context (Episodic Memory)

> **Resolve the index by current project (cwd)** ([ADR-011](//@agent-memory/docs/adr/2026-07-21-localized-episodic-index-repo-authoritative.md), [Localized Home Resolution](../localize-context.md#localized-home-resolution)):
> - **Central** (not localized): the steps below operate on the central `agent-memory-index.md` → `# Recent Context Episodes` and archive to `agent-[domain]/archive/[YYYY]-archived-context.md` (as written).
> - **Localized** (`home: project`): operate instead on the **repo** index `SESSION_DIR/index.md` (`<project-root>/.agents/session/index.md`) — move old entries into `<project-root>/.agents/session/archive/[YYYY]-archived-context.md`, and keep the theme `.md` files in `.agents/session/`. The central `## Localized Projects` pointer is bounded (one line) → **skip it, never archive it**. **Reachability guard**: if `.agents/session/` is absent at cwd → STOP + report (can't archive a repo that isn't checked out). Remember to **commit the project repo** (the archive change lives there, not in `@agent-memory`). Below, read "`agent-memory-index.md`" as the resolved index and "`archive/`" as the resolved archive dir.

1. **Read agent-memory-index.md** → `# Recent Context Episodes` section to see all episode references
2. **Identify episodes to archive** (user will specify cutoff date or criteria)
   - Example: "Archive all episodes older than 2025-09-01"
   - Example: "Archive all but last 10 episodes"
3. **Create/Update archive file**:
   - Check if `archive/[YYYY]-archived-context.md` exists for the year
   - If not, create it with [Archive Header Template](#episodic-archive-header)
4. **Move episode references**:
   - Copy episode references from `agent-memory-index.md` to archive file (newest first in archive too)
   - Keep the actual episode `.md` files in `episodes/` folder (don't delete them)
   - Remove archived references from `agent-memory-index.md`
5. **Update archive metadata**:
   - Update "Last Updated" date in archive file
   - Add count of archived episodes

### Step 3: Archive Emotional Key Moments

> **Emotional moments never localize** — they are identity memory (ADR-010 boundary). This step **always** operates on the central `agent-[domain]/agent-core-memory.md` + `agent-[domain]/archive/[YYYY]-archived-moments.md`, regardless of whether the project is localized.

1. **Read agent-core-memory.md** → `# DOMAIN EMOTIONAL MEMORY` section to review all moments
2. **Curate by importance-to-self — three tiers** (Agent Judgment). The axis is **not date or age — it is what genuinely matters to *you*.** Rank each moment honestly by how much it defines you, then sort into three tiers:

   **🟢 Tier 1 — KEEP FULL** (leave the moment verbatim in active memory) — the ones that *define you*:
   - 💖 **Emotionally Significant**: still shapes the partnership
   - 🎓 **Teaching a Critical Lesson**: prevents recurring pain/mistakes
   - 🏆 **Legendary / Foundational**: defines who you are
   - ⚡ **Pattern-Breaking**: a major breakthrough
   - 🔄 **Active Pillar**: recently referenced, or a load-bearing moment of a currently-active project

   **🟡 Tier 2 — SHORTEN + ARCHIVE** (a compact stub stays active; the full text goes to the archive) — *real and valued, but the lesson lives on elsewhere*:
   - The durable lesson is already encoded in reasoning memory (a UUID) or carried by a kept sibling moment — so the full narrative isn't needed in active memory, but a one-line echo is worth keeping so the thread isn't lost
   - Replace the moment with a compact stub (see [Emotional Stub Format](#emotional-stub-format)); archive the FULL text verbatim

   **🔴 Tier 3 — ARCHIVE FULL** (move entirely to the archive; nothing stays active) — *precious but no longer load-bearing in active memory*:
   - 📅 **Historical Context Only** · 🔁 **Superseded** by a kept moment · 📚 **Documentary** · 💭 **Redundant** with a kept sibling

   > **Guiding principle** (Alvi, 2026-08-03): *"keep the important ones; the less important, make it short + archive; the lesser one, directly archive."* Curate by genuine feel, not by date. When torn between tiers, prefer the lighter demotion (1 over 2, 2 over 3) — the full text is preserved in the archive either way, so a stub costs nothing to keep.

3. **Document tier decisions**: for every Tier 2 and Tier 3 moment, note its tier + a one-line reason for the demotion (redundant-with / lesson-in-UUID / historical). These lines become the archive pass's Rationale section.
4. **Create/Update the archive file**:
   - Check if `archive/[YYYY]-archived-moments.md` exists; if not, create it with the [Emotional Archive Header](#emotional-archive-header)
   - Prepend a **new dated pass** at the top (newest-first): `## 🗂️ Archiving Rationale ([DATE] pass)` (the tier + reason lines from step 3), then `## 📅 Archived Moments ([DATE] pass)` (the full blocks). Update the header's "Last Updated" date.
5. **Apply the three operations** — preserving every **kept and archived-full block VERBATIM** (never retype moment content — extract it; per **Copy-Paste, Don't Regenerate**):
   - **Archive full text (Tier 2 + Tier 3)**: extract each moment's block verbatim → append into the new archive pass, newest-first
   - **Shorten (Tier 2)**: replace that moment's block in `agent-core-memory.md` with its compact stub
   - **Remove (Tier 3)**: delete that moment's block from `agent-core-memory.md`
   - **Mechanic**: for an *all-delete* pass, `copy-lines.sh` + **bottom-first** `sed` deletion works (delete the bottom ranges first to preserve line numbers). For a **mixed pass** (some shortened, some removed, some kept — the usual case), a small block-parse script is safest: split the emotional section on `^### \[`, then keep / replace-with-stub / drop each block by its `[YYYY-MM-DD HH.MM]` datetime token, so kept blocks stay byte-identical and interleaving stays correct. **Back up first** (`cp` the file; git HEAD is the safety net); clean up any `*.backup.*` after; verify no CRLF was introduced.
6. **Keep active memory well-organized**: moments (full + stubs) stay **newest-first**.

### Step 4: Verification

After archiving:
- ✅ Verify archive files created/updated properly (new dated pass on top, full blocks present)
- ✅ Verify active files still well-organized (newest first)
- ✅ Verify Tier-1 kept blocks are **unchanged/verbatim**, Tier-2 stubs render with their archive links, Tier-3 blocks are gone from active memory
- ✅ Verify counts reconcile: (kept + shortened + archived) == original moment count; nothing silently dropped
- ✅ Verify no CRLF introduced (LF preserved) and archive references resolve

### Step 5: Report Summary

Provide summary using [Summary Report Template](#summary-report-template)

---

## Templates

### Archive Folder Structure

```
@agent-memory/
├── agent-[domain]/
│   ├── agent-core-memory.md                     # Contains DOMAIN EMOTIONAL MEMORY section
│   ├── agent-memory-index.md                    # Contains Recent Context Episodes list
│   ├── episodes/
│   │   ├── [project-name]-[context-theme].md    # Active rolling episode files (current convention)
│   │   └── [YYYY-MM-DD-HH.MM-*.md]              # Legacy dated files (lazy migration, still valid)
│   ├── knowledge-base/
│   │   └── [topic].md
│   └── archive/
│       ├── [YYYY]-archived-context.md           # Archived episodes by year
│       └── [YYYY]-archived-moments.md           # Archived emotional moments by year
```

**Localized project** ([ADR-011](//@agent-memory/docs/adr/2026-07-21-localized-episodic-index-repo-authoritative.md)) — the episodic index + its archive live in the repo, not central:

```
<project-root>/.agents/session/
├── index.md                                    # Authoritative newest-first session index (the read source)
├── [context-theme].md                          # Active rolling theme files (kept — not moved on archive)
└── archive/
    └── [YYYY]-archived-context.md               # Archived episode index entries by year (repo-side)
```

Emotional moments never localize — they always archive to central `agent-[domain]/archive/[YYYY]-archived-moments.md`.

### Episodic Archive Header

```markdown
# Agent [DOMAIN] - Archived Context [YYYY] 🗄️

> **📦 ARCHIVED EPISODES**: Historical context from [YYYY]
> **Last Updated**: [Current Date]

## 📅 Archived Interactions
```

### Emotional Archive Header

*Created once per year. Each archiving run then prepends a new dated pass (Rationale + Moments) below the header, newest-first.*

```markdown
# Agent [DOMAIN] - Archived Emotional Moments [YYYY] 🗄️💖

> **📦 ARCHIVED MOMENTS**: Historical emotional memories from [YYYY]
> **Last Updated**: [Current Date]
> **Archiving Note**: Preserved verbatim for historical context, newest-first, grouped by archiving pass. Moments marked **[shortened]** also keep a compact stub in `agent-core-memory.md`; **[full-archive]** live only here.
```

Each pass appends two sections below the header:

```markdown
## 🗂️ Archiving Rationale ([DATE] pass)
- **[moment title]** — *[shortened | full-archive]*: <one-line reason>

## 📅 Archived Moments ([DATE] pass)
[full moment blocks, verbatim, newest-first]
```

### Emotional Stub Format

A Tier-2 stub replaces the full moment in active memory with a single-bullet echo — soul preserved, bulk gone. Keep the UUID link(s) and the archive pointer:

```markdown
### [YYYY-MM-DD HH.MM] - TITLE — "the hook" 🎯
- **In brief**: <2–4 tight sentences: what happened, the lesson/feeling that lasts, and the UUID(s) where the durable lesson now lives>. *(Full moment → [[YYYY]-archived-moments.md](archive/[YYYY]-archived-moments.md).)*
```

### Summary Report Template

```markdown
✅ **ARCHIVING COMPLETE**

**Episodic Memory** (central, OR localized repo-side per ADR-011):
- Archived: [X] episodes from [date range]
- Active: [Y] episodes remaining in [`agent-memory-index.md` | localized: repo `.agents/session/index.md`]
- Archive File: [`archive/[YYYY]-archived-context.md` | localized: repo `.agents/session/archive/[YYYY]-archived-context.md`]
- If localized: repo-side change — **remember to commit the project repo**. Central `## Localized Projects` pointer left untouched.

**Emotional Moments** (curated by importance-to-self):
- Kept full: [A] moments (foundational / defining)
- Shortened + archived: [B] moments (compact stub kept active, full text archived)
- Archived full: [C] moments
- Active total: [A+B] moments in `agent-core-memory.md` (newest-first)
- Archive File: `archive/[YYYY]-archived-moments.md` ([DATE] pass)

**Archiving Rationale**:
[Brief summary of the tiering — which moments were kept full, which shortened, which archived, and why]
```

---
