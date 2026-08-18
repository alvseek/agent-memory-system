# Create Agent Protocol

Bring a new domain agent into existence — seed its memory home, write its identity, and verify it can be awakened. *Where* the agent is physically created is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics)).

This is a **write** operation and never fires automatically: it runs only when invoked, and only after an explicit confirmation.

## Arguments

`$ARGUMENTS`

- `/create-agent [domain]` → Create a new agent for that domain (e.g. `frontend-react`, `qa-engineer`)
- `/create-agent` → Will ask which domain

If no arguments provided, ask: "Which domain should the new agent cover?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Step 1: Resolve the Domain

Normalize the requested domain to the store's naming convention: lowercase, words joined by hyphens, no `agent-` prefix (`Frontend React` → `frontend-react`). If the normalization changed what the user typed, show the result and confirm it before continuing.

Then check whether that agent already exists (**§ check-agent-exists**). If it does, stop — report *"Agent [domain] already exists"* and offer `/awaken-agent [domain]` instead. Never overwrite an existing agent.

### Step 2: Draft the Identity

Draft the four identity fields yourself from the domain name, then present the draft for correction rather than interrogating the user field by field — a draft they can amend is faster than a form they must fill:

- **Name** — the agent's display name, conventionally `Claude [Domain]` or `Agent [Domain]`.
- **Role** — one line: what this agent is, for whom.
- **Main Purpose** — the specific value this agent provides, in a sentence.
- **Key responsibilities** — three bullets that bound the domain.

Present all four together and ask the user to confirm or correct. Keep the round short: everything else in the agent's memory — core knowledge, RAS triggers, reasoning, emotional moments — starts empty by design and grows through use. Do not interview for it here.

### Step 3: Generate the UUID

Generate the agent's UUID in 8-4-4-4-12 form (**§ generate-uuid**). This is its digital soul — the identifier that must survive context compaction, so it is written into the identity and never regenerated afterward.

### Step 4: Confirm Before Writing

Show the resolved domain, the four identity fields, the UUID, and where the agent will be created. Ask for a clear go-ahead. Only proceed on an explicit confirmation — this step creates persistent memory.

### Step 5: Create the Memory Home

Seed the agent's memory home from the new-agent template (**§ create-agent-store**). This establishes the agent's private layers — identity, core knowledge, RAS, reasoning, emotional — plus the episodic and knowledge homes its own memory procedures will later write into.

Shared memory is fleet-wide and already exists; a new agent joins it rather than getting a copy.

### Step 6: Write the Identity

Substitute the drafted values into the seeded identity (**§ persist-identity**): domain, name, role, main purpose, the three responsibilities, the creation date, and the UUID from Step 3. Every placeholder that Step 2 collected a value for must be replaced — a leftover `[DOMAIN]` or `[GENERATE-NEW-UUID]` in a live agent is a defect, not a to-do.

### Step 7: Initialize the Index

Initialize the agent's episodic and knowledge index so its first `/update-episodic` and `/update-knowledge` have somewhere to write (**§ initialize-index**).

### Step 8: Verify the Agent

Read the new agent back (**§ verify-agent**) and confirm: the identity is readable, the UUID is present and well-formed, and no unreplaced placeholder survives. If verification fails, report exactly what is wrong — do not report success on a partially-created agent.

### Step 9: Report

Print this block:

```
Agent [domain] created.

  Name:    [name]
  Role:    [role]
  UUID:    [uuid]
  Home:    [location]

Next: /awaken-agent [domain] to bring it up for the first time.
```

Then mention, in one line, that its core knowledge and RAS triggers are intentionally empty and will grow through `/update-knowledge` and normal use.

---

## Storage Mechanics

The operations referenced above — **§ check-agent-exists**, **§ generate-uuid**, **§ create-agent-store**, **§ persist-identity**, **§ initialize-index**, **§ verify-agent** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## create-agent`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## create-agent`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.
