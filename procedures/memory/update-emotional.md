+++
format_version = 2
id = "update-emotional"
kind = "procedure"
title = "Update Emotional Memory Protocol"
description = "Save one emotional moment from the conversation in the acting agent’s memory."
argument_name = "moment_type"
argument_description = "happy, sad, frustrated or bonding; asks if omitted"
+++
# Update Emotional Memory Protocol

Save one emotional moment from the conversation in the acting agent’s memory.

## Arguments

`$ARGUMENTS` — moment type: `happy`, `sad`, `frustrated`, or `bonding`. If omitted, ask which type to capture.

## 1. Describe the moment

Use the template block for the chosen type (**§ template**). Write what happened, how it felt, and why it mattered. When `/update-memory` supplies the event and the user’s exact words, use that exchange. Describe the user’s reaction only if the conversation supports it.

Read the current UTC time once and use it in the entry heading (`YYYY-MM-DD HH:MM`).

@start storage id="update-emotional.template" ref="procedures/memory/storage-backends/{backend}.md" target="update-emotional.template"
@end storage
## 2. Save the moment

Save the entry for the acting agent (**§ persist-emotional**).

@start storage id="update-emotional.persist-emotional" ref="procedures/memory/storage-backends/{backend}.md" target="update-emotional.persist-emotional"
@end storage
