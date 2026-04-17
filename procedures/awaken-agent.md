# Awaken Agent

Load agent memory and activate a domain-specific agent.

## Arguments

`$ARGUMENTS`

- `/awaken-agent [domain]` → Awaken the specified domain agent (e.g., meta, backend-nestjs, frontend-react)

If no arguments provided, ask: "Which agent domain should I awaken?"

---

## Procedure

### Step 1: Trigger Awakening

Execute the `Awaken Agent [DOMAIN]!` trigger defined in the global instructions file (`[GLOBAL-INSTRUCTIONS-FILE]`). This is the single source of truth for the awakening protocol — it reads the 5 core files and follows the phased awakening instructions.

---
