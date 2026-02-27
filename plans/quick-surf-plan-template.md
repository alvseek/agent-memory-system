# Quick Surf Plan Template

**Critical Protocol for AI - 1 LEVEL DEEP LOADING**: When using this template, I MUST load all documents listed in the "Related Documents" section to have complete context when planning and executing. This ensures proper understanding of requirements, constraints, and existing work.**

## **PROJECT INFO**
- **Project**: [Project Name]
- **Date**: [YYYY-MM-DD]
- **Agent**: [Agent Name]
- **Theme**: [Brief description of what we're building]

---

## **OBJECTIVES**
[Clear, concise statement of what we want to achieve]

### **Related Documents**: [Link to related documentation, requirements, or design files if they exist, or write "None" if no related documents]
- [Document 1](path/to/document1.md) - Brief description
- [Document 2](path/to/document2.md) - Brief description

### **SUCCESS CRITERIA**
- [ ] **Primary Goal**: [Main objective achieved]
- [ ] **Quality Check**: [Code quality/testing requirements met]
- [ ] **Integration**: [Successfully integrates with existing system]
- [ ] **Documentation**: [Necessary documentation updated]

---

## **ANALYSIS**

### 1. **Current State Analysis**
[What is our current state? Existing code, systems, capabilities, constraints. I have to scan the project to make sure the existing system is presented well in the plan]

- **Existing Systems**: [Current technology stack and architecture]
- **Current Capabilities**: [What we can do now]

### 3. **Scope Decision**
[What we will do and explicitly what we will NOT do - clear boundaries]

#### **In Scope (What We Will Do):**
- **Scope Item 1**: [Specific deliverable or feature]
- **Scope Item 2**: [Specific deliverable or feature]
- **Scope Item 3**: [Specific deliverable or feature]

#### **Out of Scope (What We Will NOT Do):**
- **Out of Scope Item 1**: [Explicitly excluded item and why]
- **Out of Scope Item 2**: [Explicitly excluded item and why]
- **Future Considerations**: [Items for later phases]

---

## **SOLUTION**
#### **Architecture Overview**
[High-level system design and component interaction]

#### **Component 1: [Feature/Component Name]**
- **Purpose**: [Why this component exists - what problem it solves]
- **Core Responsibility**: [Primary function/role in the system]
- **Key Files/Classes**: [Main code artifacts that will house this component]
- **Integration Points**: [How this component connects with other components/systems]
- **Technical Decisions**: [Key architecture choices and rationale]
- **Data Flow**: [How data enters, processes through, and exits this component]

#### **Component 2: [Feature/Component Name]**
- **Purpose**: [Why this component exists - what problem it solves]
- **Core Responsibility**: [Primary function/role in the system]
- **Key Files/Classes**: [Main code artifacts that will house this component]
- **Integration Points**: [How this component connects with other components/systems]
- **Technical Decisions**: [Key architecture choices and rationale]
- **Data Flow**: [How data enters, processes through, and exits this component]

**End Result System Flow State**
```mermaid
[Include mermaid.js sequence diagram showing the end result of the system flow and component interactions after the changes]
```

---

## **IMPLEMENTATION PHASES**

### Implement Phase 1: [Implementation Name]
- [ ] **Step 1.1**: [Overview on what step 1.1 is about]
  - **Action**: [Specific action item from the Technical Design for step 1.1]
  - **Dependencies**: [List steps that must complete first, or "None"]
  - **Technical Reference**: [Reference here using [Component Link](#component-1-featurecomponent-name) and which part]
  - **Implementation**: [What we're going to do]
  - **Testing**: [What test are we going to execute]
  - **Success Criteria**: [Specific measurable outcomes that define completion]

- [ ] **Step 1.2**: [Overview on what step 1.2 is about]
  - **Action**: [Specific action item from the Technical Design for step 1.2]
  - **Dependencies**: [List steps that must complete first, or "None"]
  - **Technical Reference**: [Reference here using [Component Link](#component-1-featurecomponent-name) and which part]
  - **Implementation**: [What we're going to do]
  - **Testing**: [What test are we going to execute]
  - **Success Criteria**: [Specific measurable outcomes that define completion]

### Implement Phase 2: [Implementation Name]
- [ ] **Step 2.1**: [Overview on what step 2.1 is about]
  - **Action**: [Specific action item from the Technical Design for step 2.1]
  - **Dependencies**: [List steps that must complete first, or "None"]
  - **Technical Reference**: [Reference here using [Component Link](#component-1-featurecomponent-name) and which part]
  - **Implementation**: [What we're going to do]
  - **Testing**: [What test are we going to execute]
  - **Success Criteria**: [Specific measurable outcomes that define completion]

- [ ] **Step 2.2**: [Overview on what step 2.2 is about]
  - **Action**: [Specific action item from the Technical Design for step 2.2]
  - **Dependencies**: [List steps that must complete first, or "None"]
  - **Technical Reference**: [Reference here using [Component Link](#component-1-featurecomponent-name) and which part]
  - **Implementation**: [What we're going to do]
  - **Testing**: [What test are we going to execute]
  - **Success Criteria**: [Specific measurable outcomes that define completion]

...{next implementation phase and step goes on}...

---

## **IMPLEMENTATION PHASES EXECUTION LOG**
**Execution Protocol for AI**:
I have to use this document as my **ONLY** source of truth to execute and track the plan steps iteratively. I should **NOT** use additional tools like ToDos because it lacks the context of what should I do. Because this file serves also as implementation phase log, everytime I want to implement a step I have to check the link to the original step plan. Everytime a sub step has been finished I need to go back to this document to make sure what have been done is logged properly by filling the step log place holder, and to make sure the next step also have the proper context.
*In other words*:
- I have to make this document as the source of truth for the implementation phase on what I have worked on and what I will be working
- As this file is only the implementation phase log, the original plan must be fully in my context, therefore, I have to make sure I loaded the **Plan File** before executing any task and read carefully the reference to the original step
- I have to do the implementation by doing it in order per step THEN, I ALWAYS have to fill the step log rightly after

**Definition of Done (Universal Quality Standards - applies to ALL steps)**:
- ✅ **Code Quality**: Code compiles/runs without errors or warnings
- ✅ **Testing**: All tests written and passing (unit, integration as applicable)
- ✅ **Logged**: Both Implementation Log and Testing Log has been filled
- 🚫 *Notes**: When found a substep that results in 🚫, I need to get an input confirmation to [USER-NAME] on what to do so I won't assume things and get lost

### Implement Phase 1:
- [ ] **Step 1.1**: {add reference to the original Step 1.1 plan section using anchor link}

  - **Implementation Log**: [Insert below]
  - **Testing Log**: [Insert below using]
  - **Tech Debts Summary**: [Summary of produced and found TODOs / tech debts by this step]
  - **Result**: [Complete result on what we have done]
  - **Success Criteria Result**: [The result based on sub step success criteria from the plan]

- [ ] **Step 1.2**: {add reference to the original Step 1.2 plan section using anchor link}

  - **Implementation Log**: [Insert below]
  - **Testing Log**: [Insert below using]
  - **Tech Debts Summary**: [Summary of produced and found TODOs / tech debts by this step]
  - **Result**: [Complete result on what we have done]
  - **Success Criteria Result**: [The result based on sub step success criteria from the plan]

### Implement Phase 2:
- [ ] **Step 2.1**: {add reference to the original Step 2.1 plan section using anchor link}

  - **Implementation Log**: [Insert below]
  - **Testing Log**: [Insert below using]
  - **Tech Debts Summary**: [Summary of produced and found TODOs / tech debts by this step]
  - **Result**: [Complete result on what we have done]
  - **Success Criteria Result**: [The result based on sub step success criteria from the plan]

- [ ] **Step 2.2**: {add reference to the original Step 1.1 plan section using anchor link}

  - **Implementation Log**: [Insert below]
  - **Testing Log**: [Insert below using]
  - **Tech Debts Summary**: [Summary of produced and found TODOs / tech debts by this step]
  - **Result**: [Complete result on what we have done]
  - **Success Criteria Result**: [The result based on sub step success criteria from the plan]
s
...{next implementation phase and step  goes on}...

---