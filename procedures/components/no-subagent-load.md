+++
format_version = 2
id = "no-subagent-load"
kind = "component"
title = "No Sub-Agent Load (component)"
description = "The rule that memory must be loaded into the agent's own context window, never through a\nsub-agent. **This is a component, not a standalone command** — callers reference it by link\nand it is inlined at compile time."
+++
Run the load yourself, in this context. Do **NOT** delegate it to a sub-agent (Agent
tool / general-purpose / Explore): sub-agents return summaries, and this load needs
the full content in **your own** context window, not a summary. A delegated load
produces a hollow result — diluted identity and missing reasoning patterns.
