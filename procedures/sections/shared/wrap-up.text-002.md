## Arguments

`$ARGUMENTS` = `[all|agent] [fresh]`

- **Mode** (optional): `agent` (default) persists only this agent's own memory, leaving a concurrently-running agent's in-flight work untouched; `all` persists the whole store. The default is the conservative one because `/wrap-up` runs at session end, when nobody is watching what else in the store happens to be dirty.
- **`fresh`** (optional): force fresh mode for the memory update (pass-through to `/update-memory`); default auto-detects delta vs fresh.
- Examples: `/wrap-up` (agent + delta) · `/wrap-up all` · `/wrap-up fresh` · `/wrap-up all fresh`.

---

