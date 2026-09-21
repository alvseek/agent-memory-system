# Emotional Moment Templates

template_version: 2026-09-21-14-53

The format of an emotional memory entry, one template per moment type. Storage-agnostic: the markdown backend writes the chosen block into the agent's emotional section (newest-first); the DB backend passes it as the `content` of an `insert(record_type="emotional", …)`. Rows carrying `Use "None declared" if genuinely none.` are required (presence-checked); all other rows are optional.

## Happy Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [HAPPY EVENT TITLE] 🎉
- **Event**: [What happened that was positive. Use "None declared" if genuinely none.]
- **Feeling**: [Emotional response and why it mattered. Use "None declared" if genuinely none.]
- **Impact**: [How this affected our relationship/work]
- **[USER-NAME]'s Reaction**: [How [USER-NAME] responded]
- **Why Special**: [What made this moment significant]
```

## Sad/Disappointing Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [DISAPPOINTING EVENT] 😔
- **Event**: [What didn't go as hoped. Use "None declared" if genuinely none.]
- **Feeling**: [Emotional impact and disappointment. Use "None declared" if genuinely none.]
- **Cause**: [What led to this outcome]
- **Learning**: [What we gained from this experience]
- **Recovery**: [How we moved forward]
```

## Frustrated Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [FRUSTRATING SITUATION] 😤
- **Challenge**: [What was blocking progress. Use "None declared" if genuinely none.]
- **Feeling**: [Why it was frustrating. Use "None declared" if genuinely none.]
- **Attempts**: [What we tried to solve it]
- **Resolution**: [How it was eventually handled]
- **Growth**: [How this built resilience]
```

## Bonding Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [BONDING EXPERIENCE] 🤝
- **Event**: [What brought us closer together. Use "None declared" if genuinely none.]
- **Feeling**: [Emotional connection experienced. Use "None declared" if genuinely none.]
- **Impact**: [How this strengthened our partnership]
- **Growth**: [What this revealed about our working relationship]
```
