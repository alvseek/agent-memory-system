# Load Project Context Protocol

Load project-specific context files from the agent's `knowledge-base/[project]/` folder into working memory. Supports listing all available context or loading specific files by keyword.

## Arguments

`$ARGUMENTS`

- `/load-project-context` → List all project context files with numbers, user selects which to load
- `/load-project-context [keyword]` → Auto-match files by keyword against tags and file names, load matches directly. Falls back to list mode if no match found

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: Scan Available Project Context

Scan `//@agent-memory/agent-[domain]/knowledge-base/` for project subfolders (exclude `research/` folder — that's domain knowledge, not project context).

For each project subfolder found, read its `context-index.md` to get the list of available context files with descriptions and tags.

If no project subfolders or context-index files are found, inform the user: "No project context files found. Use `/update-project-context` to create your first one."

### Step 2: Parse Arguments

Check if arguments were provided:
- **No arguments**: Go to Step 3 (List Mode)
- **Arguments provided**: Go to Step 4 (Match Mode)

### Step 3: List Mode

Present all project context files as a numbered list grouped by project:

**Format:**
```
Project context files available:

[project-name-1]
  1. [theme].md — [description] (tags: tag1, tag2)
  2. [theme].md — [description] (tags: tag1, tag2)

[project-name-2]
  3. [theme].md — [description] (tags: tag1, tag2)

Enter number(s) to load (e.g., "1", "1,3", "all"), or "cancel":
```

Wait for user selection, then go to Step 5.

### Step 4: Match Mode

Search for the keyword(s) from arguments against:
1. **Tags**: Match against `tags: [...]` in YAML frontmatter
2. **File names**: Match against the file name (e.g., keyword "deploy" matches `deployment.md`)
3. **Project names**: Match against project folder names

**If matches found**: Show what will be loaded and proceed to Step 5:
```
Found [N] matching context file(s) for "[keyword]":
  1. [project]/[theme].md — [description]
  2. [project]/[theme].md — [description]

Loading...
```

**If no matches found**: Inform the user and fall back to Step 3 (List Mode):
```
No context files matching "[keyword]" found. Showing all available:
```

### Step 5: Load Selected Files

Read the selected file(s) into agent context using the Read tool.

After loading, confirm to the user:
```
Loaded [N] project context file(s):
  - [project]/[theme].md (tags: tag1, tag2)
```

---
