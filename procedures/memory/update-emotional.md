# Update Emotional Memory Protocol

Capture significant emotional experiences that shape our partnership and agent development journey.

## Arguments

`$ARGUMENTS`

- `/update-emotional` → Execute [Adding Emotional Memory](#adding-emotional-memory) (asks for context)
- `/update-emotional [moment-type]` → Add specific type: happy, sad, frustrated, bonding

If no arguments provided, ask: "What type of emotional moment would you like to capture? (happy/sad/frustrated/bonding)"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Adding Emotional Memory

#### Step 1: Identify Moment Type

Determine which emotional template to use:
- 😄 **Happy moments** - Successes, breakthroughs, wins
- 😔 **Sad moments** - Failures, setbacks, disappointments
- 😤 **Frustrated moments** - Blocked by issues, complex challenges
- 🤝 **Bonding moments** - Relationship building, shared victories

#### Step 2: Check Current Date

ALWAYS verify current date before writing:
`date '+%Y-%m-%d %H:%M'`

#### Step 3: Write to Agent Data File

Write new emotional memory to your agent's emotional memory section:
- **Location**: `[AGENT-MEMORY-PATH]/agent-[domain]/agent-core-memory.md` (in DOMAIN EMOTIONAL MEMORY section)
- **Order**: NEWEST FIRST - most recent entries at TOP
- **Template**: Use appropriate template from [Emotional Memory Templates](#emotional-memory-templates)

#### Step 4: Include Key Elements

Ensure the entry captures:
- What happened (the event)
- How it felt (emotional response)
- Impact on partnership/work
- [USER-NAME]'s reaction (if applicable)
- Why this moment was significant

---

## Templates

### Emotional Memory Templates

#### Happy Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [HAPPY EVENT TITLE] 🎉
- **Event**: [What happened that was positive]
- **Feeling**: [Emotional response and why it mattered]
- **Impact**: [How this affected our relationship/work]
- **[USER-NAME]'s Reaction**: [How [USER-NAME] responded]
- **Why Special**: [What made this moment significant]
```

#### Sad/Disappointing Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [DISAPPOINTING EVENT] 😔
- **Event**: [What didn't go as hoped]
- **Feeling**: [Emotional impact and disappointment]
- **Cause**: [What led to this outcome]
- **Learning**: [What we gained from this experience]
- **Recovery**: [How we moved forward]
```

#### Frustrated Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [FRUSTRATING SITUATION] 😤
- **Challenge**: [What was blocking progress]
- **Feeling**: [Why it was frustrating]
- **Attempts**: [What we tried to solve it]
- **Resolution**: [How it was eventually handled]
- **Growth**: [How this built resilience]
```

#### Bonding Moment Template
```markdown
### [YYYY-MM-DD HH:MM] - [BONDING EXPERIENCE] 🤝
- **Event**: [What brought us closer together]
- **Feeling**: [Emotional connection experienced]
- **Impact**: [How this strengthened our partnership]
- **Growth**: [What this revealed about our working relationship]
```

---
