# Claude Agent - Planning Procedure

# Wide Ocean Protocol

## When to Use This Protocol
Use Wide Ocean Protocol when a feature requires **3-5 separate sub-plans** that need coordination. This is the "conductor's score" that orchestrates multiple protocol plans (Deep Trench, Shallow Shore, Quick Surf, etc.) into a cohesive feature delivery.

**Use when:**
- ✅ Feature requires 3-5 separate protocol plans
- ✅ Multi-agent coordination is needed
- ✅ Feature-level visibility across multiple plans is required

**Don't use when:**
- ❌ Single plan is sufficient → Use Deep Trench, Shallow Shore, or Quick Surf directly
- ❌ Only brainstorming needed → Use High Mountain or Short Hill directly

---

## Execution Protocol

*IMPORTANT: To execute the protocol, I have to use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited.*

1. I have to find and read the [Wide Ocean Plan Template](//@claude-agents/control-files/plans/wide-ocean-plan-template.md) file
2. I have to create new plan folder in the project root level `/plans` with naming: `plans/[YYYY-MM-DD]-[feature-name]/`
   - Get current date:
     - **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd'"`
     - **Linux/macOS**: `date '+%Y-%m-%d'`
   - Create folder:
     - **Windows**: `powershell -c "New-Item -ItemType Directory -Force -Path 'plans/[YYYY-MM-DD]-[feature-name]'"`
     - **Linux/macOS**: `mkdir -p plans/[YYYY-MM-DD]-[feature-name]`
3. I need to copy the [Wide Ocean Plan Template](//@claude-agents/control-files/plans/wide-ocean-plan-template.md) file to the new folder as `master.md`:
   - **Windows**: `powershell -c "Copy-Item {source} -Destination {target}/master.md -Force"`
   - **Linux/macOS**: `cp {source} {target}/master.md`
4. I have to fill the [Feature Info](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#feature-info) section
5. I have to fill the [Objectives and Success Criteria](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#objectives) section
6. I have to investigate the codebase and fill the [Analysis](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#analysis) section
7. Ask for review of Feature Info, Objectives, and Analysis, and wait for confirmation before moving on to avoid cascading change effect if the sections need to be adjusted
8. I have to fill the [Sub-Plans Listing](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#sub-plans-listing) section
9. Ask for review of Sub-Plans, and wait for confirmation before moving on to avoid cascading change effect if the sections need to be adjusted
10. I have to fill the [Execution Order](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#execution-order) section
11. I have to fill the [Dependency Graph](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#dependency-graph) section
12. Ask for review of Execution Order and Dependency Graph, and wait for confirmation before moving on to avoid cascading change effect if the sections need to be adjusted
13. I have to fill the [Integration Points](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#integration-points) section
14. I have to fill the [Handoff Checklists](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#handoff-checklists) section
15. I have to fill the [Agent Assignment Matrix](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#agent-assignment-matrix) section
16. Ask for review of Integration Points, Handoffs, and Agent Assignment, and wait for confirmation before moving on to avoid cascading change effect if the sections need to be adjusted
17. I have to fill the [Related Documents](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#related-documents) section
18. I have to fill the [Notes & Decisions Log](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#notes--decisions-log) section
19. I have to fill the [Status Tracking](//@claude-agents/control-files/plans/wide-ocean-plan-template.md#status-tracking) section (mirror Sub-Plans with NOT STARTED status)
20. Then, I have to do a self final review for the doc, by thinking critically, very hard and very carefully, as if this is another person's work:
    a. Are all sub-plans necessary? Any missing?
    b. Is the execution order correct? Any dependency issues?
    c. Are handoff checklists complete for each transition?
    d. Are agent assignments appropriate?
    e. Is there anything conflicting or redundant?
21. Present the complete master plan to Alvi with self-review findings, and wait for confirmation
22. After confirmation, the master plan is ready. Sub-plans will be created and executed using their respective protocols (Deep Trench, Shallow Shore, etc.)

---

## Execution Workflow (After Master Plan Approved)

When executing sub-plans:
1. Check STATUS TRACKING for next `NOT STARTED` plan
2. Create sub-plan file using appropriate protocol (Deep Trench, Shallow Shore, etc.)
3. Execute sub-plan using its own protocol
4. After sub-plan completion, update master plan:
   - STATUS TRACKING: Set status to `DONE`, progress to `100%`
   - Complete relevant HANDOFF CHECKLIST
   - Update PHASE SUMMARY if phase complete
5. Repeat until all sub-plans are `DONE`
6. Complete FEATURE COMPLETION CHECKLIST
7. Set Feature Status to `DONE`
