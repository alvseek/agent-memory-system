# Knowledge File Template

The structure of a knowledge-base entry. Storage-agnostic: the markdown backend creates a file with this structure; the DB backend passes it as the `content` of an `insert(record_type="knowledge", …)`.

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
