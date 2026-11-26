+++
format_version = 2
id = "wrap-up"
kind = "procedure"
title = "Wrap Up Session"
description = "Save this session's memory and report what changed."
argument_name = "mode"
argument_description = "Optional delta or fresh evaluation; omit to auto-detect"
calls = { markdown = ["update-memory", "push-memory"], db = ["update-memory"] }
+++
# Wrap Up Session

Save this session's memory and report what changed.

## Arguments

@start storage id="wrap-up.arguments" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.arguments"
@end storage
Use `delta` for work since the last matching update, or `fresh` for the whole session. Omit both to let `/update-memory` choose based on the session theme.

## Procedure

Run silently and give one final report. Execute `/update-memory`, forwarding the evaluation argument if supplied. If it cannot start, report why and stop. Otherwise use its returned results: evaluation mode and cutoff, gate decisions, promotions, episodic entry, carry-forward count, emotional status, and the episode's **Tech Debts** and **Next Steps**.

@start storage id="wrap-up.persist-store" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.persist-store" applies_to="markdown"
@end storage
### Final report

@start storage id="wrap-up.report" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.report" applies_to="markdown"
@end storage
@start storage id="wrap-up.report-db" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.report-db" applies_to="db"
@end storage

If both lists are empty, report “No open items declared from this session.”
@start storage id="wrap-up.failure-report" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.failure-report" applies_to="markdown"
@end storage
