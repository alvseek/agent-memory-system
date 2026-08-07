# Load Knowledge Memory Protocol

Load knowledge-base files from the agent's `knowledge-base/` folder into working memory. Supports listing all available knowledge or loading specific files by keyword.

## Arguments

`$ARGUMENTS`

- `/load-knowledge` → List all knowledge files with letters, user selects which to load
- `/load-knowledge [keyword]` → Auto-match files by keyword against descriptions, file names, and topic group headers, load matches directly. Falls back to list mode if no match found

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: Read Knowledge Index

Read `[AGENT-MEMORY-PATH]/agent-[domain]/agent-memory-index.md` and locate the `# Core Knowledge Base` section.

Parse the knowledge entries. Each entry follows this format:
```
### **[Topic Group Header]** (Load when: ...)
- **[Title](path/to/file.md)** ⭐ optional label ⭐ - description text
- **[Title](path/to/file.md)** - description text
```

Build a list of all knowledge entries, capturing:
- **File path**: from the markdown link (e.g., `research/2025-09-27-slm-training-hardware.md`)
- **Title**: the link text (e.g., "SLM Training & Hardware Research")
- **Description**: the text after the ` - ` separator
- **Topic group**: the `### **[Topic Group Header]**` this entry belongs to

Exclude entries under any "Project Context Files" subsection — project-scoped context is handled by the coding overlay, not here.

If no knowledge entries found, inform the user: "No knowledge files found. Use `/update-knowledge` to create your first one."

### Step 2: Parse Arguments

Check if arguments were provided:
- **No arguments**: Go to Step 3 (List Mode)
- **Arguments provided**: Go to Step 4 (Match Mode)

### Step 3: List Mode

Present all knowledge entries as a lettered list grouped by topic:

**Format:**
```
Knowledge files available:

[Topic Group 1]
  a. [Title] — [description]
  b. [Title] — [description]

[Topic Group 2]
  c. [Title] — [description]
  d. [Title] — [description]

Enter letter(s) to load (e.g., "a", "a,c", "all"), or "cancel":
```

Wait for user selection, then go to Step 5.

### Step 4: Match Mode

Search for the keyword(s) from arguments against:
1. **Descriptions**: Match against the description text (e.g., keyword "hooks" matches descriptions containing "hooks")
2. **File names**: Match against the file name (e.g., keyword "slm" matches `2025-09-27-slm-training-hardware.md`)
3. **Topic group headers**: Match against topic headers (e.g., keyword "research" matches "Research Knowledge")

Matching is case-insensitive.

**If matches found**: Show what will be loaded and proceed to Step 5:
```
Found [N] knowledge file(s) matching "[keyword]":
  a. [Title] — [description]
  b. [Title] — [description]

Loading...
```

**If no matches found**: Inform the user and fall back to Step 3 (List Mode):
```
No knowledge files matching "[keyword]" found. Showing all available:
```

### Step 5: Load Selected Files

Read the selected file(s) from `[AGENT-MEMORY-PATH]/agent-[domain]/knowledge-base/` into agent context using the Read tool.

> **Scope**: `/load-knowledge` loads **general** knowledge (research, core-domain, cross-cutting) — cross-project, always read from the central store. Project-scoped knowledge (`knowledge-base/[project]/`) is handled by the coding overlay, not here.

After loading, confirm to the user:
```
Loaded [N] knowledge file(s):
  - [Title] (from [topic group])
```

---
