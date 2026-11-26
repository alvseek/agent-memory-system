+++
format_version = 2
id = "update-memory"
kind = "procedure"
title = "Update Memory Protocol"
description = "Save what’s new in this conversation to episodic memory, along with any reusable lessons or significant emotional moments that qualify."
argument_name = "mode"
argument_description = "Optional new: create a new episode instead of appending to a matching one"
calls = ["update-reasoning", "update-knowledge", "update-episodic", "update-emotional"]
+++
# Update Memory Protocol

Save what’s new in this conversation to episodic memory, along with any reusable lessons or significant emotional moments that qualify.

**Execution style**: silent. Run Phases 0-3 silently. Produce only the Phase 4 Step 6 summary block. (When invoked by `/wrap-up`, even that is folded into the caller's summary.)

## Arguments

`$ARGUMENTS` — optional `new`. Pass it to create a new episode instead of letting `/update-episodic` match or create one. It does not change which work is evaluated.

---

## Phase 0 — Set the evaluation window

Review what’s new in this chat. For the first memory update, review from the beginning. After that, review only what happened since the last successful memory update in this chat.

---

## Phase 1 — Save reusable lessons

Review only the work identified in Phase 0.

- **Reasoning:** Propose a lesson only when it gives the agent a reusable rule for future decisions, supported by recurring experience or the user’s explicit decision to apply it going forward. Pass the rule and a concrete example to `/update-reasoning`; use its outcome and rule name in the report.
- **Knowledge:** If the conversation produced a reusable finding worth looking up again across projects, pass the finding and its supporting evidence to `/update-knowledge`. Use its outcome and entry name in the report.

Skip either step when nothing qualifies or the lesson was already saved during this conversation.

---

## Phase 2 — Save the episode

Call `/update-episodic` with the work identified in Phase 0. Forward `new` only if supplied. Return the episode's **Tech Debts** and **Next Steps** to the caller for its report.

---

## Phase 3 — Save a significant emotional moment

All 5 must pass:

1. Something meaningful happened beyond routine work.
2. It had a real impact.
3. Its significance outlasts the immediate task.
4. It matters to how we work, make decisions, or relate to each other.
5. The user's own words in the Phase 0 window show why the moment mattered to them. Routine approval alone does not qualify.

If all five are true, call `/update-emotional` with the matching moment type (`happy`, `sad`, `frustrated`, or `bonding`). Provide the event and the user's exact quote as context. Otherwise, skip it.

---

## Phase 4 — Report

### Step 6: Summary

Report completion only after all required writes succeed. If the update is incomplete, identify the failed write rather than marking a new cutoff.

```markdown
✅ MEMORY UPDATE COMPLETE

Mode: [fresh / delta since <previous successful update in this conversation>]

Phase 1 — Reusable lessons (scope: [full session / delta since CUTOFF]):
- Reasoning pattern: [added / refined / skipped] — [rule name if evaluated; otherwise why skipped]
- Knowledge: [added / updated / skipped] — [entry name if evaluated; otherwise why skipped]

Phase 2 — Session captured:
- Episodic: [appended to / created] [name] — [brief theme]
- Carry-forward: [N prior open items carried when appending / N/A for a new episode]

Phase 3 — Feeling captured (scope: [full session / delta since CUTOFF]):
- Emotional: [captured / skipped] — [moment type and why it mattered, if captured]
```
