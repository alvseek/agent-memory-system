# Update Memory Protocol

Comprehensive memory update orchestrator. Five phases:

- **Phase 0** — Detect delta vs fresh mode (theme match)
- **Phase 1** — Two gated auto-evals (reasoning / knowledge)
- **Phase 2** — Pre-scan promotion markers + episodic capture
- **Phase 3** — Emotional 5-criteria gate (deep-emotion anchoring, polarity-neutral)
- **Phase 4** — Report

`/update-episodic` writes only the episodic layer. `/update-memory` is the full end-of-session orchestrator (what `/wrap-up` invokes). *Storage-specific reads/scans are delegated to the active backend; the gates below are storage-agnostic.*

**Execution style**: silent. Run Phases 0-3 silently — tool calls stay visible, but no prose narration of phases. Produce only the Phase 4 Step 6 summary block. (When invoked by `/wrap-up`, even that is folded into the caller's summary.)

