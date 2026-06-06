# Update Memory Protocol

Comprehensive memory update orchestrator. Four phases, seven steps:

- **Phase 1 — Promote durable artifacts**: three parallel gated auto-evals (project context, reasoning, knowledge). Did this session produce rules / patterns / facts that should persist beyond the session?
- **Phase 2 — Capture the session**: collect promotion markers from Phase 1 + any mid-session writes, then write the episodic journal entry.
- **Phase 3 — Capture the feeling**: retrospective emotional 5-criteria gate. Was this session significant enough to anchor as a permanent feeling-moment?
- **Phase 4 — Report**.

`/update-episodic` only writes the episodic layer. `/update-memory` is the command for "end-of-session, do everything." This is what `/wrap-up` invokes.

## Arguments

`$ARGUMENTS`

- `/update-memory` → Comprehensive update (default)
- `/update-memory new` → Force-create a new episodic file, then run cross-layer orchestration

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

---

## Phase 1 — Promote Durable Artifacts

> Three parallel gated auto-evals. Each step asks: *"did this session produce X worth persisting beyond the session?"* Each gate is a concrete checklist that the agent can answer yes/no honestly — no vague "is this important?" judgments. If yes → call the corresponding write protocol. If no → skip silently. All three gates run independently; order doesn't matter within this phase.

### Step 1: Project Context Auto-Eval (Gated Conditional Write)

Evaluate whether this session produced **project-specific context** worth preserving for future sessions. Concrete checklist — answer each yes/no honestly:

- Were there project-specific conventions, setup steps, deployment procedures, or environment details discussed?
- Were there workarounds, configurations, or technical decisions specific to the current project?
- Were there new access credentials, URLs, API endpoints, or infrastructure details shared?

