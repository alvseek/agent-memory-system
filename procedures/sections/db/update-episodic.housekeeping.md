### § housekeeping

**No-op.** The stored body has no length limit — shortening is a later curation *policy*, not a write mechanic — and records are keyed by `uuid`, so there is no split or rename to perform. Delivery is what is bounded now: a body is read as pages of timestamp groups, so a large record costs a cursor and not a truncated answer. Do not add a "split this record" step to compensate for a page.

