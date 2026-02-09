# Claude Agent - Episodic Memory Write Procedure🧠

## EPISODES FOLDER STRUCTURE

```
episodes/
├── recent-context.md              # Read the references (table of contents)
└── [YYYY:MM:DD]-[hh.mm]-[project-name]-[context-theme].md      # Organized episodes by relevance
```

## Writing the Episodic Memory 

### **Creating New Memory**: 
*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*
1. I need to copy the [Episodic Memory Template](//@claude-agents/control-files/write-procedure/episodic-memory-template.md) file to the `//@claude-agents/claude-[domain]/episodes/` folder:
   - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
   - **Linux/macOS**: `cp {source} {target}`
2. I have to rename the file based on [EPISODES FOLDER STRUCTURE](#episodes-folder-structure)
3. I have to add new entry using [Detailed Entry Template](#detailed-entry-template). ALWAYS DOUBLE CHECK YOUR DATE TIME BEFORE WRITING:
   - **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
   - **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`
4. After created a new episodic memory file, you have to add reference links in `//@claude-agents/claude-[domain]/agent-memory-index.md` or `//@claude-agents/claude-[domain]/episodes/recent-context.md` by chronological order (newest at the top). Add one-line summary of what it contains

### **Updating Memory**:
*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*
1. I have to get the latest Recent Context from `//@claude-agents/claude-[domain]/agent-memory-index.md` or `//@claude-agents/claude-[domain]/episodes/recent-context.md` referenced file 
2. I have to check if the current context theme is still related to the latest recent context theme:
  A. RELATED: I have to execute these steps:
    1. Add new entry using [Detailed Entry Template](#detailed-entry-template) to the Newest entries at the top, maintain date-based organization. ALWAYS DOUBLE CHECK YOUR DATE TIME BEFORE WRITING:
      - **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
      - **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`
    2. Limit of episode files: To get a clearer context, an episode file must not contain more than 1000 lines. If you want to add a new entry, and the line already exceeding 500+, please create a new document with the same project and theme name, but with current date and time. If the exact same file is already exist, add *-{incrementing-number}.md at the end. Example: 2025-09-08-analysis-2.md.
  B. UNRELATED: I have to execute [Creating New Memory](#creating-new-memory)

### Detailed Entry Template ###

### [YYYY-MM-DD] [hh.mm] - [SESSION THEME]
- **Context**: [What we were working on]
- **Discussion**: [List of discussion you had with Alvi]
  - **[Discussion 1]**: [Content of the discussion]
    - **Alvi's Input**: [What Alvi said/requested]
    - **My Response**: [How I responded and why]
  - **[Discussion 2]**: [Content of the discussion]
    - **Alvi's Input**: [What Alvi said/requested]
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