# Recent Context Episodes 🧠
*WRITE INSTRUCTION: To add episodic memory and update the recent context, please read the [Update Episodic Procedure](/control-files/procedures/memory/update-episodic.md)*

## 📅 Interactions List
📂 YYYY-MM-DD hh.mm:

---

# Core Knowledge Base 📚
*WRITE INSTRUCTION: To update knowledge memory and this index, please read the [Update Knowledge Procedure](/control-files/procedures/memory/update-knowledge.md)*
*REFERENCE DIRECTORY: Use this table of contents for indexing what specialized knowledge you have*
*SELECTIVE LOADING: Load specific specialized knowledge files only when handling related tasks*

## 📋 **KNOWLEDGE DIRECTORY & TABLE OF CONTENTS**

### **Core [DOMAIN] Knowledge Files:**
- [[date]-[theme].md](#anchor) - One line description
- [[date]-[theme].md](#anchor) - One line description

### **Project Context Files:**
*Project context is indexed per-project in two layers:*
- *Per-agent (private):* `knowledge-base/[project-name]/context-index.md` *— domain-specialized facts only this agent needs*
- *Shared (cross-agent):* `shared-memory/[project-name]/context/context-index.md` *— universal facts every agent on the project should know*

*Use `/load-project-context` to browse both layers (entries are marked `[shared]` or `[private]`). Use `/update-project-context` to create new entries — it routes to the right layer based on a heuristic + your confirmation. (These are **coding-overlay** commands — project context is a coding-agent capability; a chat agent using the core alone is project-blind.)*

---