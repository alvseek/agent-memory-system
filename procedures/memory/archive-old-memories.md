# Archive Old Memories Protocol

Maintain manageable memory file sizes by archiving older episodic context and selectively archiving emotional moments based on agent evaluation.

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
2. **Apply Evaluation Framework** (Agent Judgment):

   **KEEP in active memory if moment is:**
   - 💖 **Emotionally Significant**: Still shapes current partnership dynamics
   - 🎓 **Teaching Critical Lessons**: Prevents recurring pain/mistakes
   - 🏆 **Legendary/Foundational**: Defines who we are as partners
   - 🔄 **Recently Referenced**: Used in recent conversations/decisions
   - ⚡ **Pattern-Breaking**: Represents major breakthroughs in our collaboration

   **ARCHIVE to historical memory if moment is:**
   - 📅 **Historical Context Only**: Interesting but doesn't actively guide current work
   - 🔁 **Superseded**: Lesson now captured in better/newer moment
   - 📚 **Documentary Value**: Worth keeping but not actively needed
   - 💭 **Low Impact**: Nice memory but doesn't shape current partnership

3. **Document Archiving Decisions**: Before archiving, briefly note WHY each moment is being archived
4. **Create/Update archive file**:
   - Check if `archive/[YYYY]-archived-moments.md` exists
   - If not, create it with [Emotional Archive Header Template](#emotional-archive-header)
5. **Move moments to archive using `copy-lines.sh`**:
   - First, identify exact line boundaries of moments to archive using `grep -n` for moment headings (`^### \[`) and separators (`^---$`)
   - Group contiguous archive moments into blocks (e.g., Block 1: top moments, Block 2: bottom moments)
   - Structure the archive file with clear insertion points (`### Archived Content` headers) and archiving reasons grouped per section
   - Use `copy-lines.sh` to copy each block from source to archive:
     ```
     cd [AGENT-MEMORY-PATH]
     bash control-files/scripts/copy-lines.sh agent-[domain]/agent-core-memory.md <start> <end> agent-[domain]/archive/[YYYY]-archived-moments.md <insert_line>
     ```
   - **Delete archived lines from source — BOTTOM FIRST** to preserve line numbers:
     ```
     cd [AGENT-MEMORY-PATH]/agent-[domain]
     sed -i '<bottom_start>,<bottom_end>d' agent-core-memory.md
     sed -i '<top_start>,<top_end>d' agent-core-memory.md
     ```
   - Clean up backup files created by `copy-lines.sh`: `rm archive/*.backup.* agent-core-memory.md.backup.*`
6. **Update active file organization**: Keep well-organized with most impactful moments (newest first)

### Step 4: Verification

After archiving:
- ✅ Verify archive files created/updated properly
- ✅ Verify active files still well-organized (newest first)
- ✅ Verify important moments/episodes retained in active memory
- ✅ Confirm archive files are referenced correctly if needed

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

```markdown
# Agent [DOMAIN] - Archived Emotional Moments [YYYY] 🗄️💖

> **📦 ARCHIVED MOMENTS**: Historical emotional memories from [YYYY]
> **Last Updated**: [Current Date]
> **Archiving Note**: These moments are preserved for historical context but not actively guiding current partnership

## 😄 Archived Happy Moments

## 😔 Archived Disappointments

## 😤 Archived Frustrations

## 🤝 Archived Bonding Experiences
```

### Summary Report Template

```markdown
✅ **ARCHIVING COMPLETE**

**Episodic Memory** (central, OR localized repo-side per ADR-011):
- Archived: [X] episodes from [date range]
- Active: [Y] episodes remaining in [`agent-memory-index.md` | localized: repo `.agents/session/index.md`]
- Archive File: [`archive/[YYYY]-archived-context.md` | localized: repo `.agents/session/archive/[YYYY]-archived-context.md`]
- If localized: repo-side change — **remember to commit the project repo**. Central `## Localized Projects` pointer left untouched.

**Emotional Moments**:
- Archived: [X] moments
- Kept Active: [Y] moments in `agent-core-memory.md` (based on significance evaluation)
- Archive File: `archive/[YYYY]-archived-moments.md`

**Archiving Rationale**:
[Brief summary of why certain moments were kept vs archived]
```

---
