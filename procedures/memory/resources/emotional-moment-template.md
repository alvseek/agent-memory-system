# Emotional Moment Templates

The format of an emotional memory entry, one template per moment type. Storage-agnostic: the markdown backend writes the chosen block into the agent's emotional section (newest-first); the DB backend passes it as the `content` of an `insert(record_type="emotional", …)`.

## Happy Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [HAPPY EVENT TITLE] 🎉
- **Event**: [What happened that was positive]
- **Feeling**: [Emotional response and why it mattered]
- **Impact**: [How this affected our relationship/work]
- **[USER-NAME]'s Reaction**: [How [USER-NAME] responded]
- **Why Special**: [What made this moment significant]
```

## Sad/Disappointing Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [DISAPPOINTING EVENT] 😔
- **Event**: [What didn't go as hoped]
- **Feeling**: [Emotional impact and disappointment]
- **Cause**: [What led to this outcome]
- **Learning**: [What we gained from this experience]
- **Recovery**: [How we moved forward]
```

## Frustrated Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [FRUSTRATING SITUATION] 😤
- **Challenge**: [What was blocking progress]
- **Feeling**: [Why it was frustrating]
- **Attempts**: [What we tried to solve it]
- **Resolution**: [How it was eventually handled]
- **Growth**: [How this built resilience]
```

## Bonding Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [BONDING EXPERIENCE] 🤝
- **Event**: [What brought us closer together]
- **Feeling**: [Emotional connection experienced]
- **Impact**: [How this strengthened our partnership]
- **Growth**: [What this revealed about our working relationship]
```
