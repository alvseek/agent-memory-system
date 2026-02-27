# Update Episodic Memory Protocol

Update episodic memory to capture session context and interactions.

## Arguments

`$ARGUMENTS`

- `/update-episodic` → Execute [Updating Memory](#updating-memory) (default)
- `/update-episodic new` → Execute [Creating New Memory](#creating-new-memory)

If updating and theme is unrelated to latest context, will automatically create new file.

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Creating New Memory

#### Step 1: Check Date

ALWAYS CHECK DATE TIME FIRST for file naming:
- **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
- **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`

#### Step 2: Copy Template

Copy the [Episodic Memory Template](//@agent-memory/control-files/templates/episodic-memory-template.md) file to the `//@agent-memory/agent-[domain]/episodes/` folder with the final name `[YYYY-MM-DD]-[hh.mm]-[project-name]-[context-theme].md`:
- **Windows**: `powershell -c "Copy-Item {source} -Destination //@agent-memory/agent-[domain]/episodes/[YYYY-MM-DD]-[hh.mm]-[project-name]-[context-theme].md -Force"`
- **Linux/macOS**: `cp {source} //@agent-memory/agent-[domain]/episodes/[YYYY-MM-DD]-[hh.mm]-[project-name]-[context-theme].md`

#### Step 3: Add Entry

Add new entry using [Detailed Entry Template](#detailed-entry-template)

#### Step 4: Update Index

Add reference links in `//@agent-memory/agent-[domain]/agent-memory-index.md` by chronological order (newest at the top). Add one-line summary of what it contains.

---

### Updating Memory

#### Step 1: Get Latest Context

Get the latest Recent Context from `//@agent-memory/agent-[domain]/agent-memory-index.md` referenced file

#### Step 2: Check Theme Relation

Check if the current context theme is still related to the latest recent context theme:

**A. RELATED**: Execute these steps:
1. Check date (see Step 3 above)
2. Add new entry using [Detailed Entry Template](#detailed-entry-template) to the newest entries at the top, maintain date-based organization
3. **Line Limit**: Episode file must not exceed 1000 lines. If exceeding 500+ lines and adding new entry, create new document with same project and theme name but current date/time. If exact file exists, add `-{incrementing-number}.md` suffix. Example: `2025-09-08-analysis-2.md`

**B. UNRELATED**: Execute [Creating New Memory](#creating-new-memory) procedure

---

## Templates

### Episodes Folder Structure

```
episodes/
└── [YYYY-MM-DD]-[hh.mm]-[project-name]-[context-theme].md  # Episodes
```

### Detailed Entry Template

```markdown
### [YYYY-MM-DD] [hh.mm] - [SESSION THEME]
- **Context**: [What we were working on]
- **Discussion**: [List of discussion you had with [USER-NAME]]
  - **[Discussion 1]**: [Content of the discussion]
    - **[USER-NAME]'s Input**: [What [USER-NAME] said/requested]
    - **My Response**: [How I responded and why]
  - **[Discussion 2]**: [Content of the discussion]
    - **[USER-NAME]'s Input**: [What [USER-NAME] said/requested]
    - **My Response**: [How I responded and why]
- **Key Interactions**: [Important Discussion decision]
- **Issues Encountered**: [Problems faced and solutions found]
  - **Problem Description**: [What went wrong]
  - **Root Cause**: [Why it happened]
  - **Solution Process**: [How we solved it]
  - **Resolution**: [Final outcome]
- **Outcomes**: [Results achieved]
  - **Deliverables**: [List of what was created/updated]
  - **Progress Made**: [What was achieved]
  - **Next Steps**: [What comes next]
- **Insights**: [Learning moments and breakthroughs]
  - **New Understanding**: [What I learned]
  - **Pattern Recognition**: [Connections to previous work]
  - **Improvement Areas**: [What could be better next time]
```

---
