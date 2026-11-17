### § reopen-archived-theme

Two calls, in this order: `edit_metadata(uuid, tags=[<existing without finished>])`, then `unarchive(uuid)`. Clearing first matters — leave the marker in place and the next scan archives the theme straight back. `unarchive` returns the record to the index and to newest-episode selection, after which the append lands normally.

