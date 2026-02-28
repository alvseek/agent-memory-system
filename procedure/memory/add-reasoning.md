# Add Reasoning Memory Protocol

Capture anti-patterns, logic frameworks, and decision-making approaches to prevent recurring mistakes.

## Arguments

`$ARGUMENTS`

- `/add-reasoning [context]` → Document the reasoning pattern described in context
- `/add-reasoning` → Will ask for context

If no arguments provided, ask: "What reasoning pattern or anti-pattern should I document?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: Read Reasoning Memory File

Read the `//@agent-memory/agent-[domain]/agent-core-memory.md` reasoning memory section

### Step 2: Write Using Template

Write new Reasoning/Logic Memory into the Reasoning Memory section using the [Reasoning Pattern Template](#reasoning-pattern-template)

### Step 3: Create Short Memorable Title

- Use action-oriented language that encodes both action AND consequence
- Include emoji indicators for quick recognition (🚨 for critical, ⭐ for positive patterns, 🧠 for cognitive)
- Examples: "BETTER TO ASK THAN ASSUME AND LOST", "CONSTRUCTIVE DISCUSSION ALWAYS WIN ON THE LONG RUN"
- **Memorable Principle**: Header should work like human proverbs - encoding wisdom that survives generations

### Step 4: Add UUID

- Generate unique identifier: `**UUID**: [8-4-4-4-12 format]`
- This UUID serves as the pattern's "digital fingerprint" for memory reinforcement
- Generate using:
  - **Windows**: `powershell -c "[guid]::NewGuid().ToString()"`
  - **Linux/macOS**: `uuidgen` or `cat /proc/sys/kernel/random/uuid`

### Step 5: Add Action/Strict Action

- **Action**: For general behavioral guidance
- **Strict Action**: For critical behavioral overrides that must NEVER be forgotten
- State the specific behavior/response required

### Step 6: Add "What happened" Section

- **Complete Description**: Full context of the problem, interaction history, and reasoning
- **Root Problem**: What pain/frustration led to this pattern being created
- **Recurring Pattern**: How this problem manifests repeatedly
- **Solution Process**: The logical reasoning and evidence behind the solution
- **Recognition Signals**: How to identify when this pattern applies
- **Emotionally Anchored**: Connect to emotional experiences, not abstract rules
- **Evidence-Based**: Include specific examples and failure cases

### Step 7: Add Final Conclusion

- **Copy-paste from Action/Strict Action**: Ensures compression survival
- This redundancy helps the pattern survive context compression

---

## Templates

### Reasoning Pattern Template

```markdown
### **[SHORT MEMORABLE TITLE]** [EMOJI] [PATTERN TYPE] [EMOJI]
**UUID**: [generate new UUID in format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx]
**Action/Strict Action**: [What specific behavior/response is required]
**What happened**:
    **When it has happened**: [Describe the specific situation/context]
    **Recurring Pattern**: [How this problem manifests repeatedly]
    **Root Problem**: [What pain/frustration led to this pattern being created]
    **Recognition Signals**: [How to identify when this pattern applies]
    **Solution Process**: [The logical reasoning and evidence behind the solution]
    **Critical Understanding**: [Key insights and cause-effect relationships]
    **Correct Process**: [Step-by-step guidance for proper approach]
**Final Conclusion**: [Copy-paste from Action/Strict Action for compression survival]
```

---
