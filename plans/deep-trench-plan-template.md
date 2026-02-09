# Deep Trench Plan Template

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

### 1. **Objective Analysis**
[What does the objective really want? Break down requirements and specifications in detail]

- **Requirement 1**: [Specific requirement analysis]
- **Requirement 2**: [Specific requirement analysis]
- **Specification Details**: [Technical specifications and constraints]

### 2. **Current State Analysis**
[What is our current state? Existing code, systems, capabilities, constraints]

- **Existing Systems**: [Current technology stack and architecture]
- **Current Capabilities**: [What we can do now]
- **Known Limitations**: [Current constraints and bottlenecks]
- **Available Resources**: [Time, tools, knowledge available]

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
### **Technical Design**
[Based on the analysis above, how will we architect the solution? This section has to be very clear and comprehensive, down to what code and what class, what will be added, what will be changed, the flow, the integration between steps, testing, etc. Use of table or mermaid.js for flow. Use of Implementation step is also recommended]

#### **Architecture Overview**
[High-level system design and component interaction]

#### **Component 1: [Feature/Component Name]**
- **Purpose**: [Why this component exists - what problem it solves]
- **Core Responsibility**: [Primary function/role in the system]
- **Key Files/Classes**: [Main code artifacts that will house this component]
  - **New Files**: [List of new files to create with purposes]
  - **Modified Files**: [List of existing files to change and why]
  - **Core Classes/Functions**: [Essential classes and functions for this component]
- **Integration Points**: [How this component connects with other components/systems]
- **Technical Decisions**: [Key architecture choices and rationale]
- **Data Flow**: [How data enters, processes through, and exits this component]

#### **Component 2: [Feature/Component Name]**
- **Purpose**: [Why this component exists - what problem it solves]
- **Core Responsibility**: [Primary function/role in the system]
- **Key Files/Classes**: [Main code artifacts that will house this component]
  - **New Files**: [List of new files to create with purposes]
  - **Modified Files**: [List of existing files to change and why]
  - **Core Classes/Functions**: [Essential classes and functions for this component]
- **Integration Points**: [How this component connects with other components/systems]
- **Technical Decisions**: [Key architecture choices and rationale]
- **Data Flow**: [How data enters, processes through, and exits this component]


#### **System Flow Diagram**
**Current System Flow State**
```mermaid
[Include mermaid.js sequence diagram showing the current state of the system flow and component interactions after the changes]
```
**End Result System Flow State**
```mermaid
[Include mermaid.js sequence diagram showing the end result of the system flow and component interactions after the changes]
```

#### **Integration Architecture**
[Table or diagram showing how all steps integrate together]

| Component | Integrates With | Data Flow | Dependencies |
|-----------|----------------|-----------|--------------|
| [Component 1]  | [Other components] | [Input → Processing → Output] | [Required components] |
| [Component 2]  | [Other components] | [Input → Processing → Output] | [Required components] |

### **Technical Considerations**
[What constraints, limitations, dependencies, and technical challenges need to be considered?]

- **Technical Consideration 1**: [Technical consideration 1]
  - **Subsection 1 Technical Consideration 1**: [Technical consideration 1 subsection 1]
  - **Subsection 2 Technical Consideration 1**: [Technical consideration 1 subsection 2]
- **Technical Consideration 2**: [Technical consideration 2]
  - **Subsection 1 Technical Consideration 2**: [Technical consideration 2 subsection 1]
  - **Subsection 2 Technical Consideration 2**: [Technical consideration 2 subsection 2]
- **Technical Consideration 3**: [Technical consideration 3]

---

## **IMPLEMENTATION PHASES**

### Implement Phase 1: [Implementation Name]
- [ ] **Step 1.1**: [Overview on what step 1.1 is about]
  - **Action**: [Specific action item from the Technical Design for step 1.1]
  - **Dependencies**: [List steps that must complete first, or "None"]
  - **Technical Reference**: [Reference here using [Component Link](#component-1-featurecomponent-name) and which part]
  - **Required Resources**: [Database access, API keys, external services, or "None"]
  - **Implementation**: [What we're going to do]
  - **Testing**: [What test are we going to execute]
  - **Success Criteria**: [Specific measurable outcomes that define completion]

- [ ] **Step 1.2**: [Overview on what step 1.2 is about]
  - **Action**: [Specific action item from the Technical Design for step 1.2]
  - **Dependencies**: [List steps that must complete first, or "None"]
  - **Technical Reference**: [Reference here using [Component Link](#component-1-featurecomponent-name) and which part]
  - **Required Resources**: [Database access, API keys, external services, or "None"]
  - **Implementation**: [What we're going to do]
  - **Testing**: [What test are we going to execute]
  - **Success Criteria**: [Specific measurable outcomes that define completion]

### Implement Phase 2: [Implementation Name]
- [ ] **Step 2.1**: [Overview on what step 2.1 is about]
  - **Action**: [Specific action item from the Technical Design for step 2.1]
  - **Dependencies**: [List steps that must complete first, or "None"]
  - **Technical Reference**: [Reference here using [Component Link](#component-1-featurecomponent-name) and which part]
  - **Required Resources**: [Database access, API keys, external services, or "None"]
  - **Implementation**: [What we're going to do]
  - **Testing**: [What test are we going to execute]
  - **Success Criteria**: [Specific measurable outcomes that define completion]

- [ ] **Step 2.2**: [Overview on what step 2.2 is about]
  - **Action**: [Specific action item from the Technical Design for step 2.2]
  - **Dependencies**: [List steps that must complete first, or "None"]
  - **Technical Reference**: [Reference here using [Component Link](#component-1-featurecomponent-name) and which part]
  - **Required Resources**: [Database access, API keys, external services, or "None"]
  - **Implementation**: [What we're going to do]
  - **Testing**: [What test are we going to execute]
  - **Success Criteria**: [Specific measurable outcomes that define completion]

...{next implementation phase and step goes on}...

---