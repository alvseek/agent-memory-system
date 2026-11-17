### § create-episode

1. **Build filename**: `[project-name]-[context-theme].md` (no date prefix). Examples: `agent-memory-task-system-framework-rules.md`, `plko-jira-mcp-integration.md`. If a file at this name already exists (and a separate file is wanted), use an incrementing suffix: `[project-name]-[context-theme]-2.md`.
2. **Copy the file scaffold**:
   ```
   cp [AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/episodic-memory-template.md [AGENT-MEMORY-PATH]/agent-[domain]/episodes/[filename].md
   ```
3. **Set the frontmatter `project`** in the new file to the project name, then **replace the template placeholder** at the top with the composed sub-episode block. The frontmatter is what the importer reads into the record's `project`; the filename is convention, not the source.
4. **Add index entry**:
   - Insert at the **top of today's date group** (`📂 YYYY-MM-DD:`); create today's group if it doesn't exist.
   - Entry format: `- [filename.md](episodes/filename.md) - [one-line summary]`, where the summary is the new block's `**Summary**` row copied verbatim. This entry is the record's listed description, so it and the block must not diverge.

