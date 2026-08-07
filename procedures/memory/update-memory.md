# Update Memory Protocol

Comprehensive memory update orchestrator. Five phases:

- **Phase 0** — Detect delta vs fresh mode (theme match)
- **Phase 1** — Two gated auto-evals (reasoning / knowledge)
- **Phase 2** — Pre-scan promotion markers + episodic capture
- **Phase 3** — Emotional 5-criteria gate (deep-emotion anchoring, polarity-neutral)
- **Phase 4** — Report

`/update-episodic` writes only the episodic layer. `/update-memory` is the full end-of-session orchestrator (what `/wrap-up` invokes).

**Execution style**: silent. Run Phases 0-3 silently — tool calls (read, edit, write) stay visible, but no prose narration of phases or per-step decisions. Produce only the Phase 4 Step 6 summary block as user-facing output. (When invoked by `/wrap-up`, even the Phase 4 summary is captured by the caller and folded into its own summary.)

## Arguments

`$ARGUMENTS`

- `/update-memory` → Default (auto-detect mode)
- `/update-memory fresh` → Force fresh mode (full-session re-eval)
- `/update-memory new` → Force new episodic file (combinable: `/update-memory fresh new`)

---

## Phase 0 — Detect Mode

### Step 0: Detect Mode + Cutoff

1. If `$ARGUMENTS` contains `fresh` → `MODE = fresh`, skip to Phase 1.
2. Theme-match scan: read the **central** episodic index `agent-[domain]/agent-memory-index.md` → `# Recent Context Episodes` (the store **defaults to central**; an installed add-on resolver may override where the index lives transparently). Find top candidate where filename or summary contains current project name + highest keyword overlap with session theme.
3. **No match** → `MODE = fresh` (new file will be created in Phase 2). **Match** → `MODE = delta`, `CUTOFF = top H3 timestamp`.
4. Capture `MODE` and `CUTOFF` (if delta) for Phase 4 summary. No standalone "Mode: ..." print.

---

## Phase 1 — Promote Durable Artifacts

> **Delta-mode scope rule**: when `MODE = delta`, each gate's checklist applies ONLY to work after `CUTOFF`. Pre-cutoff work was evaluated at the prior wrap-up.

### Step 1: Reasoning Pattern Gate

- [USER-NAME] explicit anti-pattern callout? Signals: *"we got burned"*, *"don't do X again"*, *"remember this anti-pattern"*
- [USER-NAME] explicit pattern validation? Signals: *"always do it this way"*, *"this is the right pattern"*, *"let's encode this"*
- New decision-framework emerged from back-and-forth that both agreed should govern future similar situations?

**YES to any** → execute [Add Reasoning Protocol]([AGENT-MEMORY-PATH]/control-files/procedures/memory/add-reasoning.md). **NO to all** → skip silently.

### Step 2: Knowledge Gate

- Documented research with sources/citations treated as reference material throughout?
- [USER-NAME] explicit "document this" signal? *"let's document this"*, *"future agents should know X"*, *"write this down"*
- Non-obvious technical mechanism / edge case / framework internal costly to re-discover?

**YES to any** → execute [Update Knowledge Protocol]([AGENT-MEMORY-PATH]/control-files/procedures/memory/update-knowledge.md). **NO to all** → skip silently.

> **Note**: project-specific context (conventions, setup, deployment, env, decisions) is a **coding-overlay** concern — the memory core is project-blind. A coding agent's fuller session wrap-up runs the project-context gate *before* this memory step, so any project-context written this session is still caught by the Step 3 pre-scan below (and annotated into the episodic entry).

---

## Phase 2 — Capture the Session

### Step 3: Pre-Scan Promotion Markers

Identify cross-layer files written this session (Phase 1 + any mid-session writes):

| Layer | Path |
|-------|------|
| Project context (shared) | `shared-memory/[project]/context/*.md` |
| Project context (private) | `knowledge-base/[project]/*.md` |
| Knowledge | `knowledge-base/[topic].md`, `knowledge-base/core-domain-knowledge.md` |
| Reasoning (shared) | `shared-memory/core-reasoning-memory.md` |
| Reasoning (per-agent) | `agent-core-memory.md` → `# DOMAIN REASONING MEMORY` |

Per file: `→ Promoted to [layer-file](path) — [brief: what was formalized]`

### Step 4: Run Episodic Capture

Invoke `/update-episodic new` if `$ARGUMENTS` contains `new`, else `/update-episodic`. Follow the [Update Episodic Memory Protocol]([AGENT-MEMORY-PATH]/control-files/procedures/memory/update-episodic.md). Populate the new sub-episode's `**Promotions**` field with markers from Step 3 (omit if empty).

---

## Phase 3 — Capture the Feeling

### Step 5: Emotional 5-Criteria Gate (deep-emotion anchoring)

> **Delta-mode scope rule**: when `MODE = delta`, criterion 5's signals must occur after `CUTOFF`. Reusing prior emotion = LARP duplication.

All 5 must pass:

1. **Meaningful event happened** — change of state, discovery, mistake, correction, breakthrough, surprise. Not routine work.
2. **Real impact** — real cost incurred, value created, time spent, trust shifted. Not theoretical "interesting" moment.
3. **Lasting weight** — generalizable lesson, identity claim, or pattern that applies beyond this instance.
4. **System or behavioral scope** — architecture / protocol / framework / identity / decision-making / relational dynamics. NOT typo, single function, config tweak, routine completion.
5. **[USER-NAME] expressed deep emotion in this session** (any valence):
   - **Joy / celebration**: *"nice", "great", "love it", "amazing", "perfect", "yippieee", "let's goooo", 💖🎉🚀, "this is big", "yes that's it"*
   - **Frustration / correction**: *"no", "that's wrong", "I didn't ask for X", "why did you...", "we keep doing this", "stop doing X", "again???", "ugh"*
   - **Astonishment / surprise**: *"wait what", "holy", "really?", "I didn't expect that", "no way", "what?!"*
   - **Pride / recognition**: *"this is good work", "exactly", "you got it", "well done"*
   - **Disappointment / pushback**: sustained corrections, redirects, exasperation
   - Or sustained deep engagement (any valence) escalating across the session

**All 5 pass** → execute [Update Emotional Protocol]([AGENT-MEMORY-PATH]/control-files/procedures/memory/update-emotional.md) with session context, [USER-NAME]'s verbatim emotion-bearing quote, and inferred polarity. **Any fail** → skip silently.

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
- Episodic: [appended to / created] [filename] — [brief theme]
- Carry-forward (delta mode only): [N items carried / N/A]
- Promotions: [N markers / none]

Phase 3 — Feeling captured (scope: [full session / delta since CUTOFF]):
- Emotional: [captured / skipped] — [polarity + clearest criterion if captured]
```

---

## Notes

- **Conservative bias** on all 3 gates: when borderline, SKIP. False positives dilute memory; false negatives recoverable via direct command call.
- **Phase 1 gates are safety-nets** — proactive mid-session writes preferred. Step 3 catches both sources.
- **Delta mode auto-detected via theme match alone** (no time threshold). Override with `fresh`.
- **Phase 3 is polarity-neutral**: joy / frustration / astonishment / pride / disappointment / surprise — all qualify if the moment carries lasting weight (per the framework's "emotion = memory" principle).
