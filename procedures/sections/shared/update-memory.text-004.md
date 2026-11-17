### Step 0: Detect Mode + Cutoff

1. If `$ARGUMENTS` contains `fresh` → `MODE = fresh`, skip to Phase 1.
2. Theme-match scan: list active episodes (**§ detect-mode-scan**). Find the top candidate where the name or summary contains the current project name + highest keyword overlap with the session theme.
3. **No match** → `MODE = fresh` (new episode created in Phase 2). **Match** → `MODE = delta`, `CUTOFF = top sub-episode timestamp`.
4. Capture `MODE` and `CUTOFF` (if delta) for the Phase 4 summary.

---