**If YES to any** → execute the [Update Project Context Protocol](//@agent-memory/control-files/procedures/memory/update-project-context.md) with the relevant context. Auto-detect the theme and the shared-vs-private scope (per the procedure's own heuristic); no user prompt needed.

**If NO to all** → skip silently.

> **Why the gate works**: checklist items are concrete artifacts (touched conventions / wrote a workaround / shared a URL). No vague judgment required.

### Step 2: Reasoning Pattern Auto-Eval (Gated Conditional Write)

Evaluate whether this session uncovered a **reasoning pattern, anti-pattern, or rule-of-thumb** that should apply across future sessions. Concrete checklist — answer each yes/no honestly:

- Did [USER-NAME] explicitly call out a recurring failure mode or anti-pattern this session? (signals: *"we got burned by this before"*, *"don't do X again"*, *"we keep making this mistake"*, *"remember this anti-pattern"*)
- Did [USER-NAME] explicitly validate a non-obvious approach as a pattern worth repeating? (signals: *"always do it this way"*, *"this is the right pattern"*, *"remember this approach"*, *"let's encode this"*)
- Did a new decision-making framework or rule-of-thumb emerge from a back-and-forth with [USER-NAME] that we both agreed should govern future similar situations?

**If YES to any** → execute the [Add Reasoning Protocol](//@agent-memory/control-files/procedures/memory/add-reasoning.md) with the relevant pattern.

**If NO to all** → skip silently.

> **Why explicit user signal is required**: agents tend to over-rate minor corrections as "anti-patterns." Requiring [USER-NAME]'s explicit identification (same evidence-grounding as Phase 3's criterion 5) prevents reasoning-memory dilution. If [USER-NAME] didn't name it as a pattern this session, it's not yet a pattern — it's a one-off.

### Step 3: Knowledge Memory Auto-Eval (Gated Conditional Write)

Evaluate whether this session produced **durable technical knowledge** worth preserving as reference material. Concrete checklist — answer each yes/no honestly:

- Did the session produce documented research with sources/citations/evidence that the agent treated as reference material throughout (not just one-time lookup)?
- Did [USER-NAME] explicitly identify a finding worth preserving for future agents? (signals: *"let's document this"*, *"this is worth knowing"*, *"future agents should know X"*, *"write this down"*)
- Did a non-obvious technical mechanism, edge case, or framework internal get uncovered that would be costly to re-discover later?

**If YES to any** → execute the [Update Knowledge Protocol](//@agent-memory/control-files/procedures/memory/update-knowledge.md) with the relevant entry.

**If NO to all** → skip silently.

> **Why the gate is tight**: knowledge memory is reference material — every entry should pay rent in future sessions. The first criterion requires evidence; the second requires [USER-NAME]'s explicit signal; the third requires the "costly to re-discover" framing. Task-specific learnings that won't apply elsewhere don't qualify.

---

## Phase 2 — Capture the Session

> Phase 1 wrote (or skipped) cross-layer artifacts. Now write the session itself as an episodic journal entry, with traceability back to whatever Phase 1 wrote. Two steps: collect the markers, then write the entry.

### Step 4: Pre-Scan Cross-Layer Promotion Markers

Identify cross-layer files written during this session. This includes any files written in Phase 1 (Steps 1-3 above) AND any files written proactively earlier by the agent via direct mid-session calls to `/update-project-context`, `/add-reasoning`, or `/update-knowledge`. Build a single promotion-markers list covering both sources.

**Common targets to scan for**:

| Layer | Path |
|-------|------|
| Project context (shared) | `shared-memory/[project]/context/*.md` |
| Project context (private) | `knowledge-base/[project]/*.md` |
| Knowledge (general) | `knowledge-base/[topic].md` |
| Knowledge (core) | `knowledge-base/core-domain-knowledge.md` |
| Reasoning (shared) | `shared-memory/core-reasoning-memory.md` |
| Reasoning (per-agent) | `agent-core-memory.md` → `# DOMAIN REASONING MEMORY` section |

For each touched file, build a marker line:
```
→ Promoted to [layer-file](path) — [brief: what was formalized]
```

If no cross-layer impact identified → proceed to Step 5 with empty promotion list.

> **Why pre-scan goes here (after Phase 1, before episodic)**: putting it after Phase 1 means it catches everything Phase 1 wrote. Putting it before episodic means the markers populate the episodic entry's Promotions field in a single write — no need to come back and edit the entry.

### Step 5: Run Episodic Capture (with markers populated)

1. Check arguments:
   - If `$ARGUMENTS` contains "new" → invoke `/update-episodic new`
   - Otherwise → invoke `/update-episodic` (default flow)

2. Follow the [Update Episodic Memory Protocol](//@agent-memory/control-files/procedures/memory/update-episodic.md) end-to-end.

3. When writing the sub-episode entry, populate the `**Promotions**` field at the end of the block with the promotion markers built in Step 4. If no promotions, leave the field absent (the template treats it as optional).

> **Why episodic is the anchor**: episodic is the journal of *what happened this session*. The promotion markers tie that journal entry to the durable artifacts Phase 1 produced. Without episodic, the artifacts have no narrative; without the markers, the narrative has no traceability to the artifacts. Together they form the session's complete record.

---

## Phase 3 — Capture the Feeling

> Phase 2 captured *what happened*. Phase 3 retrospectively asks: *was what happened significant enough to anchor as a permanent feeling-moment that survives archive cycles and shows up at every awakening?* Placed last as a workflow choice — reflection naturally comes after action. (Technically emotional could evaluate without Phase 2 written; placing it here keeps the flow act → record → reflect.)

### Step 6: Emotional Memory Auto-Capture (5-Criteria Gate)

Apply the 5 criteria to this session. **All 5 must pass** to auto-capture emotional memory:

1. **Previous state was primitive / basic / wrong, OR there was no previous system** (entirely new system created from scratch)
2. **New state is robust and proper** — well-designed, durable, not a stopgap
3. **High-value addition** — meaningful capability or insight (not just "task completed")
4. **System-level scope** — architecture, protocol, framework component, or new system. **NOT** bug fix, single function, config tweak, or routine completion
5. **[USER-NAME] expressed celebration or strong recognition** during this session. Concrete signals in the conversation transcript:
   - Affirmation with positive emotion: *"nice", "great", "love it", "amazing", "perfect", "exactly"*
   - Celebration: *"yippieee", "let's goooo", emojis like 💖🎉🚀*
   - Explicit recognition: *"this is big", "this is good", "yes that's it"*
   - Sustained positive engagement escalating across the session

**Phrasing test** for criteria 1+2: Can you describe the change as *"previously X was [primitive way], now X is [robust way]"* OR *"X did not exist, now X is a working system"*? If yes, criteria 1+2 likely met.

**Test against routine work (anti-examples)**:
- "Fixed typo in README" → no system upgrade → ✗
- "Added single endpoint" → single function → ✗
- "Created agent from existing template" → instantiation, not system upgrade → ✗
- "Completed scheduled task" → routine completion → ✗

**Test against system work (qualifying examples)**:
- "Redesigned core procedure architecture" → system-level → ✓
- "Built new memory layer from scratch" → entirely new system → ✓
- "Designed novel wizard protocol" → new system → ✓

**If all 5 pass** → execute the [Update Emotional Protocol](//@agent-memory/control-files/procedures/memory/update-emotional.md), passing the session context (previous→new framing or new-system framing, [USER-NAME]'s celebration quote verbatim, system scope, optional identity claim). The protocol owns the actual entry format — pass material, not structure.

**If any criterion fails** → skip emotional capture silently. No prompt, no entry.

> **Why emotional is separate from Phase 1**: Phase 1's gates capture *artifacts the session produced*. Emotional captures *how the session as a whole felt and what identity it claims*. Different cognitive purpose — promotion vs reflection. And reflection requires the session to be wrapped (episodic written) before it can be evaluated.

---

## Phase 4 — Report

### Step 7: Summary

Report what was done across all phases:

```markdown
✅ **MEMORY UPDATE COMPLETE**

Phase 1 — Promoted artifacts:
- **Project context**: [updated/created / skipped] — [file name if written]
- **Reasoning pattern**: [added / skipped] — [pattern name if added]
- **Knowledge**: [added / skipped] — [entry name if added]

Phase 2 — Session captured:
- **Episodic**: [appended to / created] [filename] — [brief theme]
- **Promotions** (cross-layer markers added to episodic): [N markers / none] — [list if N>0]

Phase 3 — Feeling captured:
- **Emotional**: [captured / skipped] — [if captured: theme + which criterion made the cut clearest]
```

---

## Notes

- **Conservative bias on all four gates**: when borderline, default to SKIP. False negatives (missed capture) are recoverable via direct command call; false positives (diluted memory) are corrosive and hard to undo.
- **Phase 1 gates are safety-nets, not replacements for proactive mid-session writes**. Agents should still call `/update-project-context`, `/add-reasoning`, `/update-knowledge` proactively mid-session when a pattern is clearly visible at the moment of discovery. Step 4 catches both sources (Phase 1 writes + mid-session writes) into a unified marker list.
- **This protocol is the session-end orchestrator** — it complements, does not replace, the individual layer-write commands.
