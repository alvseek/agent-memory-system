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

Run silently and give one final report. Call `/update-memory` without arguments. It evaluates this conversation since its last successful memory update, or the whole conversation if this is the first. Use the returned evaluation mode and cutoff, gate decisions, promotions, episodic entry, carry-forward count, emotional status, and the episode's **Tech Debts** and **Next Steps**.

If both lists are empty, report “No open items declared from this session.”

@start storage id="wrap-up.finish" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.finish"
@end storage
