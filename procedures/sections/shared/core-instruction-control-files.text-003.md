### Phase 2: Load Central Context & Report

3. **Load recent context (central)**: load the most recent central memory:
    - **Episodic**: from the already-loaded episodic index, take the newest entry → load that episode (**§ load-latest-episode**). A caller that knows its own project may instead load a different entry out of that index. What arrives is a **page** of timestamp groups, not necessarily the whole rolling body: continue with the row's own `uuid` and `next_cursor` only when this session's carry-forward needs the older sub-episodes, and never present a page as the episode.
4. **Report**: emit one consolidated block containing:
    - **Identity**: UUID + domain role.
    - **Latest episodic + open items**: filename + newest sub-episode title. Then surface its Tech Debts + Next Steps verbatim:
      ```
      📋 Carrying forward from last session:
      Tech debts:
        - [item]
      Next steps:
        - [item]
      ```
      If the episode is not the one expected for this work, say so explicitly and skip open items. If Tech Debts + Next Steps are empty: report *"no open items from last session."* If the page did not reach the end of the record (`next_cursor` non-null), say that the older sub-episodes were not read instead of implying the list above is complete.
    - **Knowledge Base**: if the knowledge index has entries, mention `/load-knowledge` (also auto-loads on relevance). Else skip.
    - **Episodic browsing**: mention `/load-episodic` (also auto-loads on relevance).
    - **Load-integrity report** (UUID `c4e7a19f` — SURFACE LOAD FAILURES): if ANY layer loaded during awakening failed — missing, empty, mis-encoded, or truncated — say so explicitly, naming the layer and the failure mode. For the size case specifically, follow **§ oversized-memory-warning**.

