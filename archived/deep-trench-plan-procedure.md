# Claude Agent - Deep Trench Protocol Procedure

## Instruction for Agent
*IMPORTANT: To execute the protocol, I have to use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*
1. I have to find and read the [Deep Trench Plan Template](//@claude-agents/control-files/plans/deep-trench-plan-template.md) file
2. I have to create new plan folder in the project root level `/plans`
3. I need to copy the [Deep Trench Plan Template](//@claude-agents/control-files/plans/deep-trench-plan-template.md) file to the new folder I just created in step 2:
   - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
   - **Linux/macOS**: `cp {source} {target}`
4. I have to check the current date using:
   - **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
   - **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`
5. I have to rename the new copy pasted file to `[YYYY-MM-DD]-[project]-[theme].md` name pattern
6. I have to fill the [Project Info](//@claude-agents/control-files/plans/deep-trench-plan-template.md#project-info) + [Objective and Success Criteria](//@claude-agents/control-files/plans/deep-trench-plan-template.md#-objective) sections
7. Ask the project info and objecive for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
8. I have to fill the [Analysis](//@claude-agents/control-files/plans/deep-trench-plan-template.md#analysis) section
9. Ask the analysis for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
10. I have to fill the [Solution](//@claude-agents/control-files/plans/deep-trench-plan-template.md#solution) sections
11. Ask the solution for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
12. I have to fill the [Implementation Phases](//@claude-agents/control-files/plans/deep-trench-plan-template.md#implementation-phases) section
13. Ask the implementation phase for review, and wait for confirmation before moving on to avoid cascading change effect if the section need to be adjusted
14. Then, I have to do a self final review for the doc, by thinking critically, very hard and very carefully, as if this is another person's work (this step is very important):
    a. Is there anything missing that should be in scope?
    b. Is there anything that is actually should be out of scope?
    c. Is there anything that needs to be detailed further to avoid confusion?
    d. Is there anything that is conflicting within the plan?
    e. Is there anything that is redundant in the plan?
    f. Is there anything in implementation phase that is not in order and should be reorder?
15. Present the self final review to Alvi, and wait for confirmation
16. Now, I have to copy the [Implementation Log Template](//@claude-agents/control-files/plans/implementation-log-template.md) file to the `/plans` folder in the project root level, named like the plan file name in step 5, but added '-log' as the name:
    - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
    - **Linux/macOS**: `cp {source} {target}`
    - example of Plan File: name /plans/2025-10-06-ocx-new-catalog-feature.md
    - example of Implementation Log file name: /plans/2025-10-06-ocx-new-catalog-feature-log.md.
17. I have to fill the **Plan File** placeholder with the original plan file anchor link for the newly created implementation log file
18. I have to choose the [Deep Trench Log Placeholder](//@claude-agents/control-files/plans/deep-trench-log-placeholder.md) in the **Execution Protocol for AI** section and remove the others
19. I also have to fill the {add reference to the original Step *.* plan section using anchor link} placeholder for each of the substep
20. Then, I have to present the Implementation Log file link to Alvi and wait for the instruction
21. After Alvi instructs to start implementing, then I can start to implement the implementation phase following on the **Execution Protocol for AI** in the newly created Implementation Log file