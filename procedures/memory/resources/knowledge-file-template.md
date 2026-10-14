# Knowledge File Template

template_version: 2026-10-14-10-00

The structure of a knowledge-base entry. Storage-agnostic: the markdown backend creates a file with this structure; the DB backend passes it as the `content` of an `insert(record_type="knowledge", …)`. Rows carrying `Use "None declared" if genuinely none.` are required (presence-checked); all other rows are optional.

`**Summary**` is the entry's headline and the line the record is listed by. It is authored once here and copied verbatim to wherever the record is listed: the markdown backend's knowledge-index entry, and the DB backend's `content_summary` argument.

```markdown
---
tags: []
---
# Agent - [Knowledge Area] - [Date]

- **Summary**: [One line on what this entry holds, in plain words. Use "None declared" if genuinely none.]

## 📋 **TABLE OF CONTENTS**
- [Purpose](#purpose)
- [Quick Reference](#quick-reference)
- [Section 1](#section-1)
- [Section 2](#section-2)
- [Sources](#sources)

## **PURPOSE**
[Brief description of what this knowledge file covers. Use "None declared" if genuinely none.]

## ⚡ **Quick Reference**
[Key takeaways, patterns, or cheat sheet. Use "None declared" if genuinely none.]

## 🎯 **[Main Content Sections]**
[Organized knowledge content here]

## 🎯 **Sources**
[Context or source of learning]
```
