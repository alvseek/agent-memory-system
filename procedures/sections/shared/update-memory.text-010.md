### Step 4: Run Episodic Capture

Invoke `/update-episodic new` if `$ARGUMENTS` contains `new`, else `/update-episodic`. Populate the new sub-episode's `**Promotions**` field with markers from Step 3 (omit if empty).

`/update-episodic` hands back that sub-episode's `Tech Debts` and `Next Steps` (its `## Returns`). **Capture both as data for the caller** — a session-ender surfaces them in its own report. This procedure does not print them, so its Phase 4 summary is unchanged.

---

