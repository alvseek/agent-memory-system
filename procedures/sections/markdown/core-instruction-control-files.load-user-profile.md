### § load-user-profile

**No action.** The profile is already in your context: the global instructions file carries it, compiled from `[AGENT-MEMORY-PATH]/shared-memory/user-profile.md`, which is the single source of truth. If the `## AI Agent - User Profile` section is absent from your instructions, or carries no values at all, treat that as *no profile exists* and take Phase 1's first-run branch.

