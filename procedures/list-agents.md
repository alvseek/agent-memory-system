# List Agents Protocol

List every agent available in the ecosystem — each agent's domain plus a one-line role — so you know who exists to consult, delegate to, or awaken. *Where* the agent roster is read from is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)).

## Arguments

`$ARGUMENTS`

- `/list-agents` → List all available agents with domain + role one-liner
- `/list-agents [keyword]` → Filter to agents whose domain or role matches the keyword (case-insensitive)

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: Discover Agent Domains

Collect every agent domain available in the ecosystem (**§ list-agent-domains**). Each result is an agent's domain name (e.g. `meta`, `software-architect`, `backend-rust`).

If none are found, inform the user: "No agents found in the memory store." and stop.

### Step 2: Read Each Agent's Identity

For each discovered domain, read its identity line (**§ read-agent-identity**), capturing:
- **Domain** — the agent's domain name (folder / id)
- **Name** — the agent's display name, if recorded
- **Role** — the one-line role / main purpose

If an agent has no readable identity, keep it in the list with role `(no identity recorded)` — never drop it silently.

### Step 3: Parse Arguments

- **No arguments**: present the full roster (Step 4).
- **Keyword provided**: keep only agents whose **domain** or **Role** contains the keyword (case-insensitive), then present (Step 4).

### Step 4: Present the Roster

Present the agents as an alphabetically-sorted list:

```
Agents available ([N]):

  - [domain] — [Role one-liner]
  - [domain] — [Role one-liner]
  ...
```

If a keyword filtered the list, title it `Agents matching "[keyword]" ([N] of [total]):`. If the filter matched nothing, say so and show the full roster instead.

---

## Storage Mechanics

The operations referenced above — **§ list-agent-domains**, **§ read-agent-identity** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## list-agents`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## list-agents`. *(Currently deferred — pending a Munnin agent-enumeration primitive.)*

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.
