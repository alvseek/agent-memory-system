#!/usr/bin/env bash
# check-core-invariant.sh — enforce "memory core references no add-on procedure by name".
# The core (memory-server) must be servable standalone to a chat agent with zero coding/repo
# procedures embedded. This guard greps the core file set for add-on procedure names.
# Exit 0 = clean; exit 1 = leak(s) found. Wire into setup/compile + pre-commit.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"   # control-files/

# --- Core file set (what becomes agent-memory-server) ---
CORE_FILES=(
  "$ROOT/core-instruction-control-files.md"
  "$ROOT/procedures/awaken-agent.md"
  "$ROOT/procedures/refresh-memory.md"
  "$ROOT/procedures/wrap-up.md"
  "$ROOT/procedures/push-memory.md"
  "$ROOT/procedures/pull-memory.md"
)
# plus all memory primitives + compiled core memory
while IFS= read -r f; do CORE_FILES+=("$f"); done < <(find "$ROOT/procedures/memory" -name '*.md')
while IFS= read -r f; do CORE_FILES+=("$f"); done < <(find "$ROOT/core-memory" -maxdepth 1 -name '*.md' 2>/dev/null || true)

# --- Add-on procedure names the core must NOT reference ---
ADDON='/(awaken-coder|project-wrap-up|localize-context|localized-memory-workflow|map-orientation|high-wizard|quick-wizard|council-of-wizards|rite-of-creation|forge-of-covenant|implement-plan|generate-readme|generate-docs|generate-architecture-docs|generate-domain-docs|generate-flow-docs|discovery-contract|analyze-code-quality|generate-standard|integration-test|setup-qa-instrument|setup-qa-visual-instrument|pixel-wizard|pull-all|pull-project|push-all|push-project|push-agent-work|push-exclude-policy|wait-options|ask-agent|delegate-agent|setup-fleet|update-project-context|load-project-context)\b'

leaks=0
for f in "${CORE_FILES[@]}"; do
  [ -f "$f" ] || continue
  if hits=$(grep -noiE "$ADDON" "$f" 2>/dev/null); then
    echo "LEAK in ${f#"$ROOT"/}:"
    echo "$hits" | sed 's/^/    /'
    leaks=$((leaks+1))
  fi
done

if [ "$leaks" -eq 0 ]; then
  echo "✅ Core invariant holds — the memory core references no add-on procedure by name."
  exit 0
else
  echo "🚨 Core invariant VIOLATED — $leaks core file(s) reference an add-on. The core must stay standalone."
  exit 1
fi
