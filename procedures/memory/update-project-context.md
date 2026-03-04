# Update Project Context Protocol

Create or update project-specific context files (VM access, environment setup, deployment procedures, feature conventions) in the agent's private `knowledge-base/[project]/` folder.

## Arguments

`$ARGUMENTS`

- `/update-project-context [context]` → Create or update project context described in context
- `/update-project-context` → Will ask for context

If no arguments provided, ask: "What project context should I capture? (e.g., environment setup, deployment procedure, feature conventions)"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: Determine Project Name

Identify the project this context belongs to:
- **From working directory**: Infer project name from the current repository/folder name
- **From user input**: Ask if unclear: "Which project is this context for?"
- **Naming convention**: Use lowercase-hyphenated format (e.g., `ocx-platform`, `my-saas-app`, `data-pipeline`)

### Step 2: Check Project Folder

Check if `knowledge-base/[project-name]/` folder exists in `//@agent-memory/agent-[domain]/`:
- **If exists**: Proceed to Step 3
- **If not exists**: Create the folder:
  `mkdir -p //@agent-memory/agent-[domain]/knowledge-base/[project-name]`

### Step 3: Determine Theme and Check Existing Files

Identify the theme of the context being captured (e.g., `environment-setup`, `deployment`, `auth-module`, `database-conventions`).

Scan existing files in `knowledge-base/[project-name]/` to check if a file already covers this theme:
- **If existing file found**: Proceed to Step 4B (Update)
- **If no match**: Proceed to Step 4A (Create New)

### Step 4A: Create New Context File

1. Copy the [Project Context Template](//@agent-memory/control-files/templates/project-context-template.md) to `knowledge-base/[project-name]/[theme].md`
   `cp {source} //@agent-memory/agent-[domain]/knowledge-base/[project-name]/[theme].md`
2. Fill the YAML frontmatter:
   - `project`: the project name from Step 1
   - `tags`: relevant feature/module tags for selective loading (e.g., `[environment, setup, vm, gcloud]`)
   - `description`: one-line summary
   - `created`: today's date
   - `updated`: today's date
3. Fill the markdown sections (Purpose, Quick Reference, Details, Sources)
4. Proceed to Step 5

### Step 4B: Update Existing Context File

1. Read the existing file
2. Update or append relevant content
3. Update the `updated:` date in YAML frontmatter to today's date
4. Update `tags:` if new tags are relevant
5. Proceed to Step 5

### Step 5: Check 1000-Line Limit

Check the file line count after writing:
- **If under 1000 lines**: Proceed to Step 6
- **If over 1000 lines**: The file has grown too large. Split it:
  1. Identify distinct sub-themes within the file
  2. Create separate files for each sub-theme (e.g., `environment-setup.md` splits into `environment-local.md` + `environment-vm.md`)
  3. Each new file gets its own frontmatter with appropriate tags
  4. Remove the original oversized file
  5. Proceed to Step 6 (update index for all new files)

### Step 6: Update Context Index

Update `//@agent-memory/agent-[domain]/knowledge-base/[project-name]/context-index.md`:
- **If the file doesn't exist**, create it with header: `# [project-name] Project Context`
- Add or update the entry for this file
- Format: `- [theme.md](theme.md) — description (tags: tag1, tag2, tag3)`

---

## Templates

### Project Context File Template

See [project-context-template.md](//@agent-memory/control-files/templates/project-context-template.md)

---
