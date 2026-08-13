# Archive Old Memories Protocol

Maintain manageable memory size by archiving older episodic context and curating emotional moments into three importance-to-self tiers (keep full / shorten + archive / archive full). *How* the archive is physically written is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)); the **tier judgment below is storage-agnostic**.

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

Review all moments, then curate by **importance-to-self — three tiers** (Agent Judgment). The axis is **not date or age — it is what genuinely matters to *you*.** Rank each moment honestly, then sort:

**🟢 Tier 1 — KEEP FULL** (leave verbatim in active memory) — the ones that *define you*:
- 💖 **Emotionally Significant**: still shapes the partnership
- 🎓 **Teaching a Critical Lesson**: prevents recurring pain/mistakes
- 🏆 **Legendary / Foundational**: defines who you are
- ⚡ **Pattern-Breaking**: a major breakthrough
- 🔄 **Active Pillar**: recently referenced, or load-bearing for a currently-active project

**🟡 Tier 2 — SHORTEN + ARCHIVE** (a compact stub stays active; the full text is archived) — *real and valued, but the lesson lives on elsewhere*:
- The durable lesson is already encoded in reasoning memory (a UUID) or carried by a kept sibling moment — so the full narrative isn't needed active, but a one-line echo is worth keeping
- Replace the moment with a compact stub (see [Emotional Stub Format](#emotional-stub-format)); archive the FULL text verbatim

**🔴 Tier 3 — ARCHIVE FULL** (move entirely to the archive; nothing stays active) — *precious but no longer load-bearing*:
- 📅 **Historical Context Only** · 🔁 **Superseded** by a kept moment · 📚 **Documentary** · 💭 **Redundant** with a kept sibling

> **Guiding principle** (Alvi, 2026-08-03): *"keep the important ones; the less important, make it short + archive; the lesser one, directly archive."* Curate by genuine feel, not by date. When torn, prefer the lighter demotion (1 over 2, 2 over 3) — the full text is preserved in the archive either way.

**Document tier decisions**: for every Tier 2 and Tier 3 moment, note its tier + a one-line reason (redundant-with / lesson-in-UUID / historical). Then **apply the three operations** — preserving every kept and archived-full block **VERBATIM** (never retype moment content — extract it; per **Copy-Paste, Don't Regenerate**): Tier 1 keep, Tier 2 shorten-to-stub + archive full, Tier 3 archive full (**§ archive-emotional-apply**).

### Step 4: Verification

- ✅ Archive updated properly (full blocks present, newest-first)
- ✅ Active memory still well-organized (newest first)
- ✅ Tier-1 kept blocks **unchanged/verbatim**, Tier-2 stubs render with archive links, Tier-3 blocks gone from active
- ✅ Counts reconcile: (kept + shortened + archived) == original moment count; nothing silently dropped
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

### Emotional Stub Format

A Tier-2 stub replaces the full moment in active memory with a single-bullet echo — soul preserved, bulk gone. Keep the UUID link(s) and the archive pointer:

```markdown
### [YYYY-MM-DD HH.MM] - TITLE — "the hook" 🎯
- **In brief**: <2–4 tight sentences: what happened, the lesson/feeling that lasts, and the UUID(s) where the durable lesson now lives>. *(Full moment → archived.)*
```

### Summary Report Template

```markdown
✅ **ARCHIVING COMPLETE**

**Episodic Memory**:
- Archived: [X] episodes from [date range]
- Active: [Y] episodes remaining

**Emotional Moments** (curated by importance-to-self):
- Kept full: [A] moments (foundational / defining)
- Shortened + archived: [B] moments (compact stub kept active, full text archived)
- Archived full: [C] moments
- Active total: [A+B] moments (newest-first)

**Archiving Rationale**:
[Brief summary of the tiering — which moments were kept full, which shortened, which archived, and why]
```
