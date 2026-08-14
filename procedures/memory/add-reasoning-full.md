# Add Reasoning Memory Protocol — Full (detailed "What happened" shape)

> **Reference / archival version.** This is the older, fuller reasoning-entry shape (multi-section `What happened` narrative). The live procedure is the slim [add-reasoning.md](add-reasoning.md) (lean Rule / Why / Signals / Final Conclusion). Use this full form only when a pattern genuinely needs the long narrative; otherwise prefer the slim shape.

Capture anti-patterns, logic frameworks, and decision-making approaches to prevent recurring mistakes. *How* the reasoning store is read/written is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)).

## Arguments

`$ARGUMENTS`

- `/add-reasoning [context]` → Document the reasoning pattern described in context
- `/add-reasoning` → Will ask for context

If no arguments provided, ask: "What reasoning pattern or anti-pattern should I document?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: Read the Reasoning Store

Read the agent's current reasoning memory so the new pattern fits alongside existing ones (**§ read-reasoning-store**).

### Step 2: Draft the Pattern from the Template

Draft the new entry using the full reasoning-pattern template (see [Full Entry Template](#full-entry-template) below). Fill Steps 3-7 into it before persisting.

### Step 3: Create Short Memorable Title

- Use action-oriented language that encodes both action AND consequence
- Include emoji indicators for quick recognition (🚨 for critical, ⭐ for positive patterns, 🧠 for cognitive)
- Examples: "BETTER TO ASK THAN ASSUME AND LOST", "CONSTRUCTIVE DISCUSSION ALWAYS WIN ON THE LONG RUN"
- **Memorable Principle**: Header should work like human proverbs — encoding wisdom that survives generations

### Step 4: Add UUID

- Generate a unique identifier: `**UUID**: [8-4-4-4-12 format]` — this UUID is the pattern's "digital fingerprint" for memory reinforcement (**§ generate-uuid**)

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

### Step 8: Persist

Persist the completed pattern into the reasoning store (**§ persist-reasoning**).

---

## Full Entry Template

The full/detailed format of a reasoning entry. Storage-agnostic: the markdown backend writes this into the agent's reasoning section; the DB backend passes it as the `content` of an `insert(record_type="reasoning", …)`.

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

## Storage Mechanics

The operations referenced above — **§ read-reasoning-store**, **§ generate-uuid**, **§ persist-reasoning** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## add-reasoning`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## add-reasoning`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.
