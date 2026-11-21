+++
format_version = 2
id = "update-knowledge"
kind = "procedure"
title = "Update Knowledge Memory Protocol"
description = "Capture domain expertise, technical patterns, research findings, and best practices that enhance agent capabilities. *How* the knowledge store + index are written is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics))."
argument_name = "context"
argument_description = "Input described in the procedure's Arguments section"
+++
@start storage id="caller-context" ref="procedures/memory/storage-backends/{backend}.md" target="caller-context"
@end storage
# Update Knowledge Memory Protocol

Capture domain expertise, technical patterns, research findings, and best practices that enhance agent capabilities. *How* the knowledge store + index are written is delegated to the active **storage backend**.

## Arguments

`$ARGUMENTS`

- `/update-knowledge [context]` → Document the knowledge described in context
- `/update-knowledge` → Will ask for context

If no arguments provided, ask: "What knowledge or domain expertise should I document?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: Evaluate Capture Criteria

**Capture when:**
- Domain expertise discoveries (new frameworks, libraries, patterns)
- Technical patterns (architectural solutions, design patterns)
- Research findings (comparative analysis, benchmarks, evaluations)
- Best practices with evidence (proven approaches backed by data)
- Specialized knowledge enhancing capabilities (tooling, methodologies)

**Don't capture:**
- Temporary workarounds or project-specific hacks
- Unverified claims or assumptions
- Context already covered in existing knowledge files
- Information that should be in episodic memory instead

> **Scope**: `/update-knowledge` writes **general** knowledge (research, core-domain, cross-cutting) — cross-project, always **central**. Project-specific context (VM access, deploy procedures, conventions) + project-scoped knowledge are handled by the coding overlay, not here.

### Step 2: Compose from the Template

Compose the entry using the knowledge-file template (**§ template**).

**Quality Standards:**
- Back claims with sources, documentation, or proven experience
- Include links to official documentation when available
- Reference specific examples or case studies
- Distinguish between proven practices and experimental approaches

@start storage id="update-knowledge.template" ref="procedures/memory/storage-backends/{backend}.md" target="update-knowledge.template"
@end storage
### Step 3: Persist

Persist the composed entry into the knowledge store (**§ persist-knowledge**).

@start storage id="update-knowledge.persist-knowledge" ref="procedures/memory/storage-backends/{backend}.md" target="update-knowledge.persist-knowledge"
@end storage
### Step 4: Confirm Knowledge Discoverability

Ensure the entry is discoverable through the knowledge directory (**§ update-knowledge-index**). Consider whether new knowledge should be core vs. specialized.

**Cross-Reference Standards:**
- Use markdown links for all file references: `[Pattern Name](file.md)`
- Include context in link text: `[Database Migration Strategy](migrations.md#strategy)`
- Test links to ensure they work properly

---

@start storage id="update-knowledge.update-knowledge-index" ref="procedures/memory/storage-backends/{backend}.md" target="update-knowledge.update-knowledge-index"
@end storage
