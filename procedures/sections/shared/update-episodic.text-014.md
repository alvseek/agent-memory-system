## Returns

This procedure hands two values back to its caller — **`Tech Debts`** and **`Next Steps`**, exactly as they were written into the sub-episode block. They are **captured as data, never printed**: `/update-memory` runs this procedure inside its silent phases, and the caller that surfaces open items prints them once in its own summary.

Both branches produce them:

- **Append** — the union staged in [Append Sub-Episode](#append-sub-episode) step 1c: items carried forward from the prior top sub-episode that are still open, plus genuinely new items from this delta window.
- **Create** — the two fields as composed for the first sub-episode of a new episode. There is no prior block to carry forward from, so the lists hold this session's items alone. An empty list is a real answer here — it means "none declared", not "not available".

Because both branches compose these lists before writing them, a caller never has to re-read the store to learn what the newest sub-episode says: the agent that wrote the block is the one being asked.

---

