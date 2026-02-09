# Fixing Rod Plan Template

**Quick Bug Fix Protocol** - For straightforward bugs with obvious root cause and simple fixes.

---

## **BUG INFO**

- **Project**: [Project Name]
- **Bug ID**: [Ticket/Issue ID if available]
- **Date**: [YYYY-MM-DD]
- **Agent**: [Agent Name]

### **What's Broken**
[Clear 1-2 sentence description of the bug]

### **Where**
[Which file, component, or module has the bug]

### **Impact**
- **Severity**: [Critical/High/Medium/Low]
- **Affected**: [Who or what is impacted]

---

## **QUICK SCAFFOLDING CHECK**

**5-minute access verification** - Ensure you can debug before diving in:

- [ ] **Logs**: [Where/How to access logs - file path, CloudWatch, Datadog, etc.]
- [ ] **Config/Code**: [Where config/code is stored - repo access, environment variables, config files]
- [ ] **Test Environment**: [How to test the fix - local env, staging, test command]

---

## **BUG LOCATION**

**Where is the code producing the bug symptom?**
[Identify the actual file/line/function where the error message, incorrect output, or bug symptom is generated - this is factual, not a guess]

- **File**: [File path where symptom is produced]
- **Function/Line**: [Function name or line number]
- **How Found**: [How you located this - error stack trace, log message, debugger, etc.]

---

## **HYPOTHESIS & TESTING**

*Sequential hypothesis testing - test one hypothesis at a time, confirm or reject, then proceed to next if needed*

### **Hypothesis 1**
- **What I Think Causes the Bug**: [Your hypothesis about why the bug occurs]
- **Reasoning**: [Why you think this based on bug location and symptoms]
- **Test Method**: [How you'll verify this hypothesis]
- **Test Result**: [What you observed when testing]
- **Conclusion**: ✅ Confirmed → proceed to ROOT CAUSE / ❌ Rejected → proceed to Hypothesis 2

### **Hypothesis 2** (if Hypothesis 1 rejected)
- **What I Think Causes the Bug**: [Next hypothesis]
- **Reasoning**: [Why you think this]
- **Test Method**: [How you'll verify]
- **Test Result**: [What you observed]
- **Conclusion**: ✅ Confirmed → proceed to ROOT CAUSE / ❌ Rejected → proceed to Hypothesis 3

### **Hypothesis 3** (if Hypothesis 2 rejected)
- **What I Think Causes the Bug**: [Next hypothesis]
- **Reasoning**: [Why you think this]
- **Test Method**: [How you'll verify]
- **Test Result**: [What you observed]
- **Conclusion**: ✅ Confirmed → proceed to ROOT CAUSE / ❌ Rejected → escalate to Patching Ship

---

## **ROOT CAUSE**

*This section is filled ONLY after a hypothesis is confirmed*

**Confirmed Root Cause**: [The verified cause of the bug from successful hypothesis test]

**Why This Causes the Bug**: [Technical explanation of how this root cause produces the symptoms]

**Confirmed By**: [Reference which hypothesis was confirmed - e.g., "Hypothesis 1 confirmed"]

---

## **FIX SOLUTION**

### **What to Change**
[Brief description of what needs to be changed to fix the bug]

### **Why This Fix Works**
[1-2 sentences explaining how this change addresses the root cause]

### **Code/Config Change**
```[language]
// Before (buggy)
[Current code/config that's broken]

// After (fixed)
[Fixed code/config]
```

---

## **IMPLEMENTATION PHASES**

### **Phase 1**: [First action]
- **Do**: [What to do]
- **Verify**: [How to check it worked]

### **Phase 2**: [Second action]
- **Do**: [What to do]
- **Verify**: [How to check it worked]

### **Phase 3**: [Third action - usually test and deploy]
- **Do**: [What to do]
- **Verify**: [How to check it worked]

---

## **TESTING CHECKLIST**

- [ ] **Bug Scenario**: [Original bug no longer occurs]
- [ ] **Basic Functionality**: [Related features still work]
- [ ] **Quick Regression**: [Nothing else broke]
- [ ] **Deployed**: [Fix is live and working]

---

*Fixing Rod plan template for quick bug fixes with Alvi! 🎣✨*
