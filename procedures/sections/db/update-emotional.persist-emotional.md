### § persist-emotional

`insert(agent_id="<domain>", record_type="emotional", title="<moment title>", content="<moment block>", template_version="<the template's current stamp>")`. Read `emotional-moment-template` from resources first and declare its `template_version` — a missing or stale version is refused. **Newest-first is a read concern** — the index projection orders by date, so ordering is automatic.

