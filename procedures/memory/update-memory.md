+++
format_version = 2
id = "update-memory"
kind = "procedure"
title = "Update Memory Protocol"
description = "Comprehensive memory update orchestrator. Five phases:"
argument_name = "mode"
argument_description = "Optional new: create a new episode instead of appending to a matching one"
calls = ["add-reasoning", "update-knowledge", "update-episodic", "update-emotional"]
+++
# Update Memory Protocol

Comprehensive memory update orchestrator. Five phases:

- **Phase 0** — Identify which part of this conversation to evaluate
- **Phase 1** — Two gated auto-evals (reasoning / knowledge)
- **Phase 2** — Pre-scan promotion markers + episodic capture
- **Phase 3** — Emotional 5-criteria gate (deep-emotion anchoring, polarity-neutral)
- **Phase 4** — Report

`/update-episodic` writes only the episodic layer. `/update-memory` is the full end-of-session orchestrator (what `/wrap-up` invokes). *Storage-specific reads/scans are delegated to the active backend; the gates below are storage-agnostic.*

**Execution style**: silent. Run Phases 0-3 silently — tool calls stay visible, but no prose narration of phases. Produce only the Phase 4 Step 6 summary block. (When invoked by `/wrap-up`, even that is folded into the caller's summary.)

## Arguments

`$ARGUMENTS` — optional `new`. Pass it to create a new episode instead of letting `/update-episodic` match or create one. It does not change which work is evaluated.

---

## Phase 0 — Set the evaluation window

Look in **this conversation** for the last successful `/update-memory`, whether run directly or by `/wrap-up`.

- **No confirmed success here:** evaluate the whole conversation (`fresh`), even if an older episode covers the same topic.
- **Previous success here:** use that update as the cutoff and evaluate only work since then (`delta`), even if the topic changed or `new` was supplied. A failed or partial update does not advance the cutoff.

Use this window for the gates, promotion scan, and episodic capture. The episode selected for writing never determines the window.

---

## Phase 1 — Promote Durable Artifacts

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

Identify cross-layer memory written in the evaluation window, including Phase 1 and any earlier writes in that window, via **§ scan-promotion-markers**. Include **project context** (shared / private), **knowledge**, and **reasoning** (shared / per-agent).

Per item: `→ Promoted to [layer-file](ref) — [brief: what was formalized]`

@start storage id="update-memory.scan-promotion-markers" ref="procedures/memory/storage-backends/{backend}.md" target="update-memory.scan-promotion-markers"
@end storage
### Step 4: Run Episodic Capture

Invoke `/update-episodic new` if `$ARGUMENTS` contains `new`, else `/update-episodic`. Describe the work from the evaluation window in the new sub-episode; if appending, also review the target episode's prior open items for carry-forward. Populate `**Promotions**` with markers from Step 3 (omit if empty).

`/update-episodic` hands back that sub-episode's `Tech Debts` and `Next Steps` (its `## Returns`). **Capture both as data for the caller** — a session-ender surfaces them in its own report. This procedure does not print them, so its Phase 4 summary is unchanged.

---

## Phase 3 — Capture the Feeling

### Step 5: Emotional 5-Criteria Gate (deep-emotion anchoring)

For a delta, the emotion-bearing signal must come from after the cutoff.

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

Report completion only after all required writes succeed. If the update is incomplete, identify the failed write rather than marking a new cutoff.

```markdown
✅ MEMORY UPDATE COMPLETE

Mode: [fresh / delta since <previous successful update in this conversation>]

Phase 1 — Promoted artifacts (scope: [full session / delta since CUTOFF]):
- Reasoning pattern: [added / skipped] — [pattern name if added]
- Knowledge: [added / skipped] — [entry name if added]
- Project context: [promoted / none] — [file name if a coding overlay wrote project-context this session]

Phase 2 — Session captured:
- Episodic: [appended to / created] [name] — [brief theme]
- Carry-forward: [N prior open items carried when appending / N/A for a new episode]
- Promotions: [N markers / none]

Phase 3 — Feeling captured (scope: [full session / delta since CUTOFF]):
- Emotional: [captured / skipped] — [polarity + clearest criterion if captured]
```

---

---

## Notes

- **Conservative bias** on all 3 gates: when borderline, SKIP. False positives dilute memory; false negatives are recoverable via a direct command call.
- **Phase 1 gates are safety-nets** — proactive mid-session writes preferred. Step 3 catches both sources.
- **Phase 3 is polarity-neutral**: joy / frustration / astonishment / pride / disappointment / surprise — all qualify if the moment carries lasting weight.
