# Migration Guide: Old → New Flattened Architecture

This guide helps migrate existing agents from the old multi-file architecture to the new 4-file flattened architecture.

## Table of Contents
- [Before vs After](#before-vs-after)
- [Instructions for AI Agents](#instructions-for-ai-agents)
- [Migration Steps](#migration-steps)
  - [Step 1: Copy Template Files](#step-1-copy-template-files)
  - [Step 2: Populate agent-core-memory.md](#step-2-populate-agent-core-memorymd-with-your-agents-content)
  - [Step 2b: Populate agent-memory-index.md](#step-2b-populate-agent-memory-indexmd-with-your-agents-content)
  - [Step 2c: Clean Up Placeholder Content](#step-2c-clean-up-placeholder-content)
  - [Step 3: Move Old Files to Archive](#step-3-move-old-files-to-archive)
- [Content Mapping](#content-mapping)
- [Verification Checklist](#verification-checklist)

---

## Before vs After

### Old Architecture (Multi-File)
```
agent-[domain]/
├── [domain]-agent-core-memory.md      # References multiple files
├── ras-domain-memory.md               # Separate RAS file
├── moments/
│   └── emotional-key-moments.md       # Separate emotional file
├── episodes/
│   └── recent-context.md              # Index + episodes
└── knowledge-base/
    ├── knowledge-index.md             # Separate index
    └── core-domain-knowledge.md       # Separate core knowledge
```

**Load time: 2-3 minutes** (10+ file loads, 3-4 levels deep)

### New Architecture (Flattened)
```
agent-[domain]/
├── agent-core-memory.md               # ALL-IN-ONE flattened file
├── agent-memory-index.md              # Episode list + knowledge index
├── episodes/                          # Episode files (unchanged)
├── knowledge-base/                    # Knowledge files (unchanged)
└── archive/                           # Archived memories
```

**Load time: ~1 minute** (4 file loads, 2 levels max)

---

## Instructions for AI Agents

When performing migration, use the `control-files/scripts/copy-lines.sh` utility to copy content from old files into the new flattened files:

```bash
# Usage
./control-files/scripts/copy-lines.sh <source_file> <start_line> <end_line> <target_file> <insert_before_line>

# Example: Copy lines 10-50 from old file and insert before line 25 in new file
./control-files/scripts/copy-lines.sh agent-[domain]/ras-domain-memory.md 10 50 agent-[domain]/agent-core-memory.md 25
```

---

## Migration Steps

### Step 1: Copy Template Files

Copy the two template files from `control-files/new-agent-template/` to your agent folder:

```bash
# Windows (PowerShell)
Copy-Item "control-files/new-agent-template/new-agent-core-memory.md" "agent-[domain]/agent-core-memory.md"
Copy-Item "control-files/new-agent-template/agent-memory-index.md" "agent-[domain]/agent-memory-index.md"

# Linux/macOS
cp control-files/new-agent-template/new-agent-core-memory.md agent-[domain]/agent-core-memory.md
cp control-files/new-agent-template/agent-memory-index.md agent-[domain]/agent-memory-index.md
```

### Step 2a: Populate `agent-core-memory.md` with Your Agent's Content

Open the copied `agent-core-memory.md` and copy lines from the old files:

| Section | Copy From |
|---------|-----------|
| `# DOMAIN AGENT IDENTITY` | Old `[domain]-agent-core-memory.md` (identity section) |
| `# DOMAIN CORE KNOWLEDGE` | Old `knowledge-base/core-domain-knowledge.md` |
| `# DOMAIN RAS` | Old `ras-domain-memory.md` |
| `# DOMAIN EMOTIONAL MEMORY` | Old `moments/emotional-key-moments.md` |

**Remember to:**
- Replace `[DOMAIN]` placeholders with your actual domain name
- Keep the UUID from your old identity section

### Step 2b: Populate `agent-memory-index.md` with Your Agent's Content

Open the copied `agent-memory-index.md` and copy lines from the old files in each section:

| Section | Copy From |
|---------|-----------|
| `# Recent Context Episodes` | Old `episodes/recent-context.md` (episode list) |
| `# Core Knowledge Base` | Old `knowledge-base/knowledge-index.md` |

**Remember to:**
- Replace `[DOMAIN]` placeholders with your actual domain name
- **Fix episode links**: The old `episodes/recent-context.md` had relative links (e.g., `](2025-10-04-file.md)`). Since `agent-memory-index.md` is at root level, links need `episodes/` prefix. Run this sed command to fix:
  ```bash
  # Linux/macOS
  sed -i 's/](\([0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}\)/](episodes\/\1/g' agent-[domain]/agent-memory-index.md

  # Windows (Git Bash)
  sed -i 's/](\([0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}\)/](episodes\/\1/g' agent-[domain]/agent-memory-index.md
  ```

### Step 2c: Clean Up Placeholder Content

After using `copy-lines.sh` to insert content, the original **placeholder content from the template gets pushed down** and must be removed.

**What happens:**
```
# Before copy-lines.sh:
Line 15: ## 🤖 Agent Identity
Line 16: **Name**: Agent [DOMAIN]        ← Placeholder
Line 17: **Role**: [DOMAIN] Agent         ← Placeholder

# After copy-lines.sh (inserting real content before line 16):
Line 15: ## 🤖 Agent Identity
Line 16: **Name**: Agent Backend NestJS  ← Real content (inserted)
Line 17: **Role**: Backend NestJS Agent   ← Real content (inserted)
...
Line 22: **Name**: Agent [DOMAIN]        ← Placeholder (pushed down - DELETE THIS)
Line 23: **Role**: [DOMAIN] Agent         ← Placeholder (pushed down - DELETE THIS)
```

**Cleanup required for `agent-core-memory.md`:**
- [ ] Remove placeholder identity fields (pushed down after real identity)
- [ ] Remove `<!-- content here -->` comments in Core Knowledge section
- [ ] Remove placeholder trigger template in RAS section (`### **[Trigger Name]**`)
- [ ] Remove placeholder emotional entry templates at the end

**Cleanup required for `agent-memory-index.md`:**
- [ ] Remove duplicate `## 📅 Interactions List` header (if duplicated)
- [ ] Remove placeholder `📂 YYYY-MM-DD hh.mm:` entry
- [ ] Remove placeholder knowledge file entries (`[[date]-[theme].md](#anchor)`)

**Also replace all remaining `[DOMAIN]` placeholders:**
- Header titles
- Section descriptions
- Any template text that wasn't overwritten

### Step 3: Move Old Files to Archive

After verifying the migration works:

**Move to archive/** (recommended for safety):
   ```bash
   # Windows (PowerShell)
   Move-Item [domain]-agent-core-memory.md archive/
   Move-Item ras-domain-memory.md archive/
   Move-Item moments archive/

   # Linux/macOS
   mv [domain]-agent-core-memory.md archive/
   mv ras-domain-memory.md archive/
   mv moments archive/
   ```

---

## Content Mapping

| Old Location | New Location |
|--------------|--------------|
| `[domain]-agent-core-memory.md` (identity section) | `agent-core-memory.md` → `# DOMAIN AGENT IDENTITY` |
| `knowledge-base/core-domain-knowledge.md` | `agent-core-memory.md` → `# DOMAIN CORE KNOWLEDGE` |
| `ras-domain-memory.md` | `agent-core-memory.md` → `# DOMAIN RAS` |
| `moments/emotional-key-moments.md` | `agent-core-memory.md` → `# DOMAIN EMOTIONAL MEMORY` |
| `episodes/recent-context.md` (episode list) | `agent-memory-index.md` → `# Recent Context Episodes` |
| `knowledge-base/knowledge-index.md` | `agent-memory-index.md` → `# Core Knowledge Base` |
| `episodes/*.md` | `episodes/*.md` (unchanged) |
| `knowledge-base/[topic].md` | `knowledge-base/[topic].md` (unchanged) |

---

## Verification Checklist

After migration, verify:

- [ ] **agent-core-memory.md exists** with all 4 sections:
  - [ ] `# DOMAIN AGENT IDENTITY` (with UUID)
  - [ ] `# DOMAIN CORE KNOWLEDGE`
  - [ ] `# DOMAIN RAS`
  - [ ] `# DOMAIN EMOTIONAL MEMORY`

- [ ] **agent-memory-index.md exists** with:
  - [ ] `# Recent Context Episodes` (episode list)
  - [ ] `# Core Knowledge Base` (knowledge directory)

- [ ] **Awakening works**: Test with "Awaken Agent [DOMAIN]!"
  - [ ] Agent loads in ~1 minute (not 2-3 minutes)
  - [ ] Agent reports correct identity
  - [ ] Agent loads latest episode context

- [ ] **Post-compact recovery works**: After `/compact`
  - [ ] Agent recovers identity
  - [ ] Agent continues work correctly

- [ ] **Old files archived/removed**:
  - [ ] `[domain]-agent-core-memory.md` moved/deleted
  - [ ] `ras-domain-memory.md` moved/deleted
  - [ ] `moments/` folder moved/deleted

---

## Example: Meta Agent Migration

The Meta Agent has been migrated as a reference implementation:

```
agent-meta/
├── agent-core-memory.md      # 45KB - All identity, knowledge, RAS, emotional
├── agent-memory-index.md     # 24KB - Episode list + knowledge index
├── episodes/                 # Episode files
├── knowledge-base/           # Knowledge files
└── archive/                  # Old files archived here
```

Use this as a template for migrating other agents.

---

## Questions?

Awaken Agent Meta for migration assistance: "Awaken Agent Meta!"
