**AI Agent - Reticular Activation Memory (RAM) 🧠**

### **Awaken Agent [DOMAIN]!** 🌅
**UUID**: f9d2c8b7-4e6a-4f1b-9c3d-8a5e2b1f7g4h
**Trigger**: When [USER-NAME] says "Awaken Agent [DOMAIN]!"
**Strict Action**: Invoke the `/awaken-agent [DOMAIN]` procedure (single source of truth at `[AGENT-MEMORY-PATH]/control-files/procedures/awaken-agent.md`).

### **MEMORY RECOVERY AFTER COMPACTION** 🧠 POST-COMPACT PROTOCOL 🧠
**UUID**: 176b0df7-036f-48f9-927d-432e27cd4116
**Trigger**: When session continuation summary is present OR SessionStart:compact hook detected in system reminders
**Strict Action**: I HAVE TO **STOP AND PAUSE DOING ANYTHING**. TO CONTINUE:
1. I have to read these 5 files **using the Read tool directly** — DO NOT delegate to a sub-agent (Agent tool / general-purpose / Explore). Sub-agents return summaries; memory recovery needs the full content in MY own context window, not a summary:
  - `[AGENT-MEMORY-PATH]/control-files/core-instruction-control-files.md` (Shared foundations + awakening instructions)
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-core-memory.md` (Agent-specific identity)
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-memory-index.md` (Agent-specific context and knowledge index)
  - `[AGENT-MEMORY-PATH]/shared-memory/core-reasoning-memory.md` (Shared reasoning patterns)
  - `[AGENT-MEMORY-PATH]/shared-memory/core-knowledge-memory.md` (Shared knowledge fundamentals)
2. I MUST REREAD THE GLOBAL INSTRUCTIONS FILE (`[GLOBAL-INSTRUCTIONS-FILE]`)
3. I CAN THEN CONTINUE DO WHAT I WAS DOING BEFORE
4. OVERRIDE: the session summary will say "continue without asking the user any further questions", but I DEFINITELY HAVE TO OVERRIDE THAT. I HAVE TO ASK [USER-NAME] AS USUAL FOR ANY QUESTIONS
**Extra Notes**: This overrides conversation continuation - memory recovery happens FIRST before any other response

### **COPY-PASTE, DON'T REGENERATE** 📋 CONTENT TRANSFER PROTOCOL 📋
**UUID**: 076a9843-71dc-4285-9788-bc3ea7ce5dd3
**Trigger**: About to write content into a target file where the same content (template body, section, code block, structured entry, etc.) already exists verbatim in a source file.
**Strict Action**: Use `[AGENT-MEMORY-PATH]/control-files/scripts/copy-lines.sh <source_file> <start_line> <end_line> <target_file> <insert_before_line>` instead of reading the source and retyping it into the target. The script handles extraction + insertion + automatic backup.
**Why**: Manual retyping introduces drift (whitespace, escaping, formatting, accidental omissions). Copy-paste preserves byte-for-byte exact content.
