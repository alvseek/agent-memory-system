### § recover-missing-foundations

The whole shared reasoning foundation and the metadata-only shared knowledge directory have different load contracts. An empty `shared.knowledge_index` is a valid empty directory, not a missing foundation. A missing/malformed field is a payload failure. Check reasoning separately before diagnosing:

- **Other layers also short or cut mid-record** → the payload was **truncated in transit** (the MCP tool-result cap), not empty at rest. The store is fine; the transport is not.
- **Only `shared.reasoning` unexpectedly empty** → the store has no active shared reasoning for this user (possibly an unseeded or wrong tenant). This is not an agent-scoping mistake. Do not treat an empty knowledge index as evidence of the same problem.

For **transport truncation**, recover the complete response per **§ oversized-memory-warning** before diagnosing the store. Only genuinely absent records need **server-side** recovery — seeding the records (importer / `insert`); there is nothing to create on this end. If the foundations remain unavailable, report the failure and STOP: do not fabricate them and do not continue on partial context (`c4e7a19f`).

