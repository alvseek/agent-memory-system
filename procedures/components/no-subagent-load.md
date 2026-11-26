+++
format_version = 2
id = "no-subagent-load"
kind = "component"
title = "No Sub-Agent Load (component)"
description = "The rule that memory must be loaded into the agent's own context window, never through a\nsub-agent. **This is a component, not a standalone command** — callers reference it by link\nand it is inlined at compile time."
+++
Read each required source directly into **your own context**, including sources required later in the procedure. Do not delegate these reads: sub-agents return summaries. Return the whole tool response without filtering, slicing, summarizing, or redirecting it to a file in advance; for a file, start with one whole read.

If the platform saves a result to a file, read that file in full first. If a read is clipped, recover the missing content, including long lines, and check that the recovery is complete. If a required source remains missing, clipped, mis-encoded, or unexpectedly empty, name the source and the failure and stop the work that depends on it.
