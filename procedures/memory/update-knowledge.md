+++
format_version = 2
id = "update-knowledge"
kind = "procedure"
title = "Update Knowledge Memory Protocol"
description = "Keep cross-project knowledge accurate by adding, updating, or skipping a finding."
argument_name = "context"
argument_description = "the finding and its supporting evidence; asks for the finding if omitted"
+++
# Update Knowledge Memory Protocol

Keep cross-project knowledge accurate. A runbook or convention specific to one project belongs in project context.

## Arguments

`$ARGUMENTS` — the finding and its supporting evidence, from `/update-memory` or a direct request. If either is missing, ask for it on a direct request; during unattended wrap-up, defer the finding for review.

## 1. Find the entry that answers the same question

Start with the acting agent’s active general knowledge and the shared knowledge available at awakening. Use titles and summaries to find plausible entries, then read their bodies (**§ find-entry**). A keyword match alone does not mean two entries answer the same question.

@start storage id="update-knowledge.find-entry" ref="procedures/memory/storage-backends/{backend}.md" target="update-knowledge.find-entry"
@end storage

- **Skip** if the existing answer and its limits are accurate. Return the covering entry’s name without writing.
- **Update** if the answer is incomplete, outdated, or broader than the evidence supports. Apply verified factual corrections and additions to the existing entry without approval, including shared entries. If an edit would change a shared decision or the supporting evidence conflicts, ask for a decision before writing. During unattended wrap-up, defer just that edit instead of waiting. Keep the original entry; do not create a private copy.
- **Add** if no entry answers the question. Create one general knowledge entry owned by the acting agent.

## 2. Save the answer and its listing

State what the evidence shows and under what conditions. Include the source or observation, and its version or date when that affects the answer. For a new entry, write a one-line summary a reader can use to find it. For an update, revise the summary only if it no longer describes the entry accurately.

@start storage id="update-knowledge.save" ref="procedures/memory/storage-backends/{backend}.md" target="update-knowledge.save"
@end storage

Return `added`, `updated`, or `skipped` with the entry name. For a deferred edit, return `Needs review` with the proposed change and the evidence or decision needed; nothing was saved. If the body was saved but the listing was not, report the partial write rather than claiming success.
