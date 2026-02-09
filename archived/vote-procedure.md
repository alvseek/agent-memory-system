# Claude Agent - Vote Protocol Procedure

## Instruction for Agent - Procedure Steps:
*IMPORTANT: To execute the protocol, I have to use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into voting is prohibited*

1. **Collect Options from User**: Ask Alvi to provide the options to vote on. Format: "Please provide the options you want to vote on (2-8 options recommended)"

2. **Confirm Decision Context**: Ask Alvi: "What is the decision context? (Brief description of what we're deciding and why it matters)"

3. **Format Voting Document**: Create a voting summary in docs/adr, name using following pattern: `[YYYY-MM-DD]-adr-vote-[short-descriptive-title].md`, with this structure:
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

4. **Execute My Own Vote (Evaluator 1)**: I evaluate all options, add my assessment with brief pros/cons reasoning, and cast my vote.

5. **Spawn 4 Haiku Agents for Independent Voting**: Use Task tool to spawn 4 parallel Haiku agents with `model: "haiku"`. Each agent receives the adr file for context and write the vote

6. **Collect and Tally Votes**: After all 4 Haiku agents complete, update the Vote Summary table with all 5 votes:
   - Count votes for each option
   - Identify winning option
   - Determine consensus level:
     - **Unanimous**: 5/5 votes for same option
     - **Strong Majority**: 4/5 votes for same option
     - **Majority**: 3/5 votes for same option
     - **Split**: No clear majority (2-2-1 or similar)

7. **Present Results to Alvi**: Present the complete voting results with:
   - Winner and vote count
   - Consensus level
   - Brief summary of key reasoning from voters
   - If split decision: highlight the top 2 options and key differentiators

8. **Ask To Keep This ADR File**: Ask Alvi: "Do you want me to keep this ADR (Architecture Decision Record) vote file? (Y/N)"
   - **If YES**: keep it
   - **If NO**: remove the file

9. **End Procedure**: Voting complete. Inform Alvi the decision is documented and can be referenced in future implementation work.
