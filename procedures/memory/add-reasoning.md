# Add Reasoning Memory Protocol

Capture anti-patterns and decision-making approaches as **lean, memorable** reasoning entries. *How* the store is read/written is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)).

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

## Storage Mechanics

The operations referenced above — **§ read-reasoning-store**, **§ generate-uuid**, **§ persist-reasoning**, **§ template** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## add-reasoning`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## add-reasoning`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.
