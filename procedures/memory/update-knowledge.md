# Update Knowledge Memory Protocol

Capture domain expertise, technical patterns, research findings, and best practices that enhance agent capabilities. *How* the knowledge store + index are written is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)).

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

Compose the entry using the [Knowledge File Template](../../templates/knowledge-file-template.md).

**Quality Standards:**
- Back claims with sources, documentation, or proven experience
- Include links to official documentation when available
- Reference specific examples or case studies
- Distinguish between proven practices and experimental approaches

### Step 3: Persist

Persist the composed entry into the knowledge store (**§ persist-knowledge**).

### Step 4: Register in the Knowledge Index

Add an entry to the knowledge directory for discoverability (**§ update-knowledge-index**). Consider whether new knowledge should be core vs. specialized.

**Cross-Reference Standards:**
- Use markdown links for all file references: `[Pattern Name](file.md)`
- Include context in link text: `[Database Migration Strategy](migrations.md#strategy)`
- Test links to ensure they work properly

---

## Storage Mechanics

The operations referenced above — **§ persist-knowledge**, **§ update-knowledge-index** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow [storage-backends/markdown.md → ## update-knowledge](storage-backends/markdown.md#update-knowledge).
- **DB (Munnin)** — served automatically; see [storage-backends/db.md → ## update-knowledge](storage-backends/db.md#update-knowledge).

See the [seam contract](storage-backends/README.md).

---

## Templates

### Knowledge File Template

→ **[templates/knowledge-file-template.md](../../templates/knowledge-file-template.md)**.
