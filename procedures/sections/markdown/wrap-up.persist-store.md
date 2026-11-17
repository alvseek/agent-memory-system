### § persist-store

This store is a git repository, so capturing memory is not the same as saving it. Execute `/push-memory <mode>` with the mode `/wrap-up` resolved, and carry its per-repo result back as the persistence outcome — pushed with its commit hash, no changes, or failed, including any branch left ahead of its remote.

**Completion gate** (per NO TODOS LEFT BEHIND, UUID a1b2c3d4): the wrap-up is complete only when Step 2's outcome says this session's memory is persisted. A backend that is durable at write time passes trivially. A git-backed store passes only when nothing in scope is dirty and no branch carrying this agent's commits is ahead of its remote. In `agent` mode another agent's dirty files are expected, reported, and never a failure.

