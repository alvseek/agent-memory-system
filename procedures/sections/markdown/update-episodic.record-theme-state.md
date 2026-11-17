### § record-theme-state

Edit the episode file's frontmatter `tags:` line in place: add `finished` when this block closes the theme, remove it when it does not. Touch nothing else — the body and the other frontmatter fields stay verbatim.

When no `tags:` line exists yet, add one beneath `project:` in the same block. The importer reads episode frontmatter tags into the record, so the marker survives a later import into the DB store even though no tool here reads it.

