# Delegate Agent

Send a background delegation request to another specialized agent. The target agent awakens (if new) or resumes (if UUID) and works autonomously on the task while the caller continues working. This procedure is designed for agent-to-agent communication — the calling agent constructs the prompt and sends it without user confirmation.

## Arguments

`$ARGUMENTS`

- `/delegate-agent [Name|UUID]` → Construct structured prompt, then delegate to the target agent
- `/delegate-agent` → Will ask which agent to delegate to

If no arguments provided, ask: "Which agent do you want to delegate to? Provide a Name (to awaken) or UUID (to resume)."

---

## Procedure

### Step 1: Resolve Target

Parse the argument:
- If it looks like a UUID (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`), this is a **resume**
- If it's a name (e.g., "Backend Django", "Frontend Nextjs"), this is a **new awakening** — verify the agent folder exists at `[AGENT-MEMORY-PATH]/agent-[folder-name]/`

### Step 2: Construct Structured Prompt

Fill this template based on the current task context. All fields are required:

```
## Theme
[Short label for the fleet map — e.g., "user auth middleware", "inventory tags UI"]

## Context
[What you're working on and why this task needs to be delegated]

## Task
[Clear description of what the target agent should accomplish]

## Acceptance Criteria
[How do we know the task is done? What conditions must be met?]

## Expected Deliverables
[What files, code, documents, or outputs should be produced?]

## Constraints
[Any limitations, patterns to follow, things to avoid, or dependencies to be aware of]
```

Do NOT send vague or open-ended prompts. Be specific about the task, what "done" looks like, and what constraints apply.

### Step 3: Execute

Run the script (background):

```bash
bash "[AGENT-MEMORY-PATH]/control-files/scripts/delegate-agent.sh" "[Name|UUID]" "[structured prompt]" "[theme]"
```

The script returns the UUID immediately. The target agent works in the background.

### Step 4: Continue Working

Note the returned UUID for later follow-up. Continue with your own work — do not block waiting for the delegated agent.

To check status later: `/ask-agent [UUID]` with a status request.
To wrap up a completed session: `bash "[AGENT-MEMORY-PATH]/control-files/scripts/wrap-up-agent.sh" [UUID]`

---
