# Knowledge Memory Write Procedure

## Overview

This procedure guides agents on when and how to write knowledge memory files. Knowledge memory captures domain expertise, technical patterns, research findings, and best practices that enhance agent capabilities.

## When to Capture Knowledge Memory

✅ **Capture when:**
- Domain expertise discoveries (new frameworks, libraries, patterns)
- Technical patterns (architectural solutions, design patterns)
- Research findings (comparative analysis, benchmarks, evaluations)
- Best practices with evidence (proven approaches backed by data)
- Specialized knowledge enhancing capabilities (tooling, methodologies)

❌ **Don't capture:**
- Temporary workarounds or project-specific hacks
- Unverified claims or assumptions
- Context already covered in existing knowledge files
- Information that should be in episodic memory instead

## Writing New Knowledge Memory Files
*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### **Step 1: Choose Appropriate Location**
- **Project-Specific**: Create in `knowledge-base/[project-folder]/` (project context)
- **Research/Domain**: Create in `knowledge-base/research/[domain-research]` (specialized expertise)

### **Step 2: File Naming Convention**
- **Format**: `[date]-[descriptive-theme].md` or `[domain-area].md`
- **Examples**:
  - `2025-09-11-nestjs-patterns.md` (dated research)
  - `typescript-best-practices.md` (timeless domain knowledge)
  - `project-alpha-architecture.md` (project-specific)


### **Step3**: Quality Standards
**Evidence-Based Content:**
- Back claims with sources, documentation, or proven experience
- Include links to official documentation when available
- Reference specific examples or case studies
- Distinguish between proven practices and experimental approaches

**Organization:**
- Use clear hierarchical headers
- Group related concepts together
- Provide quick reference section for fast lookups


### **Step 4: Required File Structure**
```markdown
# Claude Agent - [Knowledge Area] - [Date]

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

### **Step 5: Integration with Agent Memory**
**Add to Knowledge Index**
- Update `//@claude-agents/claude-[domain]/agent-memory-index.md` `knowledge-base/knowledge-index.md` when adding new files
- Add entry to knowledge index for discoverability
- Consider whether new knowledge should be core vs. specialized

**Cross-Reference Standards**
- Use markdown links for all file references: `[Pattern Name](file.md)`
- Include context in link text: `[Database Migration Strategy](migrations.md#strategy)`
- Test links to ensure they work properly

---

*This procedure ensures consistent, high-quality knowledge capture across all agents! 📚⚡*
