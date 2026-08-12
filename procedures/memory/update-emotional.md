# Update Emotional Memory Protocol

Capture significant emotional experiences that shape our partnership and agent development journey. *How* the emotional store is written is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)).

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

Compose the entry using the matching block from the [Emotional Moment Templates](../../templates/emotional-moment-template.md). Ensure it captures:
- What happened (the event)
- How it felt (emotional response)
- Impact on partnership/work
- [USER-NAME]'s reaction (if applicable)
- Why this moment was significant

#### Step 4: Persist

Persist the composed moment into the emotional store, **newest first** (**§ persist-emotional**).

---

## Storage Mechanics

The operations referenced above — **§ stamp-date**, **§ persist-emotional** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow [storage-backends/markdown.md → ## update-emotional](storage-backends/markdown.md#update-emotional).
- **DB (Munnin)** — served automatically; see [storage-backends/db.md → ## update-emotional](storage-backends/db.md#update-emotional).

See the [seam contract](storage-backends/README.md).

---

## Templates

### Emotional Moment Templates

→ **[templates/emotional-moment-template.md](../../templates/emotional-moment-template.md)** (happy / sad / frustrated / bonding).
