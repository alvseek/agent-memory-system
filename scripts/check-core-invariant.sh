#!/usr/bin/env bash
# check-core-invariant.sh — enforce "memory core references no add-on procedure by name".
# The core (memory-server) must be servable standalone to a chat agent with zero coding/repo
# procedures embedded. This guard greps the core file set for add-on procedure names.
# Exit 0 = clean; exit 1 = leak(s) found. Wire into setup/compile + pre-commit.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"   # control-files/

# --- Core file set (what becomes agent-memory-server) ---
CORE_FILES=(
  "$ROOT/procedures/awaken-agent.md"
  "$ROOT/procedures/refresh-memory.md"
  "$ROOT/procedures/wrap-up.md"
  "$ROOT/procedures/push-memory.md"
  "$ROOT/procedures/pull-memory.md"
  "$ROOT/procedures/create-agent.md"
  "$ROOT/procedures/list-agents.md"
  "$ROOT/procedures/wait-options.md"
)

# A file named here that no longer exists must fail LOUD. Skipping it silently is how the
# awakening protocol stopped being checked: it was listed at the repo root, moved into
# procedures/components/, and simply dropped out of the guard with a green result.
missing_listed=0
for f in "${CORE_FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "MISSING listed core file (move it or update this list): ${f#"$ROOT"/}"
    missing_listed=1
  fi
done

# plus all memory primitives, the shared components inlined into core procedures at compile
# time (their prose ships inside the core, so it is core), and the compiled core memory
while IFS= read -r f; do CORE_FILES+=("$f"); done < <(find "$ROOT/procedures/memory" -name '*.md')
while IFS= read -r f; do CORE_FILES+=("$f"); done < <(find "$ROOT/procedures/components" -name '*.md' 2>/dev/null || true)
while IFS= read -r f; do CORE_FILES+=("$f"); done < <(find "$ROOT/core-memory" -maxdepth 1 -name '*.md' 2>/dev/null || true)

# --- Add-on procedure names the core must NOT reference ---
ADDON='/(awaken-coder|project-wrap-up|localize-context|localized-memory-workflow|map-orientation|high-wizard|quick-wizard|council-of-wizards|rite-of-creation|forge-of-covenant|implement-plan|generate-readme|generate-docs|generate-architecture-docs|generate-domain-docs|generate-flow-docs|discovery-contract|analyze-code-quality|generate-standard|integration-test|setup-qa-instrument|setup-qa-visual-instrument|pixel-wizard|pull-all|pull-project|push-all|push-project|push-agent-work|push-exclude-policy|wait-options-coding|ask-agent|delegate-agent|setup-fleet|update-project-context|load-project-context)\b'

leaks=0
for f in "${CORE_FILES[@]}"; do
  [ -f "$f" ] || continue
  if hits=$(grep -noiE "$ADDON" "$f" 2>/dev/null); then
    echo "LEAK in ${f#"$ROOT"/}:"
    echo "$hits" | sed 's/^/    /'
    leaks=$((leaks+1))
  fi
done

if [ "$leaks" -eq 0 ] && [ "$missing_listed" -eq 0 ]; then
  echo "✅ Core invariant holds — the memory core references no add-on procedure by name."
  exit 0
fi
if [ "$leaks" -gt 0 ]; then
  echo "🚨 Core invariant VIOLATED — $leaks core file(s) reference an add-on. The core must stay standalone."
fi
if [ "$missing_listed" -ne 0 ]; then
  echo "🚨 Guard is blind — a listed core file is missing, so it was never checked."
fi
exit 1
