### § append-sub-episode

An episode is a single record whose body is the rolling, newest-first sub-episode list. Newest-first then needs no read and no string match — two writes:
1. `prepend(uuid, text="<new H3 block>\n\n---\n\n")` — the new block lands above the previous newest, and the separator you include keeps the two apart. Nothing has to match, so there is no `old_string` to get uniquely right.
2. `edit_metadata(uuid, content_summary="<the record's summary>")` — the summary is metadata and has one writer, so it moves in its own call.

`content_summary` is the whole new summary, not an appended fragment: it describes the record's newest content, so skipping step 2 leaves the listing describing a block the body no longer starts with. Two writes can also disagree if the second fails, which is why both steps belong to this op rather than to the caller's judgement — that is the price of one owner per field.

The index reflects the change automatically (derived `SELECT`).

