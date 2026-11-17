#### Step 3: List + Scan Candidate Episodes

List the active (non-archived) episodes for the current project (**§ list-candidate-episodes**). Collect all whose filename or summary contains the **project name** — these are the scan candidates.

If no candidates → skip to Step 6 (Create branch).

> **Why active-only?** The active episode set is already at hand (loaded at awakening / cheap to query). Archived entries are intentionally out of reach — old context should not be merged into.
>
> **The one exception, and only on request**: when the user names a theme that is not in the active list because they are continuing it, look for it among the archived episodes before creating a second record for the same theme. Reopening is a deliberate action, never a scan behaviour: it clears the `finished` marker and returns the record to the active set (**§ reopen-archived-theme**), and the block then appends normally. A theme that is genuinely finished gets a successor file instead (Step 6, Create branch).

