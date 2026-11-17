### § load-agent-memory

**One call** — `awaken(domain)` (MCP tool) or `GET /api/awaken?agent_id=<domain>` (HTTP). It assembles and returns the agent's memory payload from Valaskjalf server-side, **project-blind**: no project is accepted or resolved, so `latest_episode` is the newest episode overall and the caller selects its own out of the index:

- `shared.reasoning` — whole fleet-shared reasoning records, read from the shared table rather than from any agent.
- `shared.knowledge_index` — metadata only: uuid, title, content_summary, tags, project and dates. Inspect this alongside the agent's knowledge_index and fetch relevant bodies with get(uuid). Never load every body during awakening. A null legacy summary or an empty index is valid; do not invent a body-derived fallback.
- `shared.ras` — the **universal RAS triggers** (fleet-wide): memory recovery after compaction, and copy-paste-don't-regenerate. Automatic trigger-to-action protocols, whole, alongside reasoning.
- `shared.user_profile` — who [USER-NAME] is (name, philosophy, agent vision), as a single whole record or `null`. Fleet memory too: it does not vary by agent. `null` means nobody has been asked yet, which is the first-run branch in Phase 1 — a record that exists with an empty value inside it is a deliberate blank and is **not** that case.
- `identity` + `reasoning` + `emotional` — this agent's own records, whole (layer ii). `identity` includes the agent's core knowledge and RAS triggers.
- `knowledge_index` + `episodic_index` — metadata-only indexes; bodies via `get(uuid)` on demand (layer iii). Each index entry carries its `project`; the index itself never counts groups, so a row does not say how large its body is. When that size matters before paying for the read, `query(record_type="episode")` returns a projection that does carry `blocks_total`. `search(text)` finds a record but returns only a `snippet`, never a body.
- `latest_episode` — **a page** of the newest episode **overall**, since no project is accepted or resolved: up to three timestamp groups, with `blocks_returned` / `blocks_total` / `next_cursor`. The returned record's own `project` tells you which project it belongs to, and its `uuid` is what continues the read. When the newest overall is not that project's, say so in the open-items report. A non-null `next_cursor` means the body continues; a count smaller than `blocks_total` with a null cursor means you already have all of it.

The 4-layer assembly is a single derived call.

> **Not covered by the payload — and no longer needs to be**: the **awakening instructions** (the Phase 1/Phase 2 protocol) are not a record and are not served, because they are a **component** inlined into this procedure at compile time — the process rides in the prompt, the data comes from `awaken`. That is the whole of what the payload leaves out; the user profile used to be listed here too, and is now a record like any other (`shared.user_profile`, above). See `docs/flows/awaken-db.md` in the memory-server repo.

