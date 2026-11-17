### § record-theme-state

`edit_metadata(uuid, tags=[…])` — the tag list is written whole, so pass the record's existing tags with `finished` added when the block closes the theme, and the existing tags with it removed when it does not. `tags` is metadata with one writer, so this never rides on the body append. The write bumps `modified_date`, which is why the archive scan weighs the tag before the age.

A newly created episode carries no marker, so a create needs no call; an append that changes the state does.

