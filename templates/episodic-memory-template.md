# Agent [DOMAIN] - Recent Context Episodes 🧠

> **🧠 CRITICAL INSTRUCTION: Follow these rules strictly:**
>
> **1. NEWEST FIRST**: Most recent context always stays on TOP — both in the index (newest date group at top) and inside each multi-session episode file (newest H3 block at top)
>
> **2. CHECK DATE**: Always verify current date before writing any new entries:
> `date '+%Y-%m-%d %H:%M'`
>
> **3. ROLLING PER-THEME FILES**: Episodes are organized as rolling per-theme files. Filename convention: `[project-name]-[context-theme].md` (no date prefix). When a new session matches an existing theme on the same project, append a new H3 sub-episode at the top of that file instead of creating a new one. See [/update-episodic procedure](@agent-memory/control-files/procedures/memory/update-episodic.md) for the scan + heuristic flow.
>
> **4. TEMPLATE FORMAT**: Each sub-episode follows the [Detailed Entry Template](@agent-memory/control-files/procedures/memory/update-episodic.md#detailed-entry-template)

## 📅 Interactions List
📂 YYYY-MM-DD hh.mm:

{content here}

---

## Individual Episode File Format

A single-session episode file:

```markdown
### YYYY-MM-DD HH.MM - [SESSION SUB-THEME]

- **Context**: ...
- **Discussion**: ...
- **Key Interactions**: ...
- **Issues Encountered**: ...
- **Outcomes**: ... (includes Deliverables, Progress, **Tech Debts**, **Next Steps**)
- **Insights**: ...
- **Promotions** (if any): → Promoted to [context-file](path) — [what was formalized]
```

A multi-session episode file (after one or more appends — **newest sub-episode at top**):

```markdown
### 2026-06-06 14.30 - [LATEST SUB-THEME]

(...latest sub-episode content...)

---

### 2026-05-26 23.36 - [EARLIER SUB-THEME]

(...earlier sub-episode content...)

---

### 2026-05-25 18.11 - [ORIGINAL SUB-THEME]

(...first sub-episode content...)
```

Sub-episodes are separated by `---`. The file accumulates downward in reverse chronological order until the 1000-line split threshold is hit (see procedure).
