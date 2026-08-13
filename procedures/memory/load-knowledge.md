# Load Knowledge Memory Protocol

Load knowledge-base entries into working memory. Supports listing all available knowledge or loading specific entries by keyword. *Where* knowledge is listed/loaded from is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)).

## Arguments

`$ARGUMENTS`

- `/load-knowledge` → List all knowledge entries with letters, user selects which to load
- `/load-knowledge [keyword]` → Auto-match entries by keyword against descriptions, names, and topic group headers, load matches directly. Falls back to list mode if no match found

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: List Knowledge

List all knowledge entries (**§ list-knowledge**), capturing per entry:
- **Reference**: how to load it (path or id)
- **Title**: the entry title
- **Description**: the one-line description
- **Topic group**: the group it belongs to

> **Scope**: this loads **general** knowledge (research, core-domain, cross-cutting) — cross-project. Project-scoped knowledge is handled by the coding overlay, not here.

If no knowledge entries found, inform the user: "No knowledge files found. Use `/update-knowledge` to create your first one."

### Step 2: Parse Arguments

- **No arguments**: Go to Step 3 (List Mode)
- **Arguments provided**: Go to Step 4 (Match Mode)

### Step 3: List Mode

Present all knowledge entries as a lettered list grouped by topic:

```
Knowledge files available:

[Topic Group 1]
  a. [Title] — [description]
  b. [Title] — [description]

Enter letter(s) to load (e.g., "a", "a,c", "all"), or "cancel":
```

Wait for user selection, then go to Step 5.

### Step 4: Match Mode

Search the keyword(s) against **descriptions**, **names**, and **topic group headers** (case-insensitive).

**If matches found**: show what will be loaded and proceed to Step 5:
```
Found [N] knowledge file(s) matching "[keyword]":
  a. [Title] — [description]

Loading...
```

**If no matches found**: inform the user and fall back to Step 3 (List Mode):
```
No knowledge files matching "[keyword]" found. Showing all available:
```

### Step 5: Load Selected

Load the selected entry/entries into context (**§ load-knowledge-body**). After loading, confirm:
```
Loaded [N] knowledge file(s):
  - [Title] (from [topic group])
```

---

## Storage Mechanics

The operations referenced above — **§ list-knowledge**, **§ load-knowledge-body** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## load-knowledge`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## load-knowledge`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.
