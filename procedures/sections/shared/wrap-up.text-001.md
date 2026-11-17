# Wrap Up Session

End-of-session **memory** orchestrator: update memory → persist the store → report. Capturing a session and saving it are one job here rather than two — the procedure writes the memory layers and then commits whatever the active storage backend needs committing, so a session never ends with its own record written but unsaved.

What it does not touch is the working project: no project push, no orientation map. Those belong to a coding/environment add-on, which composes a fuller project wrap-up on top of this one.

**Delta-aware**: re-running `/wrap-up` after more work auto-scopes evaluations to the delta (theme match → cutoff = prior sub-episode timestamp). `/wrap-up fresh` forces full-session re-eval.

**Execution style**: silent. Run the steps silently — tool calls stay visible, but no prose narration. Produce ONE report block at the final step as the only user-facing output.

