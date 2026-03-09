# Wide Ocean Plan Template

> **Protocol Purpose**: Wide Ocean is a **coordination layer** that orchestrates 3-5 separate protocol plans into a cohesive feature delivery. This is the "conductor's score" - it tracks status, defines execution order, and manages handoffs between sub-plans.
>
> **How to Use**:
> 1. Fill this master plan to define the overall feature scope and sub-plans
> 2. Execute each sub-plan using its own protocol (High Wizard, Quick Wizard)
> 3. Return here after each sub-plan to update status and proceed to the next
>
> **When to Use**: Feature requires 3-5 sub-plans, multi-agent coordination needed, feature-level visibility required
>
> **When NOT to Use**: Single plan sufficient → use High Wizard or Quick Wizard directly

---

## **FEATURE INFO**

> **How to fill**: Basic metadata about this feature coordination effort.

- **Project**: [Project name]
- **Date Created**: [YYYY-MM-DD]
- **Last Updated**: [YYYY-MM-DD HH:MM]
- **Coordinating Agent**: [Agent name creating this master plan]
- **Feature Theme**: [Brief description of what this feature accomplishes]
- **Feature Folder**: `plans/[YYYY-MM-DD]-[feature-name]/`

---

## **OBJECTIVES**

> **How to fill**: Clear statement of what the complete feature achieves when ALL sub-plans are done. Be specific about the end-user or system capability being delivered.

[Write 2-4 sentences describing the feature objective]

### **SUCCESS CRITERIA** (Feature-Level)

> **How to fill**: Checklist that must ALL be true when the feature is complete. Include both standard criteria and feature-specific ones.

- [ ] **Feature Complete**: All sub-plans marked DONE in Status Tracking table
- [ ] **Integration Verified**: All handoff checklists completed successfully
- [ ] **Quality Assured**: All sub-plan success criteria met
- [ ] [Feature-specific criterion 1]
- [ ] [Feature-specific criterion 2]
- [ ] **Tests Passing**: All tests from all sub-plans passing

---

## **ANALYSIS**

> **How to fill**: BEFORE planning sub-plans, investigate what already exists. Search the codebase for existing APIs, components, or related code. Document findings here to inform your sub-plan strategy.

### Current State

> **How to fill**: List each relevant component and its status. This prevents planning work that's already done.

