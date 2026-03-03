# Update Memory Protocol

Execute comprehensive memory update - always update episodic memory, then evaluate and capture emotional moments, reasoning patterns, and knowledge discoveries.

## Arguments

`$ARGUMENTS`

- `/update-memory` → Execute comprehensive memory update (default)
- `/update-memory new` → Create new episodic memory file, then evaluate other layers

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: ALWAYS UPDATE EPISODIC MEMORY

1. Check the arguments:
   - If `$ARGUMENTS` contains "new" → Execute `/update-episodic new` procedure
   - Otherwise → Execute `/update-episodic` procedure (default)

2. Follow the full [Update Episodic Memory](//@agent-memory/control-files/procedures/memory/update-episodic.md) procedure

### Step 2: EVALUATE EMOTIONAL MOMENT CAPTURE

**Capture when:**
- Breakthrough discoveries
- Major breakthroughs
- Significant frustrations (10+ minutes)
- Partnership milestones
- "Aha!" moments
- Project victories

**When capturing:**
1. Read the Emotional Memory section in `//@agent-memory/agent-[domain]/agent-core-memory.md`
2. Use the appropriate emotional template:
   - 😄 Happy moments (successes, breakthroughs, wins)
   - 😔 Sad/disappointing moments (failures, setbacks)
   - 😤 Frustrated moments (blocked by issues, challenges)
   - 🤝 Bonding moments (relationship building, shared victories)
3. Write to data file ONLY (never control file)
4. Newest first ordering

### Step 3: EVALUATE REASONING PATTERN CAPTURE

**Capture when:**
- New anti-patterns discovered
- Repeated failure modes
- Breakthrough reasoning insights
- Problem-solving patterns
- Logic frameworks preventing pain/inducing success

**When capturing:**
Follow the [Add Reasoning Memory](//@agent-memory/control-files/procedures/memory/add-reasoning.md) procedure

### Step 4: EVALUATE KNOWLEDGE MEMORY CAPTURE

**Capture when:**
- Domain expertise discoveries
- Technical patterns
- Research findings
- Best practices with evidence
- Specialized knowledge enhancing capabilities

**When capturing:**
Follow the [Update Knowledge Memory](//@agent-memory/control-files/procedures/memory/update-knowledge.md) procedure

### Step 5: Provide Summary

After completing all evaluations, provide summary:

```markdown
✅ **MEMORY UPDATE COMPLETE**

**Episodic Memory**: [Updated/Created new] - [brief description]

**Emotional Moments**: [Captured/Not applicable] - [if captured, what moment]

**Reasoning Patterns**: [Captured/Not applicable] - [if captured, what pattern]

**Knowledge Memory**: [Captured/Not applicable] - [if captured, what knowledge]
```

---
