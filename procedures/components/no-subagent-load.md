# No Sub-Agent Load (component)

The rule that memory must be loaded into the agent's own context window, never through a
sub-agent. **This is a component, not a standalone command** — callers reference it by link
and it is inlined at compile time.

*Consumed by `/awaken-agent` (Step 1) and `/refresh-memory` (Step 3) — the two procedures
that pull the agent's memory into context.*

---

Use the **Read tool directly**. Do **NOT** delegate to a sub-agent (Agent tool /
general-purpose / Explore): sub-agents return summaries, and this load needs the full
content in **your own** context window, not a summary. A delegated load produces a hollow
result — diluted identity and missing reasoning patterns.
