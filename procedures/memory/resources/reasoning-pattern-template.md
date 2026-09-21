# Reasoning Pattern Template

template_version: 2026-09-21-14-53

The format of a reasoning/logic memory entry. Storage-agnostic: the markdown backend writes this into the agent's reasoning section; the DB backend passes it as the `content` of an `insert(record_type="reasoning", …)`. Rows carrying `Use "None declared" if genuinely none.` are required (presence-checked); rows marked optional are not.

Lean shape — shrink the prose, keep the vivid anchor and any load-bearing distinction. `Do` / `Guardrail` / `Siblings` are optional (include only when they add something). `Final Conclusion` is a one-sentence capsule fusing Rule+Why+Signals, **not** a copy of the Rule.

```markdown
### **[SHORT MEMORABLE TITLE]** [EMOJI] [PATTERN TYPE] [EMOJI]
**UUID**: [generate new UUID in format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx]
**Rule**: [the specific behavior required — one or two sentences. Use "None declared" if genuinely none.]
**Why**: [root problem + the vivid concrete beat (real quote/moment) that anchors it, compressed. Use "None declared" if genuinely none.]
**Signals**: [how to recognize when the pattern fires. Use "None declared" if genuinely none.]
**Do**: [optional — steps, only if they add beyond the Rule]
**Guardrail**: [optional — the mirror failure / over-application to avoid]
**Siblings**: [optional — related UUIDs and how this one differs]
**Final Conclusion**: [one flowing sentence fusing Rule+Why+Signals — the compression-survival capsule. Use "None declared" if genuinely none.]
```

> For the older, fuller `What happened` narrative shape, see the [add-reasoning-full.md](../add-reasoning-full.md) procedure.
