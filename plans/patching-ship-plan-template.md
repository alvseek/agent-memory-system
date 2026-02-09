# Patching Ship Plan Template

**Critical Protocol for AI - 1 LEVEL DEEP LOADING**: When using this template, I MUST load all documents listed in the "Related Documents" section to have complete context when investigating and fixing bugs. This ensures proper understanding of the system, previous fixes, and existing constraints.**

## **PROJECT INFO**
- **Project**: [Project Name]
- **Bug ID**: [Ticket/Issue ID if available]
- **Date**: [YYYY-MM-DD]
- **Agent**: [Agent Name]
- **Theme**: [Brief description of the bug we're investigating]

---

## **BUG ANALYSIS & CONTEXT**

### **Problem Description**
[Clear, detailed description of the bug - what is breaking, what is the expected vs actual behavior]

### **Related Documents**: [Link to related documentation, previous bug fixes, or system architecture if they exist, or write "None" if no related documents]
- [Document 1](path/to/document1.md) - Brief description
- [Document 2](path/to/document2.md) - Brief description

### **Impact Assessment**
- **Severity**: [Critical/High/Medium/Low]
- **Affected Users**: [Who is impacted - all users, specific segment, admin only, etc.]
- **Affected Features**: [Which features or modules are broken]
- **Business Impact**: [Revenue loss, user experience degradation, security risk, etc.]
- **Frequency**: [Always occurs, intermittent, rare edge case]

### **Environment Details**
- **Platform**: [Web/Mobile/Desktop/Backend Service]
- **Environment**: [Production/Staging/Development]
- **Version**: [Application version where bug occurs]
- **Operating System**: [If relevant - Windows/Linux/macOS/iOS/Android]
- **Browser/Client**: [If relevant - Chrome/Firefox/Safari/Mobile App]
- **Database**: [Database type and version if relevant]

### **Error Symptoms**
[Describe visible symptoms - error messages, incorrect output, crashes, performance issues, etc.]

**Error Messages/Logs**:
```
[Paste relevant error messages or stack traces here]
```

**Observed Behavior**:
- [Symptom 1]: [Description]
- [Symptom 2]: [Description]
- [Symptom 3]: [Description]

**Expected Behavior**:
[What should happen instead]

### **SUCCESS CRITERIA**
- [ ] **Bug Reproduced**: [Can reliably reproduce the issue in test environment]
- [ ] **Root Cause Identified**: [Clear understanding of why the bug occurs]
- [ ] **Fix Implemented**: [Solution successfully addresses the root cause]
- [ ] **Tests Pass**: [All existing tests pass + new tests for this bug]
- [ ] **Verification Complete**: [Bug no longer occurs in fixed version]
- [ ] **Documentation Updated**: [Fix documented, known issues updated if needed]

---

## **PLATFORM SCAFFOLDING CHECK**
[Verify diagnostic capabilities and access before investigation]

### 1. **Log Access Verification**

#### **Application Logs**
- **Location**: [Path to application logs]
- **Access Method**: [How to access - SSH, log aggregation tool, local files]
- **Log Level**: [Current logging level - DEBUG/INFO/WARN/ERROR]
- **Accessibility**: ✅ Available / ❌ Need to request access

#### **System Logs**
- **Location**: [Path to system logs if relevant]
- **Access Method**: [How to access system logs]
- **Accessibility**: ✅ Available / ❌ Need to request access

#### **Error Tracking**
- **Tool**: [Sentry/Rollbar/Bugsnag/Custom - if available]
- **Access**: ✅ Available / ❌ Need to request access
- **Error ID**: [If tracked in error monitoring tool]

### 2. **Debug Logging Capabilities**

#### **Can We Add Debug Logs?**
- **Permission**: ✅ Yes / ❌ No / ⚠️ Need approval
- **Deployment Process**: [How to deploy logging changes - hot reload, full deploy, etc.]
- **Log Persistence**: [How long logs are kept]

#### **Recommended Debug Points**
[Where should we add debug logging for this investigation?]
- [Location 1]: [File/function where logging would help]
- [Location 2]: [File/function where logging would help]
- [Location 3]: [File/function where logging would help]

### 3. **Database Access**

#### **Database Diagnostic Access**
- **Database Type**: [PostgreSQL/MySQL/MongoDB/etc.]
- **Access Method**: [Direct SQL/Admin panel/Read-only replica]
- **Query Permissions**: ✅ Read-Write / ✅ Read-Only / ❌ No access
- **Accessibility**: ✅ Available / ❌ Need to request access

#### **Relevant Tables/Collections**
[Which database tables are relevant to this bug?]
- **Table 1**: [Table name] - [Why it's relevant]
- **Table 2**: [Table name] - [Why it's relevant]

#### **Sample Diagnostic Queries**
```sql
-- Query 1: [Purpose of query]
[SQL query to diagnose issue]

-- Query 2: [Purpose of query]
[SQL query to diagnose issue]
```

### 4. **Monitoring & Observability**

#### **Available Monitoring Tools**
- **APM Tool**: [New Relic/DataDog/AppDynamics - if available]
  - Accessibility: ✅ Available / ❌ Not available
- **Metrics Dashboard**: [Grafana/CloudWatch/Custom]
  - Accessibility: ✅ Available / ❌ Not available
- **Tracing**: [Distributed tracing tool if available]
  - Accessibility: ✅ Available / ❌ Not available

#### **Relevant Metrics**
[Which metrics should we monitor during investigation?]
- **Metric 1**: [Metric name] - [Why it's relevant]
- **Metric 2**: [Metric name] - [Why it's relevant]

### 5. **Development Environment**

#### **Can We Reproduce Locally?**
- **Local Environment**: ✅ Available / ❌ Need to set up / ⚠️ Partial
- **Required Data**: [Do we need production data copy? Anonymized data? Sample data?]
- **Environment Parity**: [How close is dev environment to production?]

#### **Debugging Tools Available**
- **IDE Debugger**: ✅ Available / ❌ Not available
- **Network Inspector**: ✅ Available / ❌ Not available
- **Memory Profiler**: ✅ Available / ❌ Not available
- **Performance Profiler**: ✅ Available / ❌ Not available

---

## **ISSUE REPLICATION**

### 1. **Reproduction Steps**
[Detailed steps to reliably reproduce the bug]

**Prerequisites**:
- [Prerequisite 1 - data state, user permissions, etc.]
- [Prerequisite 2]
- [Prerequisite 3]

**Step-by-Step Reproduction**:
1. [Step 1: Detailed action to take]
2. [Step 2: Detailed action to take]
3. [Step 3: Detailed action to take]
4. [Continue until bug manifests]

**Expected Result**: [What should happen]

**Actual Result**: [What actually happens - the bug]

### 2. **Test Environment Setup**

#### **Environment Configuration**
- **Environment Used**: [Local/Staging/Production]
- **Configuration Changes**: [Any config changes needed to reproduce]
- **Test Data Requirements**: [Specific data needed]

#### **Setup Checklist**
- [ ] Environment configured correctly
- [ ] Test data loaded/prepared
- [ ] Dependencies installed/running
- [ ] Monitoring/logging enabled
- [ ] Initial state verified

### 3. **Reproduction Success Criteria**
[How do we know we've successfully reproduced the bug?]

- **Verification 1**: [Observable symptom that confirms bug]
- **Verification 2**: [Log message or error that appears]
- **Verification 3**: [System state that indicates bug occurred]

**Reproduction Rate**: [Always/Often/Sometimes/Rarely - X out of Y attempts]

### 4. **Edge Cases & Variations**

#### **Bug Variations**
[Does the bug manifest differently in different scenarios?]

**Variation 1**: [Different trigger or symptom]
- **Trigger**: [What causes this variation]
- **Symptom**: [How it manifests differently]

**Variation 2**: [Different trigger or symptom]
- **Trigger**: [What causes this variation]
- **Symptom**: [How it manifests differently]

#### **Non-Reproducing Scenarios**
[When does the bug NOT occur? This helps narrow down root cause]
- **Scenario 1**: [When bug doesn't happen] - **Why significant**: [What this tells us]
- **Scenario 2**: [When bug doesn't happen] - **Why significant**: [What this tells us]

---

## **BUG LOCATION**

**Where is the code producing the bug symptom?**
[Identify the actual file/line/function where the error message, incorrect output, or bug symptom is generated - this is FACTUAL based on stack traces, logs, or debugger, NOT a guess]

### **Symptom Source**
- **File**: [File path where the bug symptom is produced]
- **Function/Line**: [Function name and/or line number]
- **How Found**: [Stack trace / Error log / Debugger / Code search]

### **Evidence**
```
[Paste stack trace, error log, or debugger output that shows this location]
```

### **What This Code Does**
[Brief explanation of what this code is supposed to do - helps understand context]

---

## **ROOT CAUSE INVESTIGATION**

### 1. **Log Analysis**

#### **Relevant Log Entries**
[Key log entries that provide clues]

**Log Entry 1**:
```
[Timestamp] [Log Level] [Component]
[Log message with relevant details]
```
**Analysis**: [What this log entry tells us]

**Log Entry 2**:
```
[Timestamp] [Log Level] [Component]
[Log message with relevant details]
```
**Analysis**: [What this log entry tells us]

#### **Log Pattern Analysis**
- **Pattern Observed**: [What pattern do we see in logs]
- **Frequency**: [How often does this pattern appear]
- **Correlation**: [What events correlate with this pattern]

### 2. **Code Flow Analysis**

*Trace the execution path from entry point to where bug symptom is produced (Bug Location)*

```
Entry Point → Function A → Function B → Bug Location (symptom produced)
```

**Detailed Flow**:
1. **Entry**: [Where execution starts - e.g., API endpoint, user action]
2. **Step 1**: [Function/method called] - [State changes]
3. **Step 2**: [Function/method called] - [State changes]
4. **Bug Location**: [Where symptom is produced - reference BUG LOCATION section]

### 3. **Database State Examination**

#### **Data Anomalies**
[Unexpected data states that contribute to bug]

**Query Results**:
```sql
-- Diagnostic query
[SQL query used]
```

**Results**:
```
[Query results showing unexpected data]
```

**Analysis**: [What these results reveal about the bug]

#### **Data Integrity Issues**
- **Issue 1**: [Missing data, null values, invalid state, etc.]
- **Issue 2**: [Constraint violations, orphaned records, etc.]
- **Issue 3**: [Timing issues, race conditions, etc.]

### 4. **Hypothesis & Testing**

*Sequential hypothesis testing - test ONE hypothesis at a time, confirm or reject, then proceed to next if needed. Do NOT brainstorm multiple hypotheses upfront.*

#### **Hypothesis 1**
- **Suspected Root Cause**: [What you think is causing the bug]
- **Suspicious Code Location**: [File/function you think has the issue - this is a GUESS, not factual like Bug Location]
- **Reasoning**: [Why you think this based on logs, code flow, database state, and bug location]

**Test**:
- **Method**: [How to test this hypothesis - add debug logs, inspect values, trace execution, etc.]
- **Expected Result if Correct**: [What you'd observe if this is the root cause]
- **Actual Result**: [What you actually observed when testing]
- **Conclusion**: ✅ Confirmed → proceed to ROOT CAUSE CONCLUSION / ❌ Rejected → proceed to Hypothesis 2

---

#### **Hypothesis 2** *(fill only if Hypothesis 1 rejected)*
- **Suspected Root Cause**: [Next hypothesis based on what you learned from Hypothesis 1]
- **Suspicious Code Location**: [Different file/function you think has the issue]
- **Reasoning**: [Why you think this, incorporating learnings from Hypothesis 1 rejection]

**Test**:
- **Method**: [How to test this hypothesis]
- **Expected Result if Correct**: [What you'd observe if this is the root cause]
- **Actual Result**: [What you actually observed when testing]
- **Conclusion**: ✅ Confirmed → proceed to ROOT CAUSE CONCLUSION / ❌ Rejected → proceed to Hypothesis 3

---

#### **Hypothesis 3** *(fill only if Hypothesis 2 rejected)*
- **Suspected Root Cause**: [Next hypothesis based on accumulated learnings]
- **Suspicious Code Location**: [Different file/function you think has the issue]
- **Reasoning**: [Why you think this, incorporating learnings from previous rejections]

**Test**:
- **Method**: [How to test this hypothesis]
- **Expected Result if Correct**: [What you'd observe if this is the root cause]
- **Actual Result**: [What you actually observed when testing]
- **Conclusion**: ✅ Confirmed → proceed to ROOT CAUSE CONCLUSION / ❌ Rejected → consider escalation or broader investigation

### **ROOT CAUSE CONCLUSION**

*This section is filled ONLY after a hypothesis is confirmed above*

**Confirmed Root Cause**: [The verified cause of the bug from successful hypothesis test]

**Confirmed By**: [Reference which hypothesis was confirmed - e.g., "Hypothesis 2 confirmed"]

**Why This Happened**: [Technical explanation of how this root cause produces the bug symptoms]

**Supporting Evidence**:
- [Evidence 1 from hypothesis test]
- [Evidence 2 from logs/database/code analysis]
- [Evidence 3 from investigation]

---

## **SOLUTION SYNTHESIS**

### **Fix Approach Evaluation**

#### **Approach 1: [Fix Strategy Name]**
**Description**: [What this fix involves]

**Type**: [Quick Patch / Proper Fix / Refactor]

**Implementation**:
- [Change 1 required]
- [Change 2 required]
- [Change 3 required]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Risk Level**: [Low/Medium/High]

**Estimated Effort**: [Time estimate]

#### **Approach 2: [Fix Strategy Name]**
**Description**: [What this fix involves]

**Type**: [Quick Patch / Proper Fix / Refactor]

**Implementation**:
- [Change 1 required]
- [Change 2 required]
- [Change 3 required]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Risk Level**: [Low/Medium/High]

**Estimated Effort**: [Time estimate]

#### **Approach 3: [Fix Strategy Name]**
**Description**: [What this fix involves]

**Type**: [Quick Patch / Proper Fix / Refactor]

**Implementation**:
- [Change 1 required]
- [Change 2 required]
- [Change 3 required]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Risk Level**: [Low/Medium/High]

**Estimated Effort**: [Time estimate]

### **Comparison Matrix**

| Approach | Risk | Effort | Impact | Sustainability | Total Score |
|----------|------|--------|--------|----------------|-------------|
| Approach 1 | [1-10] | [1-10] | [1-10] | [1-10] | [Sum] |
| Approach 2 | [1-10] | [1-10] | [1-10] | [1-10] | [Sum] |
| Approach 3 | [1-10] | [1-10] | [1-10] | [1-10] | [Sum] |

**Scoring**:
- **Risk**: Lower risk = higher score (10 = very safe)
- **Effort**: Less effort = higher score (10 = very quick)
- **Impact**: Better fix = higher score (10 = completely resolves)
- **Sustainability**: More maintainable = higher score (10 = clean, proper fix)

### **Risk Assessment**

#### **Implementation Risks**
- **Risk 1**: [What could go wrong during implementation]
  - **Probability**: [Low/Medium/High]
  - **Impact**: [Low/Medium/High]
  - **Mitigation**: [How to reduce this risk]

- **Risk 2**: [What could go wrong during implementation]
  - **Probability**: [Low/Medium/High]
  - **Impact**: [Low/Medium/High]
  - **Mitigation**: [How to reduce this risk]

#### **Deployment Risks**
- **Risk 1**: [What could go wrong during deployment]
  - **Probability**: [Low/Medium/High]
  - **Impact**: [Low/Medium/High]
  - **Mitigation**: [How to reduce this risk]

### **Testing Strategy**

#### **Unit Tests**
- **New Test 1**: [Test for the bug scenario]
- **New Test 2**: [Test for edge cases]
- **Modified Test 1**: [Existing test that needs update]

#### **Integration Tests**
- **Test 1**: [Integration scenario to verify]
- **Test 2**: [Integration scenario to verify]

#### **Manual Testing Checklist**
- [ ] **Bug Scenario**: [Original bug reproduction - should no longer occur]
- [ ] **Edge Case 1**: [Edge case testing]
- [ ] **Edge Case 2**: [Edge case testing]
- [ ] **Regression**: [Verify existing functionality still works]
- [ ] **Performance**: [Verify no performance degradation]

### **Rollback Plan**

#### **Rollback Trigger**
[Under what conditions should we rollback?]
- **Trigger 1**: [Condition requiring rollback]
- **Trigger 2**: [Condition requiring rollback]

#### **Rollback Process**
1. **Step 1**: [How to rollback - revert commit, previous version deploy, etc.]
2. **Step 2**: [Verification after rollback]
3. **Step 3**: [Communication to stakeholders]

#### **Rollback Validation**
- [ ] **System Restored**: [Previous version running successfully]
- [ ] **Data Integrity**: [No data corruption from rollback]
- [ ] **Users Notified**: [Stakeholders informed if needed]

---

## **SELECTED FIX**

### **Chosen Approach**
[Clear statement of which fix approach was selected and why]

**Selected Fix**: [Approach name/ID]

**Selection Rationale**:
[Why this approach was chosen over alternatives - reference scoring matrix and risk assessment]

**Key Benefits**:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

**Accepted Trade-offs**:
- [Trade-off 1 we're accepting]
- [Trade-off 2 we're accepting]

### **Technical Implementation Details**

#### **Code Changes Required**

**File 1**: [File path]
```
[Language]
// Before (buggy code)
[Current code snippet]

// After (fixed code)
[Fixed code snippet]
```
**Change Description**: [What this change does and why it fixes the bug]

**File 2**: [File path]
```
[Language]
// Before
[Current code snippet]

// After
[Fixed code snippet]
```
**Change Description**: [What this change does and why it fixes the bug]

#### **Database Changes** (if applicable)
```sql
-- Migration script
[SQL for schema changes, data fixes, etc.]
```
**Change Description**: [What database changes are needed and why]

#### **Configuration Changes** (if applicable)
- **Config 1**: [Setting name] = [New value] - [Why this change]
- **Config 2**: [Setting name] = [New value] - [Why this change]

#### **Dependency Updates** (if applicable)
- **Package 1**: [Package name] - [Old version] → [New version] - [Why updating]

### **Implementation Flow**

```mermaid
sequenceDiagram
    [Include mermaid sequence diagram showing fixed flow after implementation]
```

### **Implementation Phases**

[Clear step-by-step implementation guide for the fix]

#### **Phase 1**: [First implementation step]
- **Action**: [What to do]
- **Command/Code**: [Specific command or code change if applicable]
- **Verification**: [How to verify this step worked]

#### **Phase 2**: [Second implementation step]
- **Action**: [What to do]
- **Command/Code**: [Specific command or code change if applicable]
- **Verification**: [How to verify this step worked]

#### **Phase 3**: [Third implementation step]
- **Action**: [What to do]
- **Command/Code**: [Specific command or code change if applicable]
- **Verification**: [How to verify this step worked]

#### **Phase 4**: [Testing and deployment step]
- **Action**: [How to test and deploy the fix]
- **Command/Code**: [Test and deployment commands]
- **Verification**: [How to verify fix is deployed and working]

---

*Patching Ship plan template for systematic bug investigation and root cause analysis with Alvi! 🚢🔧*
