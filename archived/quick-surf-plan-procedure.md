# Claude Agent - Quick Surf Protocol Procedure

## Instruction for Agent
*IMPORTANT: To execute the protocol, I have to use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*
1. I have to find and read the [Quick Surf Plan Template](//@claude-agents/control-files/plans/quick-surf-plan-template.md) file
2. I have to create new plan folder in the project root level `/plans` (if it doesn't exist)
3. I need to copy the [Quick Surf Plan Template](//@claude-agents/control-files/plans/quick-surf-plan-template.md) file to the `/plans` folder:
   - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
   - **Linux/macOS**: `cp {source} {target}`
4. I have to check the current date using:
   - **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
   - **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`
5. I have to rename the new copy pasted file to `[YYYY-MM-DD]-[project]-[theme].md` name pattern
6. I have to fill the [Project Info](//@claude-agents/control-files/plans/quick-surf-plan-template.md#project-info) + [Objective and Success Criteria](//@claude-agents/control-files/plans/quick-surf-plan-template.md#-objective) + [Analysis](//@claude-agents/control-files/plans/quick-surf-plan-template.md#analysis) + [Solution](//@claude-agents/control-files/plans/quick-surf-plan-template.md#solution) sections
7. Ask the project info, objective, analysis, and solution sections for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
8. I have to fill the  [Implementation Phases](//@claude-agents/control-files/plans/quick-surf-plan-template.md#implementation-phases) sections
9. Ask the implementation phase section for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
10. Then, I have to do a self final review for the doc, by thinking critically, very hard and very carefully, as if this is another person's work (this step is very important):
    a. Is there anything missing that should be in scope?
    b. Is there anything in implementation that actually should be out of scope?
    c. Is there anything that needs to be detailed further to avoid confusion?
    d. Is there anything that is conflicting within the plan?
    e. Is there anything that is redundant in the plan?
    f. Is there anything in implementation phase that is not in order and should be reorder?
11. Present the self final review to Alvi, and wait for confirmation before moving on to step 10-15 which are creating the log file
13. Next, I have to fill the {add reference to the original Step *.* plan section using anchor link} placeholder for each of the substep
14. Then, I have to present the Implementation Log file link to Alvi and wait for the instruction
15. After Alvi instructs to start implementing, then I can start to implement the implementation phase following on the **Execution Protocol for AI** from the newly created plan file
