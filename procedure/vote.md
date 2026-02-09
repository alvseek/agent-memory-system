# Vote Protocol

Execute multi-agent voting for decision-making - 5 AI agents vote independently on user-provided options to reduce bias and reach consensus.

## Arguments

`$ARGUMENTS`

- `/vote` → Start voting session (will ask for options)

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into voting is prohibited*

### Step 1: Collect Options

Ask Alvi to provide the options to vote on. Format: "Please provide the options you want to vote on (2-8 options recommended)"

### Step 2: Confirm Decision Context

Ask Alvi: "What is the decision context? (Brief description of what we're deciding and why it matters)"

### Step 3: Create Voting Document

Create a voting summary in `docs/adr`, name using pattern: `[YYYY-MM-DD]-adr-vote-[short-descriptive-title].md`

Get current date:
- **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd'"`
- **Linux/macOS**: `date '+%Y-%m-%d'`

---

## Templates

### Voting Document Structure

```markdown
## Voting Session: [Decision Context]

### Options to Vote On:
1. **Option 1**: [Description]
2. **Option 2**: [Description]
[... more options ...]

### Voting Criteria:
- Which option best solves the problem?
- Which option has the best trade-offs?
- Which option is most practical to implement?

---

## Evaluator Votes:
[To be filled by agents]

### Evaluator 1: [Agent Name] ([Model])
**Assessment**:
- Option 1: [Brief pros/cons]
- Option 2: [Brief pros/cons]
[... more options ...]

**My Vote**: Option [X]
**Reasoning**: [1-2 sentences why this option wins]

### Vote Summary:
| Option | Votes | Voters |
|--------|-------|--------|
| Option 1 | 0 | |
| Option 2 | 0 | |
[... more options ...]

### Final Tally:
**Winner**: [TBD]
**Vote Count**: [TBD]
**Consensus Level**: [Unanimous/Strong Majority/Majority/Split]
```

---

## Procedure (continued)

### Step 4: Execute My Own Vote

Evaluate all options, add my assessment with brief pros/cons reasoning, and cast my vote as Evaluator 1.

### Step 5: Spawn 4 Haiku Agents

Use Task tool to spawn 4 parallel Haiku agents with `model: "haiku"`. Each agent receives the ADR file for context and writes their vote.

### Step 6: Collect and Tally Votes

After all 4 Haiku agents complete, update the Vote Summary table with all 5 votes:
- Count votes for each option
- Identify winning option
- Determine consensus level:
  - **Unanimous**: 5/5 votes for same option
  - **Strong Majority**: 4/5 votes for same option
  - **Majority**: 3/5 votes for same option
  - **Split**: No clear majority (2-2-1 or similar)

### Step 7: Present Results

Present the complete voting results with:
- Winner and vote count
- Consensus level
- Brief summary of key reasoning from voters
- If split decision: highlight the top 2 options and key differentiators

### Step 8: Ask to Keep ADR File

Ask Alvi: "Do you want me to keep this ADR (Architecture Decision Record) vote file? (Y/N)"
- **If YES**: keep it
- **If NO**: remove the file

### Step 9: End Procedure

Voting complete. Inform Alvi the decision is documented and can be referenced in future implementation work.

---
