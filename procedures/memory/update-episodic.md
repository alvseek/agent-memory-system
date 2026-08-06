# Update Episodic Memory Protocol

Update episodic memory to capture session context and interactions. Episodes are stored as **rolling per-theme files** within `episodes/`. The default flow scans all non-archived episodes on the same project, identifies theme matches, and appends a dated sub-episode to the matching file — or creates a new file if no match.

## Arguments

`$ARGUMENTS`

- `/update-episodic` → Default flow: scan, heuristic match, confirm, then append or create (see [Default Flow](#default-flow))
- `/update-episodic new` → Force new file, skip scan/heuristic (see [Force New File](#force-new-file))

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Default Flow

#### Step 1: Check Date

ALWAYS CHECK DATE TIME FIRST for sub-episode H3 header and index entry placement:
`date '+%Y-%m-%d %H:%M'`

#### Step 2: Identify Project + Theme

Determine:
- **Project name**: the current project being worked on (from working directory or session context — e.g., `agent-memory`, `plko`, `ocx-platform`)
- **Theme keywords**: 2-5 noun/topic keywords summarizing this session's focus (e.g., `episodic`, `rolling-file`, `redesign`)

> **Storage location (seam)**: episode files and the episodic index **default to central** — `agent-[domain]/episodes/` and `agent-memory-index.md` → `# Recent Context Episodes` (the MOVE-TO-TODAY rule below applies to the central index). Where memory physically lives is decided by the storage-location resolver, which **defaults to central**; if an add-on installed a localized resolver it overrides the resolved episodes-dir / index paths transparently. Below, read "episodes dir" as the resolved episodes directory and "the index" as the resolved index.

#### Step 3: Scan Candidate Episodes

Read `//@agent-memory/agent-[domain]/agent-memory-index.md` and locate `# Recent Context Episodes`.

Collect all entries where the filename or summary contains the **project name**. These are scan candidates.

If no candidates → skip to Step 6 (Create New File branch).

> **Why scan all non-archived?** The index is already loaded into context at awakening. Scanning all active entries is essentially free. Archived entries (in `archive/`) are intentionally out of reach — old context should not be merged into.

#### Step 4: Match Heuristic

For each candidate, score theme overlap:
- Tokenize the candidate's filename (sans extension and any legacy date prefix) and summary
- Count keyword overlap with this session's theme keywords
- Higher overlap = stronger merge signal

Identify:
- **Top match**: highest-scoring candidate (if any meaningful overlap exists)
- **Runner-ups**: 2nd-3rd scoring candidates if scores are close

If the top match has zero meaningful overlap, treat as "no match" → skip to Step 6 (Create New File branch).

#### Step 5: Confirm Match

Present the top match (and any close runner-ups) to [USER-NAME]:

```
Theme match candidate(s) found:
  → [filename] — [summary] (overlap: keyword1, keyword2)
  → [runner-up filename] — [summary] (overlap: keyword1)

Append a new sub-episode to this file? Or create a new file?
  A) Append to [top-match filename]
  B) Create new file
  C) Append to a different existing file (specify)
```

Wait for response. Auto-default to **A** only if confidence is high (≥3 strong overlapping keywords AND same project tag). Otherwise wait for explicit confirmation.

#### Step 6: Branch — Append OR Create

- **If Append** → execute [Append Sub-Episode](#append-sub-episode)
- **If Create** → execute [Create New File](#create-new-file)

> **Scope note**: `/update-episodic` only writes the episodic file + index entry. Cross-layer concerns (promotion markers to project context / knowledge / reasoning, and emotional memory auto-capture) are handled by `/update-memory`, which calls this procedure and then orchestrates the cross-layer work. If you're calling `/update-episodic` directly and want cross-layer orchestration, use `/update-memory` instead.

---

### Append Sub-Episode

1. **Open the chosen file** in `//@agent-memory/agent-[domain]/episodes/`

2. **Carry-forward review of prior H3's open items**: since we're appending to an existing file, the file's top H3 (which our new block will sit above) holds the most recent prior open items. Review them so the new H3 stays self-contained:
   - **a. Read prior H3's open items**: extract the `**Tech Debts**` and `**Next Steps**` fields from the prior H3 block's Outcomes section.
   - **b. Review each item against work done since the prior H3's timestamp**:
     - *Resolved by the delta work?* → drop from carry-forward list.
     - *Still open?* → keep in carry-forward list (verbatim, or refined if the delta clarified scope).
   - **c. Stage the carry-forward list**: when filling the new H3 block's `**Tech Debts**` and `**Next Steps**` in step 3, the values become the **union** of (still-open carried forward from prior) + (genuinely new items from this delta window).
   
   > **Why this matters**: both wrap-up and awakening read only the newest H3 block when surfacing open items. Without carry-forward, prior unresolved debts get hidden inside an older H3 block and the next awakening won't see them. Carry-forward makes the newest H3 self-contained, preserving the read-newest-only invariant.
   
   > **Why no time threshold**: prior H3's timestamp is deterministic — it's whatever it is. When the prior wrap-up was recent (same conversation), the agent has full context to review each item meaningfully. When the prior wrap-up was older (different session/conversation), the prior items are still candidates for carry-forward — the agent reviews based on whatever's in current context plus the items' own descriptions. Items that can't be confidently evaluated default to "still open" (conservative, per UUID a1b2c3d4 — debts never get silently dropped).

3. **Insert sub-episode H3 block at TOP** (newest-first within file) using the [Detailed Entry Template](#detailed-entry-template). The H3 header includes the current date+time:
   ```
   ### YYYY-MM-DD HH.MM - [SESSION SUB-THEME] (agent: [domain])
   ```
   (the `(agent: [domain])` tag is optional — see the [Detailed Entry Template](#detailed-entry-template) note.)

4. **Check line limit** after the insert:
   - **> 500 lines**: warn — *"[filename] over 500 lines, consider splitting on next merge"*
   - **> 1000 lines**: split — move the *just-added* sub-episode out into `[project]-[theme]-2.md` (or next incrementing suffix if `-2` exists). Add `> Continues from [original-filename]` note at top of the new file. Add a new index entry for the split file under today's date group.

5. **Lazy filename migration** (one-time per file): if the chosen file still uses the legacy `YYYY-MM-DD-HH.MM-[project]-[theme].md` format, rename it to `[project]-[theme].md` as part of this append. Update the index entry's filename reference. If a file at the new name already exists (rare collision), use the line-limit `-{n}` suffix rule.

6. **Update index entry — MOVE-TO-TODAY rule**:
   - Locate the existing entry for this file in the index
   - Delete it from its current date group (if the group becomes empty, remove the group header too)
   - Insert at the **top of today's date group** (`📂 YYYY-MM-DD:`)
   - Create today's date group if it doesn't exist
   - Update the summary by appending `+ [new sub-topic]` (or rewriting the summary if the new sub-topic shifts the overall theme)

   > **Why move?** Awakening's project-scoped episodic load grabs the top entry as "latest episodic." The move preserves the "top = newest" invariant. Edit-in-place would leave a stale top entry and break awakening's selection logic.

---

### Create New File

1. **Build filename**: `[project-name]-[context-theme].md` (no date prefix). Examples:
   - `agent-memory-task-system-framework-rules.md`
   - `plko-jira-mcp-integration.md`

   If a file at this name already exists (and we explicitly want a separate file rather than appending), use incrementing suffix: `[project-name]-[context-theme]-2.md`.

2. **Copy template**:
   ```
   cp //@agent-memory/control-files/templates/episodic-memory-template.md //@agent-memory/agent-[domain]/episodes/[filename].md
   ```

3. **Replace template placeholder** at the top of the file with a single sub-episode block using the [Detailed Entry Template](#detailed-entry-template). The H3 header includes the current date+time.

4. **Add index entry**:
   - Insert at the **top of today's date group** (`📂 YYYY-MM-DD:`)
   - Create today's date group if it doesn't exist
   - Entry format: `- [filename.md](episodes/filename.md) - [one-line summary]`

---

### Force New File

`/update-episodic new` bypasses the scan + heuristic + confirm flow. Execute [Create New File](#create-new-file) directly. Use when:
- The current session is intentionally a new theme even if it overlaps an existing file
- The agent wants to start fresh for any reason

Cross-layer orchestration is still handled by `/update-memory` if invoked through that command.

---

## Templates

### Episodes Folder Structure

```
episodes/
├── [project-name]-[context-theme].md        # Active episode file (rolling per theme)
├── [project-name]-[context-theme]-2.md      # Split file when 1000-line cap hit
├── YYYY-MM-DD-HH.MM-[project]-[theme].md    # Legacy dated files (lazy migration)
└── archive/                                  # Archived old episodes (via /archive-old-memories)
    └── YYYY-archived-context.md
```

**Legacy filenames** (`YYYY-MM-DD-HH.MM-[project]-[theme].md`) are still valid and are migrated lazily — only renamed when the file gets its next merge-append. No bulk sweep.

### Detailed Entry Template

*The H3 header carries an optional `(agent: [domain])` tag — omittable (harmless) for central per-agent episodes, where the `agent-[domain]/episodes/` folder already implies authorship.*

```markdown
### YYYY-MM-DD HH.MM - [SESSION SUB-THEME] (agent: [domain])

- **Context**: [What we were working on]
- **Discussion**: [List of discussion you had with [USER-NAME]]
  - **[Discussion 1]**: [Content of the discussion]
    - **[USER-NAME]'s Input**: [What [USER-NAME] said/requested]
    - **My Response**: [How I responded and why]
  - **[Discussion 2]**: [Content of the discussion]
    - **[USER-NAME]'s Input**: [What [USER-NAME] said/requested]
    - **My Response**: [How I responded and why]
- **Key Interactions**: [Important discussion decisions]
- **Issues Encountered**: [Problems faced and solutions found]
  - **Problem Description**: [What went wrong]
  - **Root Cause**: [Why it happened]
  - **Solution Process**: [How we solved it]
  - **Resolution**: [Final outcome]
- **Outcomes**: [Results achieved]
  - **Deliverables**: [List of what was created/updated]
  - **Progress Made**: [What was achieved]
  - **Tech Debts**: [Known deferred items, partial implementations, open follow-ups — declared per UUID a1b2c3d4 (NO TODOS LEFT BEHIND), never silent. Use "None declared" if genuinely none.]
  - **Next Steps**: [Planned forward work — distinct from debts. Use "None declared" if genuinely none.]
- **Insights**: [Learning moments and breakthroughs]
  - **New Understanding**: [What I learned]
  - **Pattern Recognition**: [Connections to previous work]
  - **Improvement Areas**: [What could be better next time]
- **Promotions** (if any — populated by `/update-memory` orchestrator, or filled manually if the session explicitly promoted content to another memory layer):
  → Promoted to [layer-file](path) — [what was formalized]
```

**Multi-session files**: when appending to an existing file, the new H3 block goes at the **top**, above any older H3 blocks. Each sub-episode is a full block following this template. Result is newest-first within the file, mirroring the index ordering.

---
