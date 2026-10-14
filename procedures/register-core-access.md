# Register Core Access

Declare how this client reaches the memory core — `[CORE-ACCESS]` and `[CORE-MCP-URL]` — in
this client's system-prompt file. A client that reaches the core as served procedures has no
local checkout and no installed commands, so nothing else can write those two lines for it,
and hand-editing is the only alternative this replaces.

## Arguments

`$ARGUMENTS`

- `/register-core-access [harness]` → write or refresh the two declarations. `harness` is
  `claude` or `opencode`; omit it and detect, or ask.

---

## Procedure

### Step 1: Resolve the harness target

Name which harness you are, then its instructions file. Ask [USER-NAME] once only if you
genuinely cannot tell.

| Harness | Instructions file |
|---|---|
| Claude Code | `~/.claude/CLAUDE.md` |
| OpenCode | `~/.config/opencode/AGENTS.md` |

### Step 2: Read the declaration pair

Read what this layer declares itself to be — **§ read-access-pair**. The access value is not
a preference to be chosen: a procedure that is running has already reached the core, so the
form it names is the form in force. Never ask [USER-NAME] for it.

### Step 3: Write the two lines

Write the pair into the instructions file — **§ write-access-lines**. Rewrite when the lines
are present, append when they are absent, and never touch a sibling layer's declaration.

### Step 4: Report

Report the harness, the file written, and the two values. If the file cannot be written
(permissions, or you are unsure which file it is), say so and hand [USER-NAME] the exact two
lines to add himself.

## Storage Mechanics

The operations referenced above — **§ read-access-pair**, **§ write-access-lines** — are
defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## register-core-access`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## register-core-access`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.

---
