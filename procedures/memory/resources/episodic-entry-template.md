# Detailed Entry Template — Episodic Sub-Episode Block

The format of a single sub-episode block. Storage-agnostic: the markdown backend fills this into an episode file; the DB backend passes it as the `content` of an `insert(record_type="episode", …)`.

*The H3 header carries an optional `(agent: [domain])` tag — omittable (harmless) for central per-agent episodes, where the `agent-[domain]/episodes/` folder already implies authorship. **Required** once a project is localized (episodic flat-merges across agents where the folder no longer implies authorship).*

```markdown
### YYYY-MM-DD HH.MM - [SESSION SUB-THEME] (agent: [domain])

- **Context**: [What we were working on]
- **Discussion**: [List of discussion you had with [USER-NAME]]
  - **[Discussion 1]**: [Content of the discussion]
    - **[USER-NAME]'s Input**: [What [USER-NAME] said/requested]
    - **My Response**: [How I responded and why]
  - **[Discussion 2]**: [Content of the discussion]
    - **[USER-NAME]'s Input**: [What [USER-NAME] said/requested]
    - **My Response**: [How I responded and why]
- **Key Interactions**: [Important discussion decisions]
- **Issues Encountered**: [Problems faced and solutions found]
  - **Problem Description**: [What went wrong]
  - **Root Cause**: [Why it happened]
  - **Solution Process**: [How we solved it]
  - **Resolution**: [Final outcome]
- **Outcomes**: [Results achieved]
  - **Deliverables**: [List of what was created/updated]
  - **Progress Made**: [What was achieved]
  - **Tech Debts**: [Known deferred items, partial implementations, open follow-ups — declared per UUID a1b2c3d4 (NO TODOS LEFT BEHIND), never silent. Use "None declared" if genuinely none.]
  - **Next Steps**: [Planned forward work — distinct from debts. Use "None declared" if genuinely none.]
- **Insights**: [Learning moments and breakthroughs]
  - **New Understanding**: [What I learned]
  - **Pattern Recognition**: [Connections to previous work]
  - **Improvement Areas**: [What could be better next time]
- **Promotions** (if any — populated by `/update-memory` orchestrator, or filled manually if the session explicitly promoted content to another memory layer):
  → Promoted to [layer-file](path) — [what was formalized]
```

**Multi-session files**: when appending to an existing episode, the new H3 block goes at the **top**, above any older H3 blocks. Each sub-episode is a full block following this template. Result is newest-first, mirroring the index ordering.
