# Claude Agent - Patching Ship Planning Procedure

# Patching Ship Protocol

## When to Use This Protocol
Use Patching Ship Protocol when you need **systematic bug investigation and root cause analysis** through **structured debugging workflow**. This protocol helps you analyze bugs comprehensively using platform scaffolding checks, issue replication, root cause investigation, and solution synthesis.

**Perfect for:**
- Production bugs requiring thorough investigation
- Issues needing systematic debugging and root cause analysis
- Problems that need reproducible test cases
- Bugs requiring platform diagnostics (logs, database, monitoring)
- Complex issues needing structured fix approach evaluation

*IMPORTANT: To execute the protocol, I have to use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*

1. I have to find and read the [Patching Ship Plan Template](//@claude-agents/control-files/plans/patching-ship-plan-template.md) file
2. I have to create new plan folder in the project root level `/plans` (if it doesn't exist)
3. I need to copy the [Patching Ship Plan Template](//@claude-agents/control-files/plans/patching-ship-plan-template.md) file to the `/plans` folder:
   - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
   - **Linux/macOS**: `cp {source} {target}`
4. I have to check the current date using:
   - **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
   - **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`
5. I have to rename the new copy pasted file to `[YYYY-MM-DD]-[project]-[bug-theme]-debug.md` name pattern
6. I have to fill the [Project Info](//@claude-agents/control-files/plans/patching-ship-plan-template.md#project-info) + [Bug Analysis & Context](//@claude-agents/control-files/plans/patching-ship-plan-template.md#bug-analysis--context) sections
7. Ask the project info and bug analysis for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
8. I have to fill the [Platform Scaffolding Check](//@claude-agents/control-files/plans/patching-ship-plan-template.md#platform-scaffolding-check) section including verification of log locations, debug logging capabilities, database access, monitoring tools, and diagnostic access
9. Ask the platform scaffolding check results for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
10. I have to fill the [Issue Replication](//@claude-agents/control-files/plans/patching-ship-plan-template.md#issue-replication) section with detailed reproduction steps, test environment setup, success criteria for reproduction, and edge case identification
11. Ask the issue replication details for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
12. I have to fill the [Bug Location](//@claude-agents/control-files/plans/patching-ship-plan-template.md#bug-location) section - identify the ACTUAL code producing the bug symptom (factual based on stack traces, logs, or debugger - NOT a guess)
13. Ask the bug location findings for review, and wait for confirmation before moving on
14. I have to fill the [Root Cause Investigation](//@claude-agents/control-files/plans/patching-ship-plan-template.md#root-cause-investigation) section using the hypothesis-driven process:
    - Fill Log Analysis, Code Flow Analysis, and Database State Examination first (data gathering)
    - Then fill [Hypothesis & Testing](//@claude-agents/control-files/plans/patching-ship-plan-template.md#4-hypothesis--testing) section SEQUENTIALLY:
      - Create Hypothesis 1 → Test it → Confirmed? → Fill Root Cause Conclusion / Rejected? → Create Hypothesis 2
      - Repeat until hypothesis confirmed
    - Fill [Root Cause Conclusion](//@claude-agents/control-files/plans/patching-ship-plan-template.md#root-cause-conclusion) ONLY after a hypothesis is confirmed
15. Ask the root cause investigation findings for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
16. I have to fill the [Solution Synthesis](//@claude-agents/control-files/plans/patching-ship-plan-template.md#solution-synthesis) section evaluating fix approach options (quick patch vs proper fix), risk assessment, testing strategy, and rollback plan
17. Ask the solution synthesis evaluation for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
18. I have to fill the [Selected Fix](//@claude-agents/control-files/plans/patching-ship-plan-template.md#selected-fix) section with clear rationale, technical implementation details, and implementation phases
19. Ask the selected fix for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
20. Then, I have to do a self final review for the doc, by thinking critically, very hard and very carefully, as if this is another person's work (this step is very important):
    a. Is the bug clearly described with impact assessment?
    b. Did we verify all platform scaffolding is accessible (logs, debug, database)?
    c. Can we reliably reproduce the issue with documented steps?
    d. Did we identify the ACTUAL bug location (factual, not a guess)?
    e. Did we test hypotheses sequentially before declaring root cause?
    f. Is the root cause confirmed by evidence from hypothesis testing (not assumed)?
    g. Did we evaluate multiple fix approaches with proper risk assessment?
    h. Is the selected fix justified with clear rationale and rollback plan?
    i. Are implementation phases clear and executable?
21. Present the self final review to Alvi, and wait for final confirmation
22. Present the completed bug investigation and fix plan document to Alvi: `/plans/[date]-[project]-[bug-theme]-debug.md`
