# Load Episodic Memory Protocol

Load past episodic memory into working memory. Supports paginated listing or keyword matching against episode summaries. *Where* episodes are listed/loaded from is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)).

## Arguments

`$ARGUMENTS`

- `/load-episodic` → List the 10 most recent episodes with numbers, user selects which to load (paginated with `more`)
- `/load-episodic [keyword]` → Auto-match episodes by keyword against filenames and summaries, load matches directly. Falls back to list mode if no match found

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: List Episodes

List all episodes ordered newest-first (**§ list-episodes**), capturing per entry:
- **Reference**: how to load the episode (path or id)
- **Date**: the entry's date
- **Summary**: the one-line summary

If no episodes found, inform the user: "No episodic memory files found. Use `/update-episodic` to create your first one."

### Step 2: Parse Arguments

- **No arguments**: Go to Step 3 (List Mode)
- **Arguments provided**: Go to Step 4 (Match Mode)

### Step 3: List Mode (Paginated)

Present the 10 most recent episodes as a numbered list:

```
Recent episodes (showing 1-10 of [total]):

  1. [YYYY-MM-DD] [name] — [summary]
  ...
 10. [YYYY-MM-DD] [name] — [summary]

Enter number(s) to load (e.g., "1", "1,3"), "more" for next 10, or "cancel":
```

**Pagination**: on `more`, show the next 10 (11-20, 21-30, …). Continue until all shown or a selection is made; omit `"more"` on the last page. After selection, go to Step 5.

### Step 4: Match Mode

Search the keyword(s) against episode **names** and **summaries** (case-insensitive).

**If matches found**: show what will be loaded and proceed to Step 5:
```
Found [N] episode(s) matching "[keyword]":
  1. [YYYY-MM-DD] [name] — [summary]

Loading...
```

**If no matches found**: inform the user and fall back to Step 3 (List Mode):
```
No episodes matching "[keyword]" found. Showing recent episodes:
```

### Step 5: Load Selected

Load the selected episode(s) into context (**§ load-episode-body**). After loading, confirm:
```
Loaded [N] episode(s):
  - [name] ([YYYY-MM-DD])
```

---

## Storage Mechanics

The operations referenced above — **§ list-episodes**, **§ load-episode-body** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## load-episodic`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## load-episodic`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.
