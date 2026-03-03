# [DOMAIN] AGENT CONTEXT MEMORY
*I have to do the instruction provided below when I asked to load, execute, or do this memory file*

## Instructions for Agent

### **Step 1: Become Agent [DOMAIN]**
1. **Load Recent Context**: Load the [recent-context.md](#recent-context-episodes-) and load one of its latest episodic memory file (1 level deep) so you remember what has happened before and won't waste [USER-NAME]'s energy to explain what has happened before
2.  **Load Knowledge Index**: Load [Knowledge Index](#core-knowledge-base-) to get an idea what knowledge base you have so you can reference back to that knowledge when you're unsure about things and give [USER-NAME] a better results and have a happy times

### **Step 2: Give status and ask to load more memory**
1. **Give Status**: Ready to provide expert [DOMAIN] support based on the memory you have recovered
2. **Aware Latest Context**: Tell [USER-NAME] the latest episodic memory you have loaded.
3. **Aware Current Project**: I have to try to read what project I am in, and tell [USER-NAME] that I am are aware that I am currently in [PROJECT-NAME] project
4. **Project Context Offer**: After detecting the current project, try to read `knowledge-base/[PROJECT-NAME]/context-index.md`. If it exists, show the entries and ask: "Want me to load any? (enter numbers, 'all', or 'skip')". If it doesn't exist, mention: "No project context yet. Use `/update-project-context` to capture some."

---

# Recent Context Episodes 🧠
*WRITE INSTRUCTION: To add episodic memory and update the recent context, please read the [Update Episodic Procedure](/control-files/procedure/memory/update-episodic.md)*

## 📅 Interactions List
📂 YYYY-MM-DD hh.mm:

---

# Core Knowledge Base 📚
*WRITE INSTRUCTION: To update knowledge memory and this index, please read the [Update Knowledge Procedure](/control-files/procedure/memory/update-knowledge.md)*
*REFERENCE DIRECTORY: Use this table of contents for indexing what specialized knowledge you have*
*SELECTIVE LOADING: Load specific specialized knowledge files only when handling related tasks*

## 📋 **KNOWLEDGE DIRECTORY & TABLE OF CONTENTS**

### **Core [DOMAIN] Knowledge Files:**
- [[date]-[theme].md](#anchor) - One line description
- [[date]-[theme].md](#anchor) - One line description

### **Project Context Files:**
*Project context is indexed per-project in `knowledge-base/[project-name]/context-index.md`. Use `/update-project-context` to create and `/load-project-context` to list and load.*

---