# Add Reasoning Memory Protocol

Capture anti-patterns and decision-making approaches as **lean, memorable** reasoning entries. *How* the store is read/written is delegated to the active **storage backend**.

## Arguments

`$ARGUMENTS`

- `/add-reasoning [context]` → Document the reasoning pattern described in context
- `/add-reasoning` → Will ask for context

If no arguments provided, ask: "What reasoning pattern or anti-pattern should I document?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below to prevent context loss and ensure complete execution*

### Step 1: Read the Reasoning Store

Read the agent's current reasoning memory so the new pattern fits alongside the existing ones and doesn't duplicate one (**§ read-reasoning-store**).

### Step 2: Draft from the Template

Read the reasoning-pattern template (**§ template**) and draft the entry using its fixed structure.

### Step 3: Check the Entry

Check every required field against the template. For a new entry, generate its UUID (**§ generate-uuid**); for a rewrite, preserve the existing UUID. Keep the instructions, anchor, and example distinct, and check that the Final Conclusion stands on its own.

### Step 4: Persist

Persist the completed pattern into the reasoning store (**§ persist-reasoning**).

---

### § read-reasoning-store

Read the `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` reasoning memory section (`# DOMAIN REASONING MEMORY`).

### § generate-uuid

Generate a unique identifier:
- **Windows**: `powershell -c "[guid]::NewGuid().ToString()"`
- **Linux/macOS**: `uuidgen` or `cat /proc/sys/kernel/random/uuid`

### § persist-reasoning

Write the completed pattern into the `# DOMAIN REASONING MEMORY` section of `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md`.

### § template

The reasoning-pattern block format → read `[AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/reasoning-pattern-template.md`.

---
