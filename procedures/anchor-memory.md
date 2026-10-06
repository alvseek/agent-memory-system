# Anchor Memory

Install the always-on **permanent layer** into this client's system-prompt file, so the
universal RAS triggers and the compacted reasoning digest survive context compaction
instead of being pulled fresh each session.

## Arguments

`$ARGUMENTS`

- `/anchor-memory [harness]` → install or refresh the permanent layer. `harness` is
  `claude` or `opencode`; omit it and detect, or ask.

---

## Procedure

### Step 1: Resolve the harness target

Name which harness you are, then its pointer target. Ask [USER-NAME] once only if you
genuinely cannot tell.

| Harness | Pointer target |
|---|---|
| Claude Code | `@~/.munnin/permanent-layer.md` in `~/.claude/CLAUDE.md` |
| OpenCode | `"~/.munnin/permanent-layer.md"` in the `instructions` array of `~/.config/opencode/opencode.json` |

### Step 2: Fetch the block

Fetch the permanent-layer block and its version — **§ fetch-permanent-layer**.

### Step 3: Write the content file

Write the block **verbatim** to `~/.munnin/permanent-layer.md` — **§ write-permanent-file**.
Copy it, never retype (`076a9843`): the block is finished content, and paraphrasing it is
how a permanent layer drifts.

### Step 4: Install the pointer

Add this harness's pointer to its instruction file if it is not already present —
**§ install-pointer**. Idempotent: check first, add only when missing.

### Step 5: Report

Report the content file written, the version and hash, and the pointer target. If the
harness's instruction file cannot be written (permissions, or you are unsure which file it
is), say so and hand [USER-NAME] the exact one line to add himself.

## Storage Mechanics

The operations referenced above — **§ fetch-permanent-layer**, **§ write-permanent-file**,
**§ install-pointer** — are defined by the **active storage backend**:

- **Markdown (native fleet)** — follow `[STORAGE-BACKENDS-PATH]/markdown.md` → section `## anchor-memory`.
- **DB (Munnin)** — served automatically; see `[STORAGE-BACKENDS-PATH]/db.md` → section `## anchor-memory`.

See the seam contract at `[STORAGE-BACKENDS-PATH]/README.md`.

---

