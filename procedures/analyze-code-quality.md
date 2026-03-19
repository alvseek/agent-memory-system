# Analyze Code Quality

Comprehensive code quality analysis for features, milestones, or any code scope. Walks through structured quality dimensions, documents findings with severity, and presents WAIT Options so [USER-NAME] controls what gets fixed. Uses a working document copied from the analysis template to track the full investigation.

## Arguments

`$ARGUMENTS`

- `/analyze-code-quality [scope]` → Analyze code quality for the given scope
- `/analyze-code-quality` → Will ask for scope

**Scope examples:**
- File path(s): `src/api/users.ts`, `src/components/Modal.tsx`
- Directory: `src/features/auth/`
- Feature description: `the login feature we just built`
- Git-based: `all changes since last commit`
- Milestone: `everything in M1`

If no arguments provided, ask: "What code should I review? (file paths, directory, feature, or 'all changes since last commit')"

---

## Procedure

### Step 1: Read Template + Create Working Document

Read the [Code Quality Analysis Template](//@agent-memory/control-files/plan-templates/code-quality-analysis-template.md).

Copy the template to the project's plans folder as a working document:
```
cp {source} ./plans/[YYYY-MM-DD]-[project]-code-quality-analysis.md
```

Fill the **Analysis Info** section (Project, Date, Agent, Scope, Quality Standard).

### Step 2: Determine Scope

Resolve the scope to a concrete list of files to review:
- **File paths / directory**: Use directly
- **Feature description**: Identify related files via grep/glob
- **Git-based**: Use `git diff --name-only HEAD~1` (or appropriate range) to get changed files
- **Milestone**: Identify all files created/modified during the milestone

List the files that will be reviewed. If the scope resolves to more than 20 files, ask [USER-NAME] if they want to narrow it down or proceed with the full scope.

### Step 3: Discover Quality Standard

Search for a project quality standard via glob: `**/quality-standard.md`

- **If found**: Read the quality standard file. Update the Analysis Info section with the path. This will be used in Dimension 8 (Project Quality Standard Compliance) of the analysis.
- **If not found**: Note "None — freeform analysis" in Analysis Info. Skip Dimension 8 during analysis.

### Step 4: Read Files in Scope

Read all files identified in Step 2. For each file, understand:
- What the code does (purpose and context)
- How it integrates with surrounding code
- What patterns and conventions are used

### Step 5: Analyze Quality Dimensions

Walk through each quality dimension in the working document. For each dimension:

1. **Evaluate**: Check each item in the dimension against the code in scope
2. **Mark**: Check off items that pass (`[x]`), leave unchecked items that fail or don't apply
3. **Document findings**: For each failed check, add a row to the **Findings** table with:
   - Severity: **Critical** (bugs, data loss, security), **Medium** (UX gaps, maintainability), **Low** (polish, cleanup)
   - File and line reference
   - Description of the issue
   - 2-3 fix options where meaningful, or single recommended fix for straightforward issues

**Skip dimensions that don't apply** to the scope (e.g., skip "State Completeness" for backend-only code, skip "Security" for a CSS-only change).

**Use judgment beyond the checklist** — the dimensions are guidelines, not an exhaustive list. If you spot an issue that doesn't fit any dimension, document it anyway.

### Step 6: Present Findings

Fill the **WAIT Options** section in the working document, then present to [USER-NAME].

**If findings exist**, present as WAIT Options grouped by severity:

```
Code quality review for [scope]:

**Critical:**
1. [File:line] [Issue]:  [A) Fix ✓✓]  B) Alternative  (why this matters)

**Medium:**
2. [File:line] [Issue]:  [A) Fix ✓✓]  B) Alternative  (why this matters)

**Low:**
3. [File:line] [Issue]:  [A) Fix ✓✓]  B) Skip  (minor polish)

**Summary**: X critical, Y medium, Z low

Reply with changes (e.g., "skip 3", "change 1 to B") or "fix all" to accept defaults, or "ship it" to skip all.
```

STOP. Wait for [USER-NAME]'s response before fixing anything.

**If no findings**, report and proceed:
```
Quality looks good — no findings for [scope]. Proceeding.
```

### Step 7: Fix Approved Items

After [USER-NAME] responds:
- **"fix all"**: Apply all recommended fixes (option A for each finding) in one pass
- **Selective**: Apply only the approved fixes, skip the rest
- **"ship it"**: Skip all fixes, proceed

Fix all approved items in a single batch. After fixing:
1. Update the **Resolution Log** in the working document with what was decided and done
2. Briefly report what was changed to [USER-NAME]

---
