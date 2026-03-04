# Generate README (7Q README)

Generate a **7Q README** (full name: **7 Questions Framework README**) by copying the template into a project, investigating the relevant scope, and filling each section from code.

## Arguments

`$ARGUMENTS`

- `/generate-readme` → Generate README at `./docs/README.md` for the current project scope
- `/generate-readme [path]` → Generate README at the specified path (e.g., `./README.md`, `./src/orders/docs/README.md`)

If no arguments provided, use default: `./docs/README.md`

---

## Procedure

### Step 1: Determine Target

1. **If path argument provided**: Use it as the target file path
2. **If no argument**: Default to `./docs/README.md`
3. **If target file already exists**: Ask [USER-NAME] before overwriting — "A README already exists at [path]. Overwrite, merge, or pick a different location?"

### Step 2: Copy Template

1. Read the [README Template](//@agent-memory/control-files/templates/readme-template.md)
2. Copy it to the target location
3. Update the `# [Project Name]` heading with the actual project/module name
4. Remove the convention preamble block (the blockquote marked "delete this section after reading") — the agent already knows the conventions

### Step 3: Investigate Scope

First, confirm the scope is clear. If the target path or invocation context makes it obvious (e.g., `./src/orders/docs/README.md` = orders module), proceed. If not, ask [USER-NAME]: "What should this README cover? (whole project / specific module / specific service / something else?)"

Once scope is clear, investigate what's relevant to fill the README. Adapt the investigation to what exists — not every project has all of these:

- **Structure**: Folder layout, key files, entry points
- **Tech stack**: `package.json`, `requirements.txt`, `Cargo.toml`, `*.csproj`, etc.
- **API endpoints**: Routes, controllers, handlers
- **Data models**: Entities, schemas, migrations
- **External integrations**: Third-party services, queues, caches
- **CI/CD**: Pipeline configs, deployment scripts
- **Tests**: Test structure, how to run them
- **Existing docs**: Any docs that already exist (don't duplicate, reference them)

### Step 4: Scope Health Check

After investigation, estimate whether the README will exceed **500 lines**. Signs of a too-large scope:
- Many modules/services to document
- 20+ API endpoints
- Complex multi-step setup across multiple environments
- Multiple large data models or integration flows

**If estimated <= 500 lines**: Proceed to Step 5.

**If estimated > 500 lines**: STOP. The scope is too big for a single README. Recommend **fractal scaling** to [USER-NAME]:
- "This scope is too large for a single README (~[estimate] lines). The detail should live in child unit READMEs, not in one big file."
- Identify which buildable units (services, modules, packages) should get their own 7Q README
- Offer to generate the parent README first (high-level Q1-Q7), then handle child unit READMEs in separate `/generate-readme` invocations
- **DO NOT recommend splitting into section files** (SETUP.md, ARCHITECTURE.md...) — that's decomposition, not fractal. Every `README*.md` is a complete 7Q README at its scope
- Cross-cutting topics that span multiple units can go in `README-{topic}.md` at the parent `docs/` level (e.g., `docs/README-deployment.md`)
- If the project also has standards docs (`STANDARDS.md`, `STANDARDS-{topic}.md`), note their existence but don't generate them with this procedure
- Wait for [USER-NAME]'s decision before proceeding

### Step 5: Fill Sections

Fill each Q1-Q7 section based on investigation findings:

- **Q1 (What Is This?)**: Project purpose, architecture overview, tech stack
- **Q2 (How Do I Set It Up?)**: Prerequisites, setup steps, environment variables
- **Q3 (How Do I Use It?)**: Commands, API endpoints or usage examples
- **Q4 (How Does It Work Inside?)**: Core flows, data model, external integrations
- **Q5 (How Is It Deployed?)**: Environments, CI/CD, infrastructure, monitoring
- **Q6 (What Decisions Were Made?)**: Key ADRs if any exist
- **Q7 (What's Broken / Known Debts?)**: Known issues, tech debts, limitations

**Filling rules**:
- Fill from actual code — don't invent or assume
- Delete sections that genuinely don't apply (e.g., Q5 for a library with no deployment)
- Keep it honest — an incomplete README is better than a fictional one
- Remove HTML comment tips as you fill each section (they're guidance, not content)

**Unknown markers** — use typed markers instead of generic TODOs:
- `[TODO: ...]` — needs human input, not findable in code (e.g., deployment URLs, monitoring dashboards, credentials locations)
- `[CONFIRM: ...]` — found something but needs human verification (e.g., "Found Dockerfile — is Docker the current deployment method?")
- `[NOT FOUND: ...]` — expected to exist in code but couldn't locate (e.g., "No CI/CD config found — is there a pipeline?")

### Step 6: Present for Review

Present the completed README to [USER-NAME]:
- Group outstanding markers by type so [USER-NAME] can address them efficiently:
  - **Needs input** (`[TODO]`): items only a human can provide
  - **Needs confirmation** (`[CONFIRM]`): items found but uncertain
  - **Not found** (`[NOT FOUND]`): items expected but missing from codebase
- Note any sections that were removed and why
- Ask if anything needs adjustment

---
