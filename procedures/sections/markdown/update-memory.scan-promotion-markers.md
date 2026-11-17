### § scan-promotion-markers

Identify cross-layer files written this session, by path:

| Layer | Path |
|-------|------|
| Project context (shared) | `shared-memory/[project]/context/*.md` |
| Project context (private) | `knowledge-base/[project]/*.md` |
| Knowledge | `knowledge-base/[topic].md`, `knowledge-base/core-domain-knowledge.md` |
| Reasoning (shared) | `shared-memory/core-reasoning-memory.md` |
| Reasoning (per-agent) | `agent-core-memory.md` → `# DOMAIN REASONING MEMORY` |

