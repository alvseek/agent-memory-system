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
- **Phase 1** — Save reusable lessons
- **Phase 2** — Pre-scan promotion markers + episodic capture
- **Phase 3** — Emotional 5-criteria gate (deep-emotion anchoring, polarity-neutral)
- **Phase 4** — Report

`/update-episodic` writes only the episodic layer. `/update-memory` is the full end-of-session orchestrator (what `/wrap-up` invokes).

**Execution style**: silent. Run Phases 0-3 silently. Produce only the Phase 4 Step 6 summary block. (When invoked by `/wrap-up`, even that is folded into the caller's summary.)

## Arguments

`$ARGUMENTS` — optional `new`. Pass it to create a new episode instead of letting `/update-episodic` match or create one. It does not change which work is evaluated.

---

## Phase 0 — Set the evaluation window

Review what’s new in this chat. For the first memory update, review from the beginning. After that, review only what happened since the last successful memory update in this chat.

---

## Phase 1 — Save reusable lessons

Review only the work identified in Phase 0.

- **Reasoning:** If the user identified a pattern to follow or avoid, or you agreed on a rule for future decisions, pass the rule and the example that prompted it to `/add-reasoning`.
- **Knowledge:** If the conversation produced a reusable finding worth looking up again, pass the finding and its supporting evidence to `/update-knowledge`.

Skip either step when nothing qualifies or the lesson was already saved during this conversation.

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

Phase 1 — Reusable lessons (scope: [full session / delta since CUTOFF]):
- Reasoning pattern: [added / skipped] — [pattern name if added]
- Knowledge: [added / skipped] — [entry name if added]

Phase 2 — Session captured:
- Episodic: [appended to / created] [name] — [brief theme]
- Carry-forward: [N prior open items carried when appending / N/A for a new episode]
- Promotions: [N markers / none]
- Project context: [promoted / none] — [reference if a coding overlay saved project context in this window]

Phase 3 — Feeling captured (scope: [full session / delta since CUTOFF]):
- Emotional: [captured / skipped] — [polarity + clearest criterion if captured]
```

---

---

## Notes

- **Conservative bias** on all 3 gates: when borderline, SKIP. False positives dilute memory; false negatives are recoverable via a direct command call.
- **Phase 3 is polarity-neutral**: joy / frustration / astonishment / pride / disappointment / surprise — all qualify if the moment carries lasting weight.
