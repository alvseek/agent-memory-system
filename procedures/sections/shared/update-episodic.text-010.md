#### Step 6: Branch — Append OR Create

- **If Append** → execute [Append Sub-Episode](#append-sub-episode)
- **If Create** → execute [Create New Episode](#create-new-episode)

> **Scope note**: `/update-episodic` only writes the episode + its index projection. Cross-layer concerns (promotion markers to project context / knowledge / reasoning, and emotional memory auto-capture) are handled by `/update-memory`, which calls this procedure and then orchestrates the cross-layer work. If you're calling `/update-episodic` directly and want cross-layer orchestration, use `/update-memory` instead.

---

