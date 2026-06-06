# Load Episodic Memory Protocol

Load past episodic memory files from the agent's `episodes/` folder into working memory. Supports paginated listing or keyword-based matching against episode filenames and summaries.

## Arguments

`$ARGUMENTS`

- `/load-episodic` → List the 10 most recent episodes with numbers, user selects which to load (paginated with `more`)
- `/load-episodic [keyword]` → Auto-match episodes by keyword against filenames and summaries, load matches directly. Falls back to list mode if no match found

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: Read Episode Index

Read `//@agent-memory/agent-[domain]/agent-memory-index.md` and locate the `# Recent Context Episodes` section.

Parse the episode entries. Each entry follows this format:
```
📂 YYYY-MM-DD:
- [filename.md](episodes/filename.md) - summary text
```

Build a list of all episodes ordered newest-first (as they appear in the index), capturing:
- **File path**: `episodes/[filename.md]`
- **Date**: from the `📂 YYYY-MM-DD:` group header
- **Summary**: the text after the ` - ` separator

If no episodes found, inform the user: "No episodic memory files found. Use `/update-episodic` to create your first one."

### Step 2: Parse Arguments

Check if arguments were provided:
- **No arguments**: Go to Step 3 (List Mode)
- **Arguments provided**: Go to Step 4 (Match Mode)

### Step 3: List Mode (Paginated)

Present the 10 most recent episodes as a numbered list:

**Format:**
```
Recent episodes (showing 1-10 of [total]):

  1. [YYYY-MM-DD] [filename] — [summary]
  2. [YYYY-MM-DD] [filename] — [summary]
  ...
 10. [YYYY-MM-DD] [filename] — [summary]

Enter number(s) to load (e.g., "1", "1,3"), "more" for next 10, or "cancel":
```

**Pagination:**
- If the user replies `more`, show the next 10 episodes (numbered 11-20, then 21-30, etc.)
- Continue until all episodes are shown or the user makes a selection
- On the last page, omit the `"more"` option

After user selection, go to Step 5.

### Step 4: Match Mode

Search for the keyword(s) from arguments against:
1. **Filenames**: Match against the episode filename (e.g., keyword "readme" matches `agent-memory-readme-memory-in-action-improvement.md`). Legacy dated filenames like `2026-03-03-20.56-agent-memory-readme-memory-in-action-improvement.md` still match by the same keywords — only the date prefix is being phased out.
2. **Summaries**: Match against the one-line summary text (e.g., keyword "wizard" matches summaries containing "high-wizard")

Matching is case-insensitive.

**If matches found**: Show what will be loaded and proceed to Step 5:
```
Found [N] episode(s) matching "[keyword]":
  1. [YYYY-MM-DD] [filename] — [summary]
  2. [YYYY-MM-DD] [filename] — [summary]

Loading...
```

**If no matches found**: Inform the user and fall back to Step 3 (List Mode):
```
No episodes matching "[keyword]" found. Showing recent episodes:
```

### Step 5: Load Selected Files

Read the selected episode file(s) from `//@agent-memory/agent-[domain]/episodes/` into agent context using the Read tool.

After loading, confirm to the user:
```
Loaded [N] episode(s):
  - [filename] ([YYYY-MM-DD])
```

---
