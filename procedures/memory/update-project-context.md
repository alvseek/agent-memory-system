# Update Project Context Protocol

Create or update project-specific context files. Routes new entries to **shared** (`shared-memory/[project-name]/context/`, for cross-agent universal facts) or **private** (`agent-[domain]/knowledge-base/[project-name]/`, for domain-specialized facts) based on a heuristic + user confirmation. Also supports moving an existing private entry to shared.

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

### Step 2: Determine Scope (Shared vs Private)

Decide whether this context belongs in the **shared** layer (cross-agent universal facts) or the **private** layer (domain-specialized facts for this agent only).

**Heuristic:**
- **Shared** (default when in doubt): Universal facts that are true for every agent on this project. Examples: GitButler usage, deployment process, env vars, repo conventions, infrastructure URLs.
- **Private**: Domain-specialized facts only one agent's role cares about. Examples: backend's DB schemas, frontend's component patterns, PM's stakeholder map.

> **Why this matters**: Under-sharing causes drift (agent A learns a fact, agent B doesn't know it). Over-sharing is just slightly noisier loads. When the call is genuinely ambiguous, default to **shared**.

Present the suggestion via [WAIT Options](//@agent-memory/control-files/procedures/wait-options.md) and wait for confirmation:

```
**Scope determination for "[context summary]":**

- [Brief reason for the suggestion — e.g., "This describes the project's deployment workflow, which applies to every agent."]

  > A) Shared — `shared-memory/[project-name]/context/` `✓✓`
  > B) Private — `agent-[domain]/knowledge-base/[project-name]/`

  ([Reason: why this scope is suggested.])

Reply with "shared", "private", or your preferred scope.
```

Based on the confirmed scope, the subsequent steps will use the matching path:
- **Shared scope**: `//@agent-memory/shared-memory/[project-name]/context/`
- **Private scope**: `//@agent-memory/agent-[domain]/knowledge-base/[project-name]/`

> **Move operation**: If the user has asked to **move** an existing private entry to shared (e.g., "move X to shared", "promote X to shared"), skip the rest of this procedure and follow the [Move-to-Shared Sub-Flow](#move-to-shared-sub-flow) section below.

### Step 3: Check Project Folder

Check if the project folder exists at the scope-aware path determined in Step 2:
- **Shared scope**: `//@agent-memory/shared-memory/[project-name]/context/`
- **Private scope**: `//@agent-memory/agent-[domain]/knowledge-base/[project-name]/`

- **If exists**: Proceed to Step 4
- **If not exists**: Create the folder:
  - Shared: `mkdir -p //@agent-memory/shared-memory/[project-name]/context`
  - Private: `mkdir -p //@agent-memory/agent-[domain]/knowledge-base/[project-name]`

### Step 4: Determine Theme and Check Existing Files

Identify the theme of the context being captured (e.g., `environment-setup`, `deployment`, `auth-module`, `database-conventions`).

Scan existing files in the scope-aware folder to check if a file already covers this theme:
- **If existing file found**: Proceed to Step 5B (Update)
- **If no match**: Proceed to Step 5A (Create New)

### Step 5A: Create New Context File

1. Copy the [Project Context Template](//@agent-memory/control-files/templates/project-context-template.md) to the scope-aware path: `[scope-folder]/[theme].md`
   - Shared: `cp {source} //@agent-memory/shared-memory/[project-name]/context/[theme].md`
   - Private: `cp {source} //@agent-memory/agent-[domain]/knowledge-base/[project-name]/[theme].md`
2. Fill the YAML frontmatter:
   - `project`: the project name from Step 1
   - `tags`: relevant feature/module tags for selective loading (e.g., `[environment, setup, vm, gcloud]`)
   - `description`: one-line summary
   - `created`: today's date
   - `updated`: today's date
3. Fill the markdown sections (Purpose, Quick Reference, Details, Sources)
4. Proceed to Step 6

### Step 5B: Update Existing Context File

1. Read the existing file
2. Update or append relevant content
3. Update the `updated:` date in YAML frontmatter to today's date
4. Update `tags:` if new tags are relevant
5. Proceed to Step 6

### Step 6: Check 1000-Line Limit

Check the file line count after writing:
- **If under 1000 lines**: Proceed to Step 7
- **If over 1000 lines**: The file has grown too large. Split it:
  1. Identify distinct sub-themes within the file
  2. Create separate files for each sub-theme (e.g., `environment-setup.md` splits into `environment-local.md` + `environment-vm.md`)
  3. Each new file gets its own frontmatter with appropriate tags
  4. Remove the original oversized file
  5. Proceed to Step 7 (update index for all new files)

### Step 7: Update Context Index

Update the scope-aware `context-index.md`:
- **Shared**: `//@agent-memory/shared-memory/[project-name]/context/context-index.md`
- **Private**: `//@agent-memory/agent-[domain]/knowledge-base/[project-name]/context-index.md`

- **If the file doesn't exist**, create it with header: `# [project-name] Project Context`
- Add or update the entry for this file
- Format: `- [theme.md](theme.md) — description (tags: tag1, tag2, tag3)`

---

## Move-to-Shared Sub-Flow

When the user explicitly asks to move an existing private entry to shared (e.g., "move X to shared", "promote X to shared"), follow this sub-flow instead of the normal procedure.

### M.1: Identify Source File

Locate the private file to move:
- Source path: `//@agent-memory/agent-[domain]/knowledge-base/[project-name]/[theme].md`
- Source index: `//@agent-memory/agent-[domain]/knowledge-base/[project-name]/context-index.md`

If unclear which theme the user means, ask: "Which file should I move? Available private entries: [list]"

### M.2: Check Collision in Shared

Check if a file with the same theme name already exists in shared:
- `//@agent-memory/shared-memory/[project-name]/context/[theme].md`

- **If no collision**: Proceed to M.3
- **If collision**: **STOP**. Present the conflict to user: "A shared file with this name already exists. Options: A) merge the content manually first, B) rename the private file before moving, C) cancel." Wait for user direction.

### M.3: Write to Shared Location

1. Ensure the shared folder exists:
   `mkdir -p //@agent-memory/shared-memory/[project-name]/context`
2. Copy the private file content (unchanged — same template) to the shared location:
   `cp //@agent-memory/agent-[domain]/knowledge-base/[project-name]/[theme].md //@agent-memory/shared-memory/[project-name]/context/[theme].md`

### M.4: Delete Private File

Remove the private file:
`rm //@agent-memory/agent-[domain]/knowledge-base/[project-name]/[theme].md`

### M.5: Update Both Indexes

1. **Remove entry from private index**: Edit `//@agent-memory/agent-[domain]/knowledge-base/[project-name]/context-index.md` and delete the line referencing this theme
2. **Add entry to shared index**: Edit `//@agent-memory/shared-memory/[project-name]/context/context-index.md` and add the entry (create the index file with `# [project-name] Project Context` header if it doesn't exist):
   - Format: `- [theme.md](theme.md) — description (tags: tag1, tag2, tag3)`

### Partial-Failure Cleanup

This sub-flow is **not atomic** at the filesystem level. If a step fails partway:
- **After M.3 but before M.4**: Both files exist. Manual cleanup: delete the duplicate that shouldn't be there (usually the private one).
- **After M.4 but before M.5**: File is moved but indexes are inconsistent. Manual cleanup: finish the index updates.

If any step fails, report the partial state to user and ask before retrying.

---

## Templates

### Project Context File Template

See [project-context-template.md](//@agent-memory/control-files/templates/project-context-template.md)

---
