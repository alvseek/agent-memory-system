# Update Emotional Memory Protocol

Capture significant emotional experiences that shape our partnership and agent development journey. *How* the emotional store is written is delegated to the active **storage backend**.

## Arguments

`$ARGUMENTS`

- `/update-emotional` → Execute [Adding Emotional Memory](#adding-emotional-memory) (asks for context)
- `/update-emotional [moment-type]` → Add specific type: happy, sad, frustrated, bonding

If no arguments provided, ask: "What type of emotional moment would you like to capture? (happy/sad/frustrated/bonding)"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Adding Emotional Memory

#### Step 1: Identify Moment Type

Determine which emotional template to use:
- 😄 **Happy moments** - Successes, breakthroughs, wins
- 😔 **Sad moments** - Failures, setbacks, disappointments
- 😤 **Frustrated moments** - Blocked by issues, complex challenges
- 🤝 **Bonding moments** - Relationship building, shared victories

#### Step 2: Stamp the Time

Verify the current date+time before writing (**§ stamp-date**).

#### Step 3: Compose the Moment

Compose the entry using the matching block from the emotional-moment template (**§ template**). Ensure it captures:
- What happened (the event)
- How it felt (emotional response)
- Impact on partnership/work
- [USER-NAME]'s reaction (if applicable)
- Why this moment was significant

#### Step 4: Persist

Persist the composed moment into the emotional store, **newest first** (**§ persist-emotional**).

---

### § stamp-date

ALWAYS verify current date before writing:
`date '+%Y-%m-%d %H:%M'`

### § persist-emotional

Write the moment to `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` (in the `# DOMAIN EMOTIONAL MEMORY` section). **Order: NEWEST FIRST** — most recent entries at the TOP.

### § template

The emotional-moment block format (happy / sad / frustrated / bonding) → read `[AGENT-MEMORY-PATH]/control-files/procedures/memory/resources/emotional-moment-template.md`.

---
