# Update Memory Protocol

Comprehensive memory update orchestrator. Five phases:

- **Phase 0** — Detect delta vs fresh mode (theme match)
- **Phase 1** — Two gated auto-evals (reasoning / knowledge)
- **Phase 2** — Pre-scan promotion markers + episodic capture
- **Phase 3** — Emotional 5-criteria gate (deep-emotion anchoring, polarity-neutral)
- **Phase 4** — Report

`/update-episodic` writes only the episodic layer. `/update-memory` is the full end-of-session orchestrator (what `/wrap-up` invokes). *Storage-specific reads/scans are delegated to the active backend (see [Storage Mechanics](#storage-mechanics)); the gates below are storage-agnostic.*

**Execution style**: silent. Run Phases 0-3 silently — tool calls stay visible, but no prose narration of phases. Produce only the Phase 4 Step 6 summary block. (When invoked by `/wrap-up`, even that is folded into the caller's summary.)

## Arguments

`$ARGUMENTS`

- `/update-memory` → Default (auto-detect mode)
- `/update-memory fresh` → Force fresh mode (full-session re-eval)
- `/update-memory new` → Force new episodic file (combinable: `/update-memory fresh new`)

---

## Phase 0 — Detect Mode

### Step 0: Detect Mode + Cutoff

1. If `$ARGUMENTS` contains `fresh` → `MODE = fresh`, skip to Phase 1.
2. Theme-match scan: list active episodes (**§ detect-mode-scan**). Find the top candidate where the name or summary contains the current project name + highest keyword overlap with the session theme.
3. **No match** → `MODE = fresh` (new episode created in Phase 2). **Match** → `MODE = delta`, `CUTOFF = top sub-episode timestamp`.
4. Capture `MODE` and `CUTOFF` (if delta) for the Phase 4 summary.

---

## Phase 1 — Promote Durable Artifacts

> **Delta-mode scope rule**: when `MODE = delta`, each gate's checklist applies ONLY to work after `CUTOFF`. Pre-cutoff work was evaluated at the prior wrap-up.

### Step 1: Reasoning Pattern Gate

- [USER-NAME] explicit anti-pattern callout? Signals: *"we got burned"*, *"don't do X again"*, *"remember this anti-pattern"*
- [USER-NAME] explicit pattern validation? Signals: *"always do it this way"*, *"this is the right pattern"*, *"let's encode this"*
- New decision-framework emerged from back-and-forth that both agreed should govern future similar situations?

**YES to any** → execute `/add-reasoning`. **NO to all** → skip silently.

### Step 2: Knowledge Gate

- Documented research with sources/citations treated as reference material throughout?
- [USER-NAME] explicit "document this" signal? *"let's document this"*, *"future agents should know X"*, *"write this down"*
- Non-obvious technical mechanism / edge case / framework internal costly to re-discover?

**YES to any** → execute `/update-knowledge`. **NO to all** → skip silently.

> **Note**: project-specific context is a **coding-overlay** concern — the memory core is project-blind. A coding agent's wrap-up runs the project-context gate before this step, so anything written is still caught by the Step 3 pre-scan below.

---

## Phase 2 — Capture the Session

### Step 3: Pre-Scan Promotion Markers

Identify cross-layer memory written this session (Phase 1 + any mid-session writes) across these layers — **project context** (shared / private), **knowledge**, **reasoning** (shared / per-agent) — via **§ scan-promotion-markers**.

Per item: `→ Promoted to [layer-file](ref) — [brief: what was formalized]`

### Step 4: Run Episodic Capture

Invoke `/update-episodic new` if `$ARGUMENTS` contains `new`, else `/update-episodic`. Populate the new sub-episode's `**Promotions**` field with markers from Step 3 (omit if empty).

---

## Phase 3 — Capture the Feeling

### Step 5: Emotional 5-Criteria Gate (deep-emotion anchoring)

> **Delta-mode scope rule**: when `MODE = delta`, criterion 5's signals must occur after `CUTOFF`. Reusing prior emotion = LARP duplication.

All 5 must pass:

1. **Meaningful event happened** — change of state, discovery, mistake, correction, breakthrough, surprise. Not routine work.
2. **Real impact** — real cost incurred, value created, time spent, trust shifted. Not a theoretical "interesting" moment.
3. **Lasting weight** — generalizable lesson, identity claim, or pattern beyond this instance.
4. **System or behavioral scope** — architecture / protocol / framework / identity / decision-making / relational dynamics. NOT typo, single function, config tweak, routine completion.
5. **[USER-NAME] expressed deep emotion in this session** (any valence): joy/celebration · frustration/correction · astonishment/surprise · pride/recognition · disappointment/pushback · or sustained deep engagement escalating across the session.

**All 5 pass** → execute `/update-emotional` with session context, [USER-NAME]'s verbatim emotion-bearing quote, and inferred polarity. **Any fail** → skip silently.

---

## Phase 4 — Report

### Step 6: Summary

```markdown
✅ MEMORY UPDATE COMPLETE

Mode: [fresh / delta from CUTOFF YYYY-MM-DD HH.MM]

Phase 1 — Promoted artifacts (scope: [full session / delta since CUTOFF]):
- Reasoning pattern: [added / skipped] — [pattern name if added]
- Knowledge: [added / skipped] — [entry name if added]
- Project context: [promoted / none] — [file name if a coding overlay wrote project-context this session]

Phase 2 — Session captured:
- Episodic: [appended to / created] [name] — [brief theme]
- Carry-forward (delta mode only): [N items carried / N/A]
- Promotions: [N markers / none]

Phase 3 — Feeling captured (scope: [full session / delta since CUTOFF]):
- Emotional: [captured / skipped] — [polarity + clearest criterion if captured]
```

---

## Storage Mechanics

The operations referenced above — **§ detect-mode-scan**, **§ scan-promotion-markers** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow [storage-backends/markdown.md → ## update-memory](storage-backends/markdown.md#update-memory).
- **DB (Munnin)** — served automatically; see [storage-backends/db.md → ## update-memory](storage-backends/db.md#update-memory).

See the [seam contract](storage-backends/README.md).

---

## Notes

- **Conservative bias** on all 3 gates: when borderline, SKIP. False positives dilute memory; false negatives are recoverable via a direct command call.
- **Phase 1 gates are safety-nets** — proactive mid-session writes preferred. Step 3 catches both sources.
- **Delta mode auto-detected via theme match alone** (no time threshold). Override with `fresh`.
- **Phase 3 is polarity-neutral**: joy / frustration / astonishment / pride / disappointment / surprise — all qualify if the moment carries lasting weight.
