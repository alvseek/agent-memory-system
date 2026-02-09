# Claude Agent - High Mountain Planning Procedure

# High Mountain Protocol

## When to Use This Protocol
Use High Mountain Protocol when you need **systematic creative problem-solving** through **structured brainstorming**. This protocol helps you explore problems comprehensively using multiple creative techniques (5 Whys, SCAMPER, Mind Mapping) and converge on the best solution through evaluation frameworks.

**Perfect for:**
- Complex problems requiring creative solutions
- Issues needing root cause analysis and innovative thinking
- Situations where multiple solution approaches should be explored
- Problems that benefit from divergent → convergent thinking cycles

*IMPORTANT: To execute the protocol, I have to use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*

1. I have to find and read the [High Mountain Plan Template](//@claude-agents/control-files/plans/high-mountain-plan-template.md) file
2. I have to create new plan folder in the project root level `/plans` (if it doesn't exist)
3. I need to copy the [High Mountain Plan Template](//@claude-agents/control-files/plans/high-mountain-plan-template.md) file to the `/plans` folder:
   - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
   - **Linux/macOS**: `cp {source} {target}`
4. I have to check the current date using:
   - **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
   - **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`
5. I have to rename the new copy pasted file to `[YYYY-MM-DD]-[project]-[theme].md` name pattern
6. I have to fill the [Project Info](//@claude-agents/control-files/plans/high-mountain-plan-template.md#project-info) + [Problem Statement](//@claude-agents/control-files/plans/high-mountain-plan-template.md#problem-statement) sections
7. Ask the project info and problem statement for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
8. I have to fill the [Problem Analysis](//@claude-agents/control-files/plans/high-mountain-plan-template.md#problem-analysis) section including root cause exploration using 5 Whys technique
9. Ask the problem analysis for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
10. I have to fill the [Divergent Thinking Phase](//@claude-agents/control-files/plans/high-mountain-plan-template.md#divergent-thinking-phase) section using multiple brainstorming techniques (SCAMPER, Mind Mapping, Reverse Brainstorming, etc.) to generate creative solutions
11. Ask the divergent thinking results for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
12. I have to fill the [Convergent Thinking Phase](//@claude-agents/control-files/plans/high-mountain-plan-template.md#convergent-thinking-phase) section evaluating and prioritizing the generated solutions
13. Ask the convergent thinking evaluation for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
14. I have to fill the [Selected Solution](//@claude-agents/control-files/plans/high-mountain-plan-template.md#selected-solution) sections with clear rationale and technical design
15. Ask the selected solution for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
16. Then, I have to do a self final review for the doc, by thinking critically, very hard and very carefully, as if this is another person's work (this step is very important):
    a. Is the problem clearly defined and root cause identified?
    b. Did we explore enough creative solutions using multiple techniques?
    c. Is the evaluation framework clear and objective?
    d. Is the selected solution justified with clear rationale?
    e. Are there any gaps in the brainstorming or evaluation process?
    f. Is the decision rationale comprehensive and evidence-based?
17. Present the self final review to Alvi, and wait for confirmation before moving on to ADR creation steps
18. Now, I have to create the Architecture Decision Record (ADR) document in `/docs/adr/` folder:
    a. First, check if `/docs/adr/` folder exists in project root, if not create it using:
       - **Windows**: `powershell -c "New-Item -ItemType Directory -Path './docs/adr' -Force"`
       - **Linux/macOS**: `mkdir -p ./docs/adr`
    b. Copy the [ADR Template](//@claude-agents/control-files/plans/adr-template.md) to `/docs/adr/` folder:
       - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
       - **Linux/macOS**: `cp {source} {target}`
    c. Rename the ADR file following pattern: `[YYYY-MM-DD]-[short-descriptive-title].md`
       - Example: `/docs/adr/2025-11-17-api-redesign-solution.md`
    d. Determine the ADR number by checking existing ADR files in `/docs/adr/` and using next sequential number
19. I have to fill the ADR document sections:
    a. Fill ADR number, title, date, and status (Accepted)
    b. Fill **Problem** section - clear 2-3 sentence problem statement from brainstorming document
    c. Fill **Decision** section - what we decided to build, how it addresses problem, and 3 key reasons why
    d. Fill **What to Build (Requirements)** section - core requirements and success criteria from selected solution
    e. Fill **Alternatives Rejected** section - top 3 alternatives with brief one-sentence rejection reasons
    f. Fill **Full brainstorming context** link to the High Mountain plan file
20. Ask Alvi to review the ADR document, and wait for confirmation
21. Present both documents to Alvi:
    a. Full brainstorming document: `/plans/[date]-[project]-[theme]-brainstorm.md`
    b. Decision summary (ADR): `/docs/adr/[date]-[title].md`
22. Inform Alvi that the ADR document should be used as "Related Documents" reference when creating implementation plans with Deep Trench/Shallow Shore/Quick Surf protocols
