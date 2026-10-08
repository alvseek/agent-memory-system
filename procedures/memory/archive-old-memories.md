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

### Step 2: Archive Recent Context (Episodic Memory)

1. Review the active episode set.
2. **Identify episodes to archive** (user specifies cutoff date or criteria) — e.g. "archive all older than 2025-09-01", "archive all but last 10".
3. **Archive them** (**§ archive-episodes**): archived episodes drop out of the hot/active set but their bodies are retained and remain reachable on demand.

### Step 3: Archive Emotional Key Moments

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

### Step 4: Verification

- ✅ Archive updated properly (full blocks present, newest-first)
- ✅ Active memory still well-organized (newest first)
- ✅ Kept blocks **unchanged/verbatim**, archived blocks gone from active
- ✅ Counts reconcile: (kept + archived) == original moment count; nothing silently dropped
- ✅ No CRLF introduced (LF preserved) and archive references resolve

### Step 5: Report Summary

Provide a summary using the [Summary Report Template](#summary-report-template).

---

## Storage Mechanics

The operations referenced above — **§ stamp-date**, **§ archive-episodes**, **§ archive-emotional-apply** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## archive-old-memories`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## archive-old-memories`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.

---

## Templates

### Summary Report Template

```markdown
✅ **ARCHIVING COMPLETE**

**Episodic Memory**:
- Archived: [X] episodes from [date range]
- Active: [Y] episodes remaining

**Emotional Moments** (curated by importance-to-self):
- Kept: [A] moments (foundational / defining)
- Archived: [B] moments
- Active total: [A] moments (newest-first)

**Archiving Rationale**:
[Brief summary of the curation — which moments were kept and which archived, and why]
```
