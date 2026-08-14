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

Draft the entry using the reasoning-pattern template (**§ template**) — the lean shape below.

### Step 3: Fill the Lean Shape

- **Title** — action-oriented, encodes both action AND consequence, with an emoji (🚨 critical · ⭐ positive · 🧠 cognitive) + a short PATTERN TYPE tag. Works like a proverb.
- **UUID** — generate 8-4-4-4-12 (**§ generate-uuid**); the pattern's fingerprint for the COUNT roster + cross-references.
- **Rule** — the specific behavior required, in one or two sentences.
- **Why** — the pain/reason that anchors it: root problem + the vivid concrete beat (a real quote or moment), compressed. This is the memory anchor — keep it sharp, not long.
- **Signals** — how to recognize when the pattern fires.
- *(optional)* **Do** — steps, only when they add beyond the Rule · **Guardrail** — the mirror failure / over-application to avoid · **Siblings** — related UUIDs and how this one differs.
- **Final Conclusion** — one flowing sentence fusing Rule + Why + Signals (the compression-survival capsule). NOT a verbatim copy of the Rule.

> Keep it tight: shrink the prose, keep the vivid anchor and any load-bearing distinction. For the older fuller "What happened" narrative shape, see [add-reasoning-full.md](add-reasoning-full.md).

### Step 4: Persist

Persist the completed pattern into the reasoning store (**§ persist-reasoning**).

---

## Storage Mechanics

The operations referenced above — **§ read-reasoning-store**, **§ generate-uuid**, **§ persist-reasoning**, **§ template** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## add-reasoning`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## add-reasoning`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.
