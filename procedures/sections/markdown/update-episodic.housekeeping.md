### § housekeeping

1. **Check line limit** after an append:
   - **> 500 lines**: warn — *"[filename] over 500 lines, consider splitting on next merge"*.
   - **> 1000 lines**: split — move the *just-added* sub-episode into `[project]-[theme]-2.md` (next incrementing suffix if `-2` exists). Add `> Continues from [original-filename]` at the top of the new file. Add a new index entry for the split file under today's date group.
2. **Lazy filename migration** (one-time per file): if the chosen file still uses the legacy `YYYY-MM-DD-HH.MM-[project]-[theme].md` format, rename it to `[project]-[theme].md` as part of this append and update the index entry's filename reference. If a file at the new name already exists (rare collision), use the line-limit `-{n}` suffix rule.

> **Episodes folder structure**:
> ```
> episodes/
> ├── [project-name]-[context-theme].md        # Active episode file (rolling per theme)
> ├── [project-name]-[context-theme]-2.md      # Split file when 1000-line cap hit
> ├── YYYY-MM-DD-HH.MM-[project]-[theme].md    # Legacy dated files (lazy migration)
> └── archive/                                  # Archived old episodes (via /archive-old-memories)
>     └── YYYY-archived-context.md
> ```
> Legacy filenames are migrated lazily — only renamed when the file gets its next merge-append. No bulk sweep.