| Component | Status | Notes |
|-----------|--------|-------|
| [Component 1] | [Exists / Missing / Partial] | [What exists, what's missing] |
| [Component 2] | [Exists / Missing / Partial] | [Details] |

### Key Findings

> **How to fill**: Bullet points of important discoveries from your investigation. What works? What needs modification? What patterns can you reuse?

- [Finding 1]
- [Finding 2]
- [Finding 3]

### Strategy Decision

> **How to fill**: Based on your analysis, state the chosen approach. E.g., "Create new admin controller" vs "Modify existing endpoints".

Based on analysis: [Brief statement of approach]

---

## **SUB-PLANS LISTING**

> **How to fill**: List 3-5 sub-plans that make up this feature. Each will be executed using its own protocol.
>
> **Protocol Types**:
> - **File-based planning**: High Wizard (any complexity — dynamically adapts sections based on task context)
> - **Direct execution**: Quick Wizard (lightweight tasks — decision collection + direct execution)

| # | Plan Name | Protocol Type | Description | File Path |
|---|-----------|---------------|-------------|-----------|
| 1 | [Plan Name] | [Protocol] | [What this plan accomplishes] | `[plan-name.md]` |
| 2 | [Plan Name] | [Protocol] | [Description] | `[plan-name.md]` |
| 3 | [Plan Name] | [Protocol] | [Description] | `[plan-name.md]` |

*Add more rows as needed (typical: 3-5 sub-plans)*

---

## **EXECUTION ORDER**

> **How to fill**: Define which plans can start when. Identify dependencies between plans.

### Execution Sequence

> **How to fill**: Number the plans in execution order. Specify what must be complete before each can start.

| Order | Plan Name | Can Start When | Blocking For |
|-------|-----------|----------------|--------------|
| 1 | [Plan 1] | Immediately | [Plans that depend on this] |
| 2 | [Plan 2] | Plan 1 DONE | [Plans that depend on this] |
| 3 | [Plan 3] | Plan 2 DONE | None (final) |

*Adjust rows to match your actual sub-plans*

### Parallel Execution Opportunities

> **How to fill**: Identify plans that can run simultaneously (no dependencies between them). If none, state "Sequential execution required".

- **Parallel Group 1**: [Plans that can run together] - [Why they're independent]
- Or: **No Parallel Groups** - Sequential execution required

---

## **DEPENDENCY GRAPH**

> **How to fill**: Create a mermaid diagram showing plan dependencies. Adjust node names and arrows to match your actual plans.

```mermaid
graph LR
    subgraph "Phase 1: [Name]"
        A[Plan 1: [Name]]
    end

    subgraph "Phase 2: [Name]"
        B[Plan 2: [Name]]
    end

    A --> B

    style A fill:#fff3e0
    style B fill:#fff3e0
```

*Customize: Add/remove nodes, adjust arrows based on actual dependencies*

### Dependency Validation Checklist

> **How to fill**: Verify your dependency graph is valid before proceeding.

- [ ] **No Circular Dependencies**: No plan depends on itself or creates a cycle
- [ ] **All Plans Connected**: Every plan is reachable from starting plan(s)
- [ ] **Clear Starting Point**: At least one plan has no incoming dependencies
- [ ] **Clear End Point**: At least one plan has no outgoing dependencies
- [ ] **Parallel Opportunities Identified**: Plans that can run simultaneously are noted

### Critical Path

> **How to fill**: Identify the longest path through dependencies - this determines minimum completion time.

1. **Critical Path**: [Plan X → Plan Y → Plan Z]
2. **Bottleneck Plans**: [Plans that, if delayed, delay the entire feature]

---

## **INTEGRATION POINTS**

> **How to fill**: Document how sub-plans connect. What does each plan hand off to the next? Define contract files that producers create and consumers read.

### Contract Files

> **How to fill**: List contract files that serve as handoff artifacts between plans. Store in `contracts/` subfolder.

| Contract | Producer | Consumer | Path |
|----------|----------|----------|------|
| [Contract Name] | [Plan #] | [Plan #] | `contracts/[contract-name].yml` |

**Contract Location**: `plans/[YYYY-MM-DD]-[feature-name]/contracts/`

### Plan Transition Overview

| From Plan | To Plan | Handoff Type | Key Deliverables | Verification Method |
|-----------|---------|--------------|------------------|---------------------|
| [Plan 1] | [Plan 2] | [Type: API Contract/Schema/Docs] | [Contract file path] | [How to verify] |

*Add rows for each transition in your execution sequence*

---

## **HANDOFF CHECKLISTS**

> **How to fill**: Create one checklist per plan transition. These ensure clean handoffs between plans.

### Handoff: [Plan X] → [Plan Y]
**From**: [Source Plan Name]
**To**: [Target Plan Name]

#### Outputs from [Source Plan] (Must be complete):
> **How to fill**: What must the source plan deliver?

- [ ] [Key deliverable 1]
- [ ] [Key deliverable 2]
- [ ] Build successful / Tests passing

#### Inputs needed by [Target Plan] (Must be available):
> **How to fill**: What does the target plan need to start?

- [ ] [Required resource/access 1]
- [ ] [Required resource/access 2]

#### Verification Steps:
> **How to fill**: How do we confirm the handoff is complete?

- [ ] [Target plan] agent has reviewed deliverables
- [ ] No blocking issues remaining

---

*Copy and customize handoff section for each plan transition*

---

## **AGENT ASSIGNMENT MATRIX**

> **How to fill**: Assign an agent to each sub-plan. Consider agent expertise (Backend-NestJS for APIs, Frontend-React for UI, etc.)

### Agent Assignments

| Plan # | Plan Name | Assigned Agent | Role | Status | Notes |
|--------|-----------|----------------|------|--------|-------|
| 1 | [Plan 1] | [Agent Name] | Lead | Available | [Notes] |
| 2 | [Plan 2] | [Agent Name] | Lead | Available | [Notes] |
| 3 | [Plan 3] | [Agent Name] | Lead | Available | [Notes] |

*Mirror rows from SUB-PLANS LISTING*

### Coordination Strategy

> **How to fill**: Choose ONE strategy and mark it selected.

**Option A: Sequential Single Agent** (Simplest)
- [ ] Selected
- One agent executes all sub-plans in sequence
- Best for: Smaller features, tight integration needs

**Option B: Parallel Different Agents** (Fastest)
- [ ] Selected
- Different specialized agents work on different sub-plans simultaneously
- Best for: Larger features, independent components

**Option C: Cloned Same Agent** (Balanced)
- [ ] Selected
- Same agent cloned for parallel work on independent sub-plans
- Best for: Medium features, when consistency matters

---

### Multi-Agent Synchronization

> **How to fill**: If using parallel agents, define sync points where agents must align before proceeding.

#### Sync Point 1: [After Plan X]
- **When**: [Trigger condition]
- **Purpose**: [Why sync is needed]
- **Action**: [What agents must do]
- **Verification**: [ ] [How to confirm sync complete]

#### Sync Point 2: Feature Completion
- **When**: All plans complete
- **Purpose**: Confirm feature is ready for release
- **Action**: Coordinating agent reviews all success criteria
- **Verification**: [ ] All feature-level success criteria met

*Customize sync points based on your plan transitions*

---

## **RELATED DOCUMENTS**

> **How to fill**: Central reference for all documents related to this feature.

### Design Documents

| Document | Purpose | Link |
|----------|---------|------|
| [Document Name] | [What it defines] | `[path]` |

### Sub-Plan Files

> **How to fill**: Links to each sub-plan file. Fill as sub-plans are created.

| Plan # | Plan Name | Protocol | Plan File | Log File |
|--------|-----------|----------|-----------|----------|
| 1 | [Plan Name] | [Protocol] | `[plan-name.md]` | `[plan-name-log.md]` |
| 2 | [Plan Name] | [Protocol] | `[plan-name.md]` | `[plan-name-log.md]` |

*Mirror rows from SUB-PLANS LISTING*

### External References

| Reference | Type | Purpose | Link |
|-----------|------|---------|------|
| [Reference Name] | [Docs/API/Tool] | [Why relevant] | `[URL or path]` |

---

## **NOTES & DECISIONS LOG**

> **How to fill**: Track important decisions, changes, and notes throughout the feature lifecycle. Add rows as decisions are made.

| Date | Decision/Note | Made By | Impact | Related Plans |
|------|---------------|---------|--------|---------------|
| [YYYY-MM-DD] | [Description] | [Agent/User] | [High/Medium/Low] | [Plan #s] |

---

## **STATUS TRACKING**

> **How to fill**: Mirror the sub-plans from SUB-PLANS LISTING. All start as NOT STARTED. Update this table after completing each sub-plan during execution.
>
> **Status values**: `NOT STARTED` → `IN PROGRESS` → `DONE` (or `BLOCKED` if waiting)
>
> **Progress guidelines**: 0% (not started), 25% (planning done), 50% (implementation in progress), 75% (testing), 100% (complete)

| Plan Name | Protocol Type | Status | Agent | Progress % | Started | Completed |
|-----------|---------------|--------|-------|------------|---------|-----------|
| [Plan 1] | [Type] | NOT STARTED | [Agent] | 0% | - | - |
| [Plan 2] | [Type] | NOT STARTED | [Agent] | 0% | - | - |
| [Plan 3] | [Type] | NOT STARTED | [Agent] | 0% | - | - |

*Mirror rows from SUB-PLANS LISTING above*

---

## **FEATURE COMPLETION CHECKLIST**

> **How to fill**: Final checklist before marking feature complete. All must be checked.

- [ ] All sub-plans marked DONE in Status Tracking table
- [ ] All handoff checklists completed
- [ ] All Phase Summary shows DONE for all phases
- [ ] All feature-level success criteria met
- [ ] All sync points verified (if multi-agent)
- [ ] All documentation updated
- [ ] All tests passing
- [ ] Feature ready for release

**Feature Status**: [NOT STARTED / IN PROGRESS / DONE]
**Last Updated**: [YYYY-MM-DD HH:MM]
**Updated By**: [Agent Name]

---
