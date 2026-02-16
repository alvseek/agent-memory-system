# High Wizard Plan

## **PROJECT INFO**
- **Project**: [Project Name]
- **Date**: [YYYY-MM-DD]
- **Agent**: [Agent Name]
- **Theme**: [Brief description of what we're building]

---

## **OBJECTIVES**
[Clear, concise statement of what we want to achieve]

### **Related Documents**
[Link to related documentation, requirements, or design files if they exist, or write "None"]
- [Document 1](path/to/document1.md) - Brief description

### **SUCCESS CRITERIA**
- [ ] [Primary goal achieved]
- [ ] [Quality/testing requirements met]
- [ ] [Integration requirements met]
- [ ] [Documentation updated if needed]

---

## **SCOPE**

### In Scope
- [Specific deliverable or feature]
- [Specific deliverable or feature]

### Out of Scope
- [Explicitly excluded item and why]
- [Future consideration for later]

---

## **CONFIRMED DECISIONS**
*These decisions were collected during investigation and confirmed by Alvi. The reasons serve as the analysis record.*

| # | Decision | Chosen | Reason |
|---|----------|--------|--------|
| 1 | [Decision topic] | [Chosen option] | [Evidence-based reason] |
| 2 | [Decision topic] | [Chosen option] | [Evidence-based reason] |

---

## **SOLUTION**

### Architecture Overview
[High-level system design and component interaction, built from confirmed decisions]

### Component 1: [Name]
- **Purpose**: [What problem it solves]
- **Key Files**: [Files to create/modify]

### Component 2: [Name]
- **Purpose**: [What problem it solves]
- **Key Files**: [Files to create/modify]

```mermaid
[System flow diagram if applicable]
```

---

## **IMPLEMENTATION PHASES**

### Phase 1: [Name]
- [ ] **Step 1.1**: [Overview]
  - **Action**: [What to do]
  - **Implementation**: [How to do it]
  - **Testing**: [How to verify]
  - **Success Criteria**: [When it's done]

- [ ] **Step 1.2**: [Overview]
  - **Action**: [What to do]
  - **Implementation**: [How to do it]
  - **Testing**: [How to verify]
  - **Success Criteria**: [When it's done]

### Phase 2: [Name]
- [ ] **Step 2.1**: [Overview]
  - **Action**: [What to do]
  - **Implementation**: [How to do it]
  - **Testing**: [How to verify]
  - **Success Criteria**: [When it's done]

...{next phases and steps as needed}...

---

## **EXECUTION LOG**
**Execution Protocol for AI**:
I have to use this document as my **ONLY** source of truth to execute and track the plan steps iteratively. I should **NOT** use additional tools like ToDos because it lacks the context of what should I do. Everytime I want to implement a step I have to check the reference to the original step plan above. Everytime a step has been finished I need to go back to this document to log what was done.
*In other words*:
- I have to make this document as the source of truth for the implementation phase on what I have worked on and what I will be working
- The original plan must be fully in my context, therefore, I have to make sure I loaded the **Plan File** before executing any task and read carefully the reference to the original step
- I have to do the implementation by doing it in order per step THEN, I ALWAYS have to fill the step log rightly after

**Definition of Done (applies to ALL steps)**:
- ✅ **Code Quality**: Code compiles/runs without errors
- ✅ **Testing**: Tests written and passing
- ✅ **Logged**: Implementation and testing logged below
- 🚫 **Blocked**: Get input from Alvi before assuming

### Phase 1:
- [ ] **Step 1.1**: [link to step above]
  - **Implementation Log**: [What was done]
  - **Testing Log**: [What was tested and results]
  - **Success Criteria**: [Pass/Fail against step's success criteria]
  - **Tech Debts**: [Optional - any shortcuts, TODOs, or future improvements noted]
  - **Result**: [Outcome compared to success criteria]

- [ ] **Step 1.2**: [link to step above]
  - **Implementation Log**: [What was done]
  - **Testing Log**: [What was tested and results]
  - **Success Criteria**: [Pass/Fail against step's success criteria]
  - **Tech Debts**: [Optional - any shortcuts, TODOs, or future improvements noted]
  - **Result**: [Outcome compared to success criteria]

### Phase 2:
- [ ] **Step 2.1**: [link to step above]
  - **Implementation Log**: [What was done]
  - **Testing Log**: [What was tested and results]
  - **Success Criteria**: [Pass/Fail against step's success criteria]
  - **Tech Debts**: [Optional - any shortcuts, TODOs, or future improvements noted]
  - **Result**: [Outcome compared to success criteria]

...{next phases as needed}...

---

## **POST-COMPLETION**
After all phases are executed and logged, move this plan to `plans/completed/`:
- **Windows**: `powershell -c "if (!(Test-Path './plans/completed')) { New-Item -ItemType Directory -Path './plans/completed' -Force }; Move-Item './plans/[this-file].md' './plans/completed/[this-file].md' -Force"`
- **Linux/macOS**: `mkdir -p ./plans/completed && mv ./plans/[this-file].md ./plans/completed/[this-file].md`
