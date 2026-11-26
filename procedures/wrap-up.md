+++
format_version = 2
id = "wrap-up"
kind = "procedure"
title = "Wrap Up Session"
description = "Save this session's memory and report what changed."
argument_name = "mode"
argument_description = "Optional wrap-up arguments; use fresh to re-evaluate the whole session"
calls = { markdown = ["update-memory", "push-memory"], db = ["update-memory"] }
+++
# Wrap Up Session

Save this session's memory and report what changed.

## Arguments

@start storage id="wrap-up.arguments" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.arguments"
@end storage
By default, `/update-memory` uses the session theme to decide whether to evaluate the whole session or only work since the previous update. Pass `fresh` to evaluate the whole session.

## Procedure

Run silently and give one final report. Execute `/update-memory`, forwarding `fresh` if supplied. Use its returned results: evaluation mode and cutoff, gate decisions, promotions, episodic entry, carry-forward count, emotional status, and the episode's **Tech Debts** and **Next Steps**.

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
