### § create-episode

`insert(agent_id="<domain>", record_type="episode", project="<project>", title="<project-theme>", tags=[…], content="<first sub-episode block>", content_summary="<the block's Summary row>", template_version="<the template's current stamp>")`. Read `episodic-entry-template` from resources first and declare its `template_version` — a missing or stale version is refused. `content_summary` is required for an episode: pass the block's `**Summary**` row verbatim, because that one line is what the index projection lists the record by. The record is assembled and `uuid`-stamped server-side and appears in the index projection immediately.

