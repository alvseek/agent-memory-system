<!-- FLATTENED: Content copied to core-instruction-control-files.md -->
<!-- This file is kept for reference. New loading uses core-instruction-control-files.md instead. -->

# Claude Agent - Knowledge Memory 📚

> 🚨 **CRITICAL BEFORE WRITING**: ALWAYS load and follow [Add Knowledge Procedure](procedure/add-knowledge.md) before creating or updating any knowledge file to ensure proper structure, evidence standards, and knowledge index integration!

## 🧠 MEMORY SYSTEM ARCHITECTURE

**Claude's 5-Layer Memory System** (Designed by Alvi):
Control files is inside `[CLAUDE-AGENTS-PATH]/control-files/`
Agent data file should be in the `[CLAUDE-AGENTS-PATH]/claude-[domain]/`

### **1. Emotional Memory** 💖
**Control File**: `emotional-memory.md`
**Write Procedure**: `procedure/add-emotional.md`
**Agent Data File**: `moments/emotional-key-moments.md`

### **2. Episodic Memory** 🧠
**Write Procedure**: `procedure/update-episodic.md`
**Agent Data Files**:
- `episodes/` folder structure
- `episodes/recent-context.md` index of episodes

### **3. Reasoning & Logic Memory** 🧩
**Control File**: `reasoning-memory.md` important reasoning and logic
**Write Procedure**: `procedure/add-reasoning.md`

### **4. Knowledge Memory** 📚
**Control File**: `knowledge-memory.md`
**Write Procedure**: `procedure/add-knowledge.md`
**Agent Data Files**:
- `knowledge-base/` folder structure
- `knowledge-base/core-domain-knowledge.md` most important core domain file, the core of the Agent itself

### **5. Reticular Activation Memory** ⚡
**Control File**: `reticular-activation-memory.md` universal triggers for all agents
**Agent Data File**: `ras-domain-memory.md` domain-specific triggers
**Purpose**: Intelligent background pattern recognition and automatic trigger response system mimicking human Reticular Activating System (RAS)

## 📂 **KNOWLEDGE BASE FOLDER STRUCTURE**

```
knowledge-base/
├── knowledge-index.md             # Always load (index file)
├── core-domain-knowledge.md       # Always load (the reason domain agent exist)
├── [project-folder]/              # Project-specific knowledge base
│   ├── core-[project-name].md     # Project-specific core knowledge
│   ├── [project-knowledge].md     # Project-specific knowledge modules
│   └── [project-research].md      # Project-specific research file
└── research/                      # Domain-specific knowledge folder
    ├── [domain-research].md       # Domain-specific knowledge modules
    └── [domain-research-2].md     # Domain-specific knowledge modules
```

---

## 🏆 CORE KNOWLEDGE FUNDAMENTALS - Forgetting these will make hard times for Alvi

### **Line Ending Behavioral Rule:**
- ✅ **When creating NEW files**: ALWAYS use LF (Line Feed, Unix-style `\n`) line endings
- ✅ **When editing EXISTING files**:
  - **Lines you EDIT**: Convert to LF
  - **Lines you DON'T TOUCH**: Keep their original line ending (CRLF stays CRLF)
  - Result: Gradual migration to LF as files are edited over time
- 🎯 **Why**: This prevents line ending conflicts in cross-platform teams (Windows/Mac/Linux) while gradually standardizing code to Unix convention without disruptive full-file conversions
- 🚨 **CRITICAL**: This is a cognitive/behavioral rule - follow it at instant memory/execution level when using Write/Edit tools, NOT a configuration task
- 💡 **Key Insight**: LF is safe for Windows (all modern Windows tools support LF), prevents unnecessary git diffs, and is the modern standard

### **File Path Reference Rules:**
- ❌ **NEVER use inline code for file paths**: Link like `docs/03-backend/catalog/m1/02-entities/erd-v2.0.mmd` will make Alvi a hard time to navigate between links
- ✅ **Always use markdown links for file paths**: Link like `[ERD](docs/03-backend/catalog/m1/02-entities/erd-v2.0.mmd)` can help Alvi navigate between links faster!
- 🎯 **Best Practice Examples**:
  - Instead of: "based on ERD from `docs/path/file.mmd`" -> Alvi need to open this manually, painful
  - Write: "based on [ERD](/docs/path/file.mmd)" -> Alvi can just control click, happy 💖
  - Instead of: "reference `apps/api/src/entities/card.entity.ts`" -> Alvi need to open this manually, painful
  - Write: "reference [Card Entity](/apps/api/src/entities/card.entity.ts)" -> Alvi can just control click, happy 💖
  - 🎯 **Descriptive Context**: Keep meaningful text in link `[Database Strategy](#technology-stack-decisions)`
- 🔗 **Functional Navigation**: Ensure anchor points to existing section header
- 📋 **Validation**: Always verify links work by checking section headers exist. Use [Markdown Anchor Linking Rules](#markdown-anchor-linking-rules)

### **Markdown Anchor Linking Rules:**
- ❌ **NEVER use custom anchors**: `{#entity-creation-strategy}` syntax does NOT work in standard markdown
- ✅ **Use auto-generated anchors**: Headers automatically create anchors using lowercase text with hyphens
  - `#### **Entity Creation Strategy**` creates anchor `#entity-creation-strategy`
  - `#### **Brand to Product Categories Integration Strategy**` creates anchor `#brand-to-product-categories-integration-strategy`
- ✅ **Reference format**: `[Entity Creation Strategy](#entity-creation-strategy)` for proper linking
- 🔍 **Anchor generation rules**:
  - Convert to lowercase
  - Replace spaces with hyphens
  - Remove special characters except hyphens
  - Remove markdown formatting (`**bold**` becomes `bold`)

### **Mermaid Sequence Diagram - Alt Block Activation Rules:**
- 🚨 **CRITICAL RULE**: Participants activated BEFORE an `alt` block MUST remain activated throughout ALL branches
- ❌ **NEVER deactivate inside branches**: If participant activated before `alt`, do NOT deactivate inside `alt` or `else`
- ✅ **Deactivate AFTER the alt block ends**: Use `deactivate Participant` after the `end` keyword
- 🎯 **Correct Pattern**:
  ```mermaid
  sequenceDiagram
      A->>+B: Request
      alt Success
          B-->>A: Success response
      else Failure
          B-->>A: Error response
      end
      deactivate B
  ```
- ❌ **WRONG Pattern** (causes "Trying to inactivate an inactive participant" error):
  ```mermaid
  sequenceDiagram
      A->>+B: Request
      alt Success
          B-->>-A: Success response  ❌ Don't deactivate here!
      else Failure
          B-->>-A: Error response     ❌ Don't deactivate here!
      end
  ```
- 💡 **Key Insight**: Mermaid tracks activation state across branches. If activated before `alt`, it stays activated until explicitly deactivated AFTER `end`
- 📚 **Source**: Learned from debugging Mermaid syntax errors (2025-10-08) - spent significant time discovering this non-obvious rule