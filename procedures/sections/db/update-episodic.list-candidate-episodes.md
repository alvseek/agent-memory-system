### § list-candidate-episodes

`query(agent_id="<domain>", record_type="episode", project="<project>")` → returns the derived index projection (uuid, title, content_summary, tags, dates, **`blocks_total`**) for the agent's active episodes. Theme-match against `title`/`tags`, and read `content_summary` when the theme alone is ambiguous. There is no body here — reading one is a deliberate `get(uuid)`, a page at a time (see `## all-procedures`). `blocks_total` tells you how much body that read will hold before you pay for it. (Archived episodes are excluded by default — pass `include_archived=True` only to reach them.)

