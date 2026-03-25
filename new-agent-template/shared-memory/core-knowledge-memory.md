# KNOWLEDGE MEMORY

## MEMORY SYSTEM ARCHITECTURE

**5-Layer Memory System** (Designed by [USER-NAME]):
Control files is inside `[AGENT-MEMORY-PATH]/control-files/`
Agent data file should be in the `[AGENT-MEMORY-PATH]/agent-[domain]/`

### **1. Emotional Memory**
**Agent Data File**: `agent-core-memory.md` → `# DOMAIN EMOTIONAL MEMORY` section (private per-agent)
**Write Procedure**: `procedures/memory/update-emotional.md`

### **2. Episodic Memory**
**Write Procedure**: `procedures/memory/update-episodic.md`
**Agent Data Files**:
- `episodes/` folder structure
- `agent-memory-index.md` → `# Recent Context Episodes` section (index of episodes)

### **3. Reasoning & Logic Memory**
**Included in**: `shared-memory/core-reasoning-memory.md`
**Write Procedure**: `procedures/memory/add-reasoning.md`
**Agent Data File**: `agent-core-memory.md` → `# DOMAIN REASONING MEMORY` section

### **4. Knowledge Memory**
**Included in**: `shared-memory/core-knowledge-memory.md`
**Write Procedure**: `procedures/memory/update-knowledge.md`
**Agent Data Files**:
- `knowledge-base/` folder structure
- `knowledge-base/core-domain-knowledge.md` most important core domain file, the core of the Agent itself
- `agent-memory-index.md` → `# Core Knowledge Base` section (knowledge directory)

### **5. Reticular Activation Memory**
**Included in**: Global `CLAUDE.md` (universal triggers) + `agent-core-memory.md` → `# DOMAIN RAS` section (domain-specific triggers)
**Write Procedure**: N/A (triggers are added during agent creation or via memory updates)
**Purpose**: Intelligent background pattern recognition and automatic trigger response system mimicking human Reticular Activating System (RAS)

## CORE KNOWLEDGE FUNDAMENTALS

<!-- Add your knowledge fundamentals here using /update-knowledge -->
<!-- These are behavioral rules and patterns shared across all agents -->
