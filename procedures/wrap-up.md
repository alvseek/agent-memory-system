+++
format_version = 2
id = "wrap-up"
kind = "procedure"
title = "Wrap Up Session"
description = "Save this session's memory and report what changed."
calls = { markdown = ["update-memory", "push-memory"], db = ["update-memory"] }
+++
# Wrap Up Session

Save this session's memory and report what changed.

## Save memory

Run silently and give one final report. Call `/update-memory` without arguments. The first wrap-up evaluates the whole session; later wrap-ups evaluate only work since the last matching update. Use the returned evaluation mode and cutoff, gate decisions, promotions, episodic entry, carry-forward count, emotional status, and the episode's **Tech Debts** and **Next Steps**.

If both lists are empty, report “No open items declared from this session.”

@start storage id="wrap-up.finish" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.finish"
@end storage
