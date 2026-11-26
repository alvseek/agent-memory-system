+++
format_version = 2
id = "update-reasoning"
kind = "procedure"
title = "Update Reasoning Memory Protocol"
description = "Compare a proposed decision rule with active reasoning memory, then add, refine, or skip it."
argument_name = "context"
argument_description = "the proposed decision rule and a concrete example; asks for the rule if omitted"
+++
# Update Reasoning Memory Protocol

Compare the proposed rule with the rules the agent already uses. The question is whether it would change a decision.

## Arguments

`$ARGUMENTS` — the proposed rule and a concrete example. Use the proposal from `/update-memory` or from a direct request. If no rule was supplied, ask what decision the lesson should guide.

## 1. Compare the decisions

Compare active rules owned by the acting agent and applicable shared rules (**§ read-reasoning-store**). Use the example to ask: in the same situation, would an existing rule already lead to the proposed action?

@start storage id="update-reasoning.read-reasoning-store" ref="procedures/memory/storage-backends/{backend}.md" target="update-reasoning.read-reasoning-store"
@end storage

- **Skip** if the action is already covered. Name the covering rule; a different title or another example is not a reason to write.
- **Refine** if the proposal adds a condition, exception, or correction to an existing rule. Change only the affected wording and preserve the existing UUID. If the rule is shared, propose the exact change and wait for explicit agreement before editing it. Do not add a private copy instead.
- **Add** if no existing rule covers the decision. Create one rule owned by the acting agent.

## 2. Save the chosen change

For an addition, use the reasoning-pattern template. For a refinement, keep the Final Conclusion consistent with the changed instruction. Skip requires no write.

@start storage id="update-reasoning.save" ref="procedures/memory/storage-backends/{backend}.md" target="update-reasoning.save"
@end storage

Return `added`, `refined`, or `skipped` with the rule’s name. Report a write failure rather than returning a successful change.
