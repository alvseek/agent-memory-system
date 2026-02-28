# Add Knowledge Memory Protocol

Capture domain expertise, technical patterns, research findings, and best practices that enhance agent capabilities.

## Arguments

`$ARGUMENTS`

- `/add-knowledge [context]` → Document the knowledge described in context
- `/add-knowledge` → Will ask for context

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

### Step 2: Choose Location

- **Project-Specific**: Create in `knowledge-base/[project-folder]/` (project context)
- **Research/Domain**: Create in `knowledge-base/research/` (specialized expertise)

### Step 3: Name File

- **Format**: `[date]-[descriptive-theme].md` or `[domain-area].md`
- **Examples**:
  - `2025-09-11-nestjs-patterns.md` (dated research)
  - `typescript-best-practices.md` (timeless domain knowledge)
  - `project-alpha-architecture.md` (project-specific)

### Step 4: Create File with Structure

Use the [Knowledge File Template](#knowledge-file-template)

**Quality Standards:**
- Back claims with sources, documentation, or proven experience
- Include links to official documentation when available
- Reference specific examples or case studies
- Distinguish between proven practices and experimental approaches

### Step 5: Update Knowledge Index

- Update `//@agent-memory/agent-[domain]/agent-memory-index.md` knowledge directory
- Add entry to knowledge index for discoverability
- Consider whether new knowledge should be core vs. specialized

**Cross-Reference Standards:**
- Use markdown links for all file references: `[Pattern Name](file.md)`
- Include context in link text: `[Database Migration Strategy](migrations.md#strategy)`
- Test links to ensure they work properly

---

## Templates

### Knowledge File Template

```markdown
# Agent - [Knowledge Area] - [Date]

## 📋 **TABLE OF CONTENTS**
- [Purpose](#purpose)
- [Quick Reference](#quick-reference)
- [Section 1](#section-1)
- [Section 2](#section-2)
- [Sources](#sources)

## **PURPOSE**
[Brief description of what this knowledge file covers]

## ⚡ **Quick Reference**
[Key takeaways, patterns, or cheat sheet]

## 🎯 **[Main Content Sections]**
[Organized knowledge content here]

## 🎯 **Sources**
[Context or source of learning]
```

---
