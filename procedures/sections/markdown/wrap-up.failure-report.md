**On failure** (Step 2's outcome reports anything of this agent's still uncommitted or unpushed) — do NOT print "complete". Print this block instead:

```
🚨 WRAP-UP INCOMPLETE — MEMORY NOT SAVED. NEED CONFIRMATION.

[Memory update / Open items sections — same as above]

Memory persisted — FAILED / INCOMPLETE:
- [repo]: ⚠️ [uncommitted N file(s) / branch ahead by N / push error: <reason>]

⚠️ This session's memory is written but NOT saved to the remote. What remains, and where:
- [repo → which path is uncommitted or unpushed]
(In `agent` mode another agent's dirty files are expected and are NOT listed here.)

Retry the persistence, or resolve the blocker, before leaving — the wrap-up is complete only when this session's memory is committed AND pushed.
```
