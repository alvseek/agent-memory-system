### § persist-knowledge

`insert(agent_id="<domain>", record_type="knowledge", title="<knowledge area>", tags=[…], content="<knowledge doc>", content_summary="<the entry's Summary row>", template_version="<the template's current stamp>")`. Read `knowledge-file-template` from resources first and declare its `template_version` — a missing or stale version is refused. `content_summary` is required for a knowledge record: pass the entry's `**Summary**` row verbatim, because that one line is what the knowledge index lists the record by. General/central knowledge only — Munnin is project-blind (no project-scoped knowledge).

