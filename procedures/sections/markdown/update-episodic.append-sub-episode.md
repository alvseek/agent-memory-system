### § append-sub-episode

1. **Open the chosen file** in `[AGENT-MEMORY-PATH]/agent-[domain]/episodes/`.
2. **Insert the sub-episode H3 block at the TOP** (newest-first within the file), above any older H3 blocks. Sub-episodes are separated by `---`.
3. **Update the index entry — MOVE-TO-TODAY rule**:
   - Locate the existing entry for this file in the index.
   - Delete it from its current date group (if the group becomes empty, remove the group header too).
   - Insert at the **top of today's date group** (`📂 YYYY-MM-DD:`); create today's group if it doesn't exist.
   - Update the summary from the new block's `**Summary**` row: carry that text verbatim, appended as `+ [new sub-topic]` when the overall theme still holds, or rewritten when the new sub-topic shifts it.

   > **Why move?** Awakening's project-scoped episodic load grabs the top entry as "latest episodic." The move preserves the "top = newest" invariant. Edit-in-place would leave a stale top entry and break awakening's selection logic.

