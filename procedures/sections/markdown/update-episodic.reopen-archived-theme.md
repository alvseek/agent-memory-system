### § reopen-archived-theme

Markdown keeps no archive flag on a record: an archived episode is one whose index line was moved into `archive/[YYYY]-archived-context.md`, while the file itself never moved. To reopen it, remove `finished` from the file's frontmatter, move its index line back from the archive file into the episode index (newest-first, under today's date group), and decrement the archive's count. Then append normally.

