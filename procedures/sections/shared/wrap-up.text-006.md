### Step 3: Wrap-Up Report (only visible output)

**Completion gate** (UUID a1b2c3d4): report completion only when Step 2 confirms this session's memory is persisted. Apply the selected backend's persistence and failure rules below.

**On success**, print this block:

```
Wrap-up complete (mode: [agent / all] · [fresh / delta from CUTOFF]):

Memory update:
- Phase 1 — Promoted artifacts: project context: [updated/created — file / skipped] / reasoning: [added — pattern name / skipped] / knowledge: [added — entry name / skipped]
- Phase 2 — Session captured: [appended to / created] [name] ([timestamp]) — [brief theme]; carry-forward: [N items / N/A]; promotions: [N markers / none]
- Phase 3 — Feeling captured: emotional [captured — polarity + clearest criterion / skipped — brief reason]

