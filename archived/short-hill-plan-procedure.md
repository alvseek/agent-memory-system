# Claude Agent - Short Hill Planning Procedure

# Short Hill Protocol

## When to Use This Protocol
Use Short Hill Protocol when you need **quick decision-making** through **rapid brainstorming**. This protocol helps you generate 5-8 solution options quickly, evaluate them simply, and make a decision fast - perfect for mid-planning decisions or time-sensitive choices.

**Perfect for:**
- Quick decisions needed during implementation planning
- Time-sensitive choices (15-30 minutes available)
- Focused problems with clear scope
- Mid-planning decision points (e.g., during Shallow Shore/Deep Trench execution)
- When you need quick ideation with 5-8 options

**NOT for:**
- Complex problems requiring deep analysis → Use High Mountain
- Problems needing root cause discovery → Use High Mountain
- Situations requiring extensive brainstorming → Use High Mountain

*IMPORTANT: To execute the protocol, I have to use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*

1. I have to find and read the [Short Hill Plan Template](//@claude-agents/control-files/plans/short-hill-plan-template.md) file
2. I have to create new plan folder in the project root level `/plans` (if it doesn't exist)
3. I need to copy the [Short Hill Plan Template](//@claude-agents/control-files/plans/short-hill-plan-template.md) file to the `/plans` folder:
   - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
   - **Linux/macOS**: `cp {source} {target}`
4. I have to check the current date using:
   - **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
   - **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`
5. I have to rename the new copy pasted file to `[YYYY-MM-DD]-[project]-[decision-name]-shorthill.md` name pattern
6. I have to fill the [Project Info](//@claude-agents/control-files/plans/short-hill-plan-template.md#project-info) + [Problem](//@claude-agents/control-files/plans/short-hill-plan-template.md#problem) sections
7. Ask the project info and problem for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
8. I have to fill the [Current State Analysis](//@claude-agents/control-files/plans/short-hill-plan-template.md#current-state-analysis) section - brief analysis of what exists now
9. Ask the current state analysis for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
10. I have to fill the [Quick Solution Generation](//@claude-agents/control-files/plans/short-hill-plan-template.md#quick-solution-generation) section - use ONE rapid technique to generate 5-8 solution options
11. Ask the generated solutions for review and if the user need more options, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
12. I have to fill the [Quick Evaluation](//@claude-agents/control-files/plans/short-hill-plan-template.md#quick-evaluation) section - simple Pros/Cons comparison of the 5-8 options
13. Ask the evaluation for review, AND proactively ask: "Do you want multi-agent voting? (5 AI agents vote independently to reduce bias - optional but recommended for important decisions)". Wait for confirmation before moving on.
    - **If YES to multi-agent voting**, execute steps 13a-13d:
      13a. I fill my own Quick Evaluation assessment + vote for one option, add "### Evaluator 1: [Agent Name] ([Model])" section with my assessment and vote
      13b. Spawn 4 Haiku agents in parallel using Task tool with `model: "haiku"`: each agent reads the Short Hill document, independently evaluates all options, adds their assessment in "### Evaluator [2-5]: Haiku Agent [1-4]" section, and votes for one option
      13c. After all agents complete, update the Vote Summary table with all 5 votes
      13d. Calculate Final Tally and present results to Alvi for review before moving to Selected Solution
    - **If NO to multi-agent voting**, proceed directly to step 14 after confirmation to move to Selected Solution

14. I have to fill the [Selected Solution](//@claude-agents/control-files/plans/short-hill-plan-template.md#selected-solution) section with decision and rationale
15. Ask the selected solution for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
16. Now, I have to create the Architecture Decision Record (ADR) document in `/docs/adr/` folder:
    a. First, check if `/docs/adr/` folder exists in project root, if not create it using:
       - **Windows**: `powershell -c "New-Item -ItemType Directory -Path './docs/adr' -Force"`
       - **Linux/macOS**: `mkdir -p ./docs/adr`
    b. Copy the [ADR Template](//@claude-agents/control-files/plans/adr-template.md) to `/docs/adr/` folder:
       - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
       - **Linux/macOS**: `cp {source} {target}`
    c. Rename the ADR file following pattern: `[YYYY-MM-DD]-[short-descriptive-title].md`
       - Example: `/docs/adr/2025-11-17-api-choice-decision.md`
    d. Determine the ADR number by checking existing ADR files in `/docs/adr/` and using next sequential number
17. I have to fill the ADR document sections:
    a. Fill ADR number, title, date, and status (Accepted)
    b. Fill **Problem** section - clear 2-3 sentence problem statement from brainstorming document
    c. Fill **Decision** section - what we decided to build, how it addresses problem, and 3 key reasons why
    d. Fill **What to Build (Requirements)** section - core requirements and success criteria from selected solution
    e. Fill **Alternatives Rejected** section - the 1-2 other options with brief one-sentence rejection reasons
    f. Fill **Full brainstorming context** link to the Short Hill plan file
18. Ask Alvi to review the ADR document, and wait for confirmation
19. Present both documents to Alvi:
    a. Quick brainstorming document: `/plans/[date]-[project]-[decision]-shorthill.md`
    b. Decision summary (ADR): `/docs/adr/[date]-[title].md`
20. Inform Alvi that the ADR document should be used as "Related Documents" reference when continuing the main implementation plan (Shallow Shore/Deep Trench/Quick Surf)
