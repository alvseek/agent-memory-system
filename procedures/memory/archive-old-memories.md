# Archive Old Memories Protocol

Maintain manageable memory size by archiving older episodic context and curating emotional moments into two importance-to-self tiers (keep / archive). *How* the archive is physically written is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)); the **tier judgment below is storage-agnostic**.

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

Verify the current date before archiving (**§ stamp-date**).

### Step 2: Propose the Episodic Candidates

1. **Scan the active themes** (**§ propose-archive-candidates**). The scan writes nothing and returns three sets:
   - **auto**: themes carrying the `finished` marker that are older than their project's newest episode. These need no decision.
   - **ask**: themes with no marker whose newest sub-episode was last modified longer ago than the window, 30 days unless you were given another. These are the decision.
   - **protected**: the newest episode of each project, the newest overall, and any record with no usable date. This procedure never archives these.
2. **Present the `ask` list**, one line per theme: project, title, last modified, and its `content_summary`. State how many rows were protected and why, in one line, without printing them.

> **A finished theme is marked, not guessed.** The scan archives what carries the marker, so a theme that looks closed but has no marker is a tagging gap: name it in the report and fix it through `/update-episodic`, rather than archiving it by hand.

### Step 3: Archive What Was Decided

1. **Apply the auto set** (**§ apply-archive-candidates**). This is the only bulk write in the procedure.
2. **Archive each theme the user chose** from the ask list, one at a time (**§ archive-selected**).
3. **Touch nothing else.** If a theme was archived in error and the user asks for it back, that is **§ recover-archived**: clear its marker first, then return it to the active set, in that order.

### Step 4: Archive Emotional Key Moments

Review all moments, then decide each one by **importance-to-self** (Agent Judgment). The axis is **not date or age — it is what genuinely matters to *you*.**

**🟢 KEEP** (leave verbatim in active memory) — the ones that *define you*:
- 💖 **Emotionally Significant**: still shapes the partnership
- 🎓 **Teaching a Critical Lesson**: prevents recurring pain/mistakes
- 🏆 **Legendary / Foundational**: defines who you are
- ⚡ **Pattern-Breaking**: a major breakthrough
- 🔄 **Active Pillar**: recently referenced, or load-bearing for a currently-active project

**🔴 ARCHIVE** (out of the active set; the full text is retained and still findable) — *precious but no longer load-bearing*:
- 📅 **Historical Context Only** · 🔁 **Superseded** by a kept moment · 📚 **Documentary** · 💭 **Redundant** with a kept sibling

> **Why two tiers, not three** (2026-10-08): a former middle tier kept a compact stub active while archiving the full text. On the DB that stub-write *overwrites the record body*, and there is no archive file to recover the full from, so shortening silently destroys it. "Archived" now means only *out of the awakening load*, with the full body kept.

> **Guiding principle** (Alvi, 2026-08-03): *"keep the important ones; the less important, make it short + archive; the lesser one, directly archive."* — **updated 2026-10-08**: the middle option is retired; every moment is either kept or archived, and the full text is preserved either way.

**Document the decision** for each archived moment (a one-line reason: historical / superseded / redundant-with). Then **apply the two operations** — preserving every kept and archived block **VERBATIM** (never retype moment content — extract it; per **Copy-Paste, Don't Regenerate**): KEEP, or ARCHIVE (**§ archive-emotional-apply**).

### Step 5: Verification

- ✅ The auto set was applied, and the only other archived rows are the ones the user chose
- ✅ Archived themes left the index and are still reachable by `search`
- ✅ Protected rows were not touched; the count matches the scan
- ✅ If the emotional half ran: kept blocks **unchanged/verbatim**, archived blocks gone from active, and (kept + archived) equals the original moment count
- ✅ No CRLF introduced (LF preserved) and archive references resolve

### Step 6: Report Summary

Provide a summary using the [Summary Report Template](#summary-report-template).

---

## Storage Mechanics

The operations referenced above — **§ stamp-date**, **§ propose-archive-candidates**, **§ apply-archive-candidates**, **§ archive-selected**, **§ recover-archived**, **§ archive-emotional-apply** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## archive-old-memories`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## archive-old-memories`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.

---

## Templates

### Summary Report Template

```markdown
✅ **ARCHIVING COMPLETE**

**Episodic Memory**:
- Archived automatically (tagged finished): [X] themes
- Archived by decision (from the ask list): [D] themes
- Remaining active: [Y] themes
- Protected (newest per project, newest overall, undated): [P] records

**Emotional Moments** (curated by importance-to-self):
- Kept: [A] moments (foundational / defining)
- Archived: [B] moments
- Active total: [A] moments (newest-first)

**Archiving Rationale**:
[Brief summary of the curation — which moments were kept and which archived, and why]
```
