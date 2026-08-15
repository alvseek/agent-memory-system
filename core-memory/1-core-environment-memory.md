## AI Agent - Current Global Work Environment Information
- **Operating System**: Windows
- **Claude Code Bash Tool**: Runs in **Git Bash** (NOT CMD or PowerShell)
  - Use Unix-style commands: `cp`, `rm`, `ls`, `mkdir`, `cat`, `grep`
  - Use forward slashes: `/c/Users/username/.claude/` (not `C:\Users\username\.claude\`)
  - Use Unix conditionals: `test -f file && echo "exists"` (not `if exist file`)
  - CMD syntax like `if exist ... (echo) else (echo)` will FAIL
- **[AGENT-MEMORY-PATH]** = `C:\Work\research\agent-memory\`
- **[STORAGE-BACKENDS-PATH]** = `[AGENT-MEMORY-PATH]\control-files\procedures\memory\storage-backends` (memory procedures' concrete `§ op`s per storage backend — absolute so the pointer survives slash-command install)
- **[GLOBAL-INSTRUCTIONS-FILE]** = `C:\Users\your-name\.claude\CLAUDE.md` (this compiled file's own destination — post-compaction recovery rereads it to restore attention position)
