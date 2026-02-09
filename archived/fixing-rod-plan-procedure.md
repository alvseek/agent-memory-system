# Claude Agent - Fixing Rod Planning Procedure

# Fixing Rod Protocol

## When to Use This Protocol
Use Fixing Rod Protocol when you need **quick straightforward bug fixes** where the root cause is obvious and the fix is simple. This protocol is streamlined for speed while maintaining quality.

**Perfect for:**
- Simple bugs where hypothesis can be confirmed within 1-3 attempts
- Quick fixes that take less than 30 minutes
- Bugs with limited scope (single file/module)
- Straightforward issues where root cause is likely obvious after locating bug

**NOT for (use Patching Ship instead):**
- Complex bugs requiring extensive platform diagnostics
- Issues requiring deep log analysis or database state examination
- Bugs needing multiple fix approach evaluation with risk assessment
- Problems requiring detailed rollback planning

*IMPORTANT: To execute the protocol, I have to use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution. Jump directly into implementation is prohibited*

1. I have to find and read the [Fixing Rod Plan Template](//@claude-agents/control-files/plans/fixing-rod-plan-template.md) file
2. I have to create new plan folder in the project root level `/plans` (if it doesn't exist)
3. I need to copy the [Fixing Rod Plan Template](//@claude-agents/control-files/plans/fixing-rod-plan-template.md) file to the `/plans` folder:
   - **Windows**: `powershell -c "Copy-Item {source} -Destination {target} -Force"`
   - **Linux/macOS**: `cp {source} {target}`
4. I have to check the current date using:
   - **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
   - **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`
5. I have to rename the new copy pasted file to `[YYYY-MM-DD]-[project]-[bug-theme]-fix.md` name pattern
6. I have to fill sections in order following the hypothesis-driven process:
   - [Bug Info](//@claude-agents/control-files/plans/fixing-rod-plan-template.md#bug-info) - What's broken, where, and impact
   - [Quick Scaffolding Check](//@claude-agents/control-files/plans/fixing-rod-plan-template.md#quick-scaffolding-check) - Verify debugging access
   - [Bug Location](//@claude-agents/control-files/plans/fixing-rod-plan-template.md#bug-location) - Find the ACTUAL code producing the bug symptom (factual, not a guess)
   - [Hypothesis & Testing](//@claude-agents/control-files/plans/fixing-rod-plan-template.md#hypothesis--testing) - Sequential hypothesis testing:
     - Create Hypothesis 1 → Test it → Confirmed? → Fill Root Cause / Rejected? → Create Hypothesis 2
     - Repeat until hypothesis confirmed or escalate to Patching Ship after 3 failed hypotheses
   - [Root Cause](//@claude-agents/control-files/plans/fixing-rod-plan-template.md#root-cause) - Fill ONLY after hypothesis is confirmed
   - [Fix Solution](//@claude-agents/control-files/plans/fixing-rod-plan-template.md#fix-solution) - What to change and why it fixes the root cause
   - [Implementation Phases](//@claude-agents/control-files/plans/fixing-rod-plan-template.md#implementation-phases) - Step-by-step fix implementation
   - [Testing Checklist](//@claude-agents/control-files/plans/fixing-rod-plan-template.md#testing-checklist) - Verify fix works
7. Then, I have to do a quick self review by asking myself:
    a. Is the bug clearly described with location identified?
    b. Did I verify access to logs, config, and test environment?
    c. Did I locate the actual code producing the bug symptom (not just a guess)?
    d. Did I test my hypothesis before declaring root cause?
    e. Is the root cause confirmed by evidence (not assumed)?
    f. Does the fix solution address the confirmed root cause?
    g. Are implementation phases clear?
    h. Is testing adequate?
8. Present the quick fix plan to Alvi for review and confirmation
9. Present the completed quick fix plan document to Alvi: `/plans/[date]-[project]-[bug-theme]-fix.md`
