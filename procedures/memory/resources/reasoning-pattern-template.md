# Reasoning Pattern Template

template_version: 2026-11-09-10-00

Use this fixed structure for every reasoning memory entry.

```markdown
### [Plain, memorable title]
**UUID**: [xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx]

**Instruction**
[State what to do and when it applies. Include any boundary needed to prevent misapplication.]

**Anchor**
[Explain why this matters, using a real event or a concrete reason. Do not invent an incident.]

**Example**
[Show one concrete application. Use a contrasting pair when it makes the difference clearer.]

**Final Conclusion**: [One self-contained sentence under 240 characters that preserves the essential instruction.]
```

## Requirements

- Keep all six fields: title, UUID, Instruction, Anchor, Example, and Final Conclusion.
- Use a plain title without decorative tags or required emojis.
- Generate a UUID for a new pattern; preserve it when rewriting an existing one.
- State each point once. The sections should complement, not repeat, each other.
- Examples may be hypothetical, but must not be presented as events that actually happened.
- The Final Conclusion is the rule’s always-on form, printed under its title in the permanent layer. It must make sense without the rest of the entry.
