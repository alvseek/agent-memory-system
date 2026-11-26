+++
format_version = 2
id = "awaken-agent"
kind = "procedure"
title = "Awaken Agent"
description = "Load agent memory and activate a domain-specific agent. *Where* the memory is loaded from is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics))."
argument_name = "domain"
argument_description = "the agent domain to awaken; asks if omitted"
+++
# Awaken Agent

Load agent memory and activate a domain-specific agent.

## Arguments

**Domain:** `$ARGUMENTS` — the agent's domain name (e.g. `unreal`), not its identity UUID. If omitted, ask: "Which agent domain should I awaken?"

---

## Procedure

### Step 1: Load the Awakening Set

Load the four layers using **§ load-agent-memory**:

1. **Agent identity** — this domain's identity, core knowledge, and RAS triggers.
2. **Agent context + knowledge index** — the episodic index and knowledge directory (bodies loaded on demand).
3. **Shared reasoning patterns.**
4. **Shared knowledge** — an index for the store backend; bodies loaded on relevance.

**CRITICAL — Load integrity**

@start component id="awaken-agent.include-no-subagent-load" ref="procedures/components/no-subagent-load.md"
@end component
@start storage id="core-instruction-control-files.load-agent-memory" ref="procedures/memory/storage-backends/{backend}.md" target="core-instruction-control-files.load-agent-memory"
@end storage

### Step 2: Follow Awakening Instructions

Follow the phased protocol below — Phase 1 (Process Loaded Identity), then Phase 2 (Load Central Context & Report).

**Awakening protocol**

---

@start component id="awaken-agent.include-core-instruction-control-files" ref="procedures/components/core-instruction-control-files.md"
@end component
