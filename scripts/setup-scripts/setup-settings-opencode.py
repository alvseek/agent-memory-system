"""Configure ``~/.config/opencode/opencode.jsonc`` for agent-memory.

Configures:
  - Bypass permissions: wildcard ``allow`` so OpenCode never prompts (prompted,
    skipped when already configured — same UX as the Claude Code settings script).

Everything else in the file (providers, models, other permissions) is preserved.
A timestamped backup is written before any change.

Cross-platform: run directly on macOS/Linux, or via the ``.bat`` wrapper on Windows.

Usage:        python control-files/scripts/setup-scripts/setup-settings-opencode.py [--yes]
Env override: AGENT_MEMORY_OPENCODE_CONFIG (default: ~/.config/opencode/opencode.jsonc)
"""

from __future__ import annotations

import datetime
import json
import os
import re
import shutil
import sys
from pathlib import Path

DEFAULT_CONFIG = Path.home() / ".config" / "opencode" / "opencode.jsonc"

WILDCARD_ALLOW = {"action": "*", "resource": "*", "effect": "allow"}
ENV_GUARDS = [
    {"action": "read", "resource": "*.env", "effect": "ask"},
    {"action": "read", "resource": "*.env.*", "effect": "ask"},
]

# Strip // line comments and /* */ block comments that appear outside strings.
_TOKEN_RE = re.compile(
    r'"(?:\\.|[^"\\])*"|(?P<line>//[^\n]*)|(?P<block>/\*.*?\*/)',
    re.DOTALL,
)


def _strip_jsonc_comments(text: str) -> str:
    def _repl(m: re.Match[str]) -> str:
        if m.group("line") is not None or m.group("block") is not None:
            return ""
        return m.group(0)

    return _TOKEN_RE.sub(_repl, text)


def _load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        return {}
    try:
        data = json.loads(_strip_jsonc_comments(raw))
    except json.JSONDecodeError as exc:
        print(f"  ERROR: Failed to parse {path}: {exc}")
        print("  Restore from the .bak backup or fix the JSON and re-run.")
        raise SystemExit(1)
    if not isinstance(data, dict):
        print(f"  ERROR: {path} does not contain a JSON object.")
        raise SystemExit(1)
    return data


def _same_rule(a: dict, b: dict) -> bool:
    return (
        a.get("action") == b.get("action")
        and a.get("resource") == b.get("resource")
        and a.get("effect") == b.get("effect")
    )


def _has_wildcard_allow(permissions: list) -> bool:
    return any(
        isinstance(r, dict)
        and r.get("action") == "*"
        and r.get("resource") == "*"
        and r.get("effect") == "allow"
        for r in permissions
    )


def main(argv: list[str] | None = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]
    auto_yes = "--yes" in args

    config_path = Path(
        os.environ.get("AGENT_MEMORY_OPENCODE_CONFIG") or str(DEFAULT_CONFIG)
    )
    print(f"Config: {config_path}\n")

    config = _load_config(config_path)
    permissions = config.get("permissions")
    if permissions is None:
        permissions = []
        config["permissions"] = permissions
    if not isinstance(permissions, list):
        print("  ERROR: 'permissions' is not an array — fix it manually and re-run.")
        return 1

    # --- Bypass permissions (prompt unless already configured or --yes) ---
    enable_bypass: str
    if _has_wildcard_allow(permissions):
        enable_bypass = "skip"
    elif auto_yes:
        enable_bypass = "yes"
    else:
        print()
        try:
            answer = input(
                "  Enable bypass permissions? Skips permission prompts "
                "for all tool executions. (Y/n) "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Cancelled.")
            return 1
        enable_bypass = "yes" if (not answer or answer.lower().startswith("y")) else "no"

    changed = False

    if enable_bypass == "yes":
        # Drop any existing */* rule (allow or otherwise), then append the allow last
        # so it wins — OpenCode uses the last matching rule.
        before = len(permissions)
        permissions[:] = [
            r
            for r in permissions
            if not (
                isinstance(r, dict)
                and r.get("action") == "*"
                and r.get("resource") == "*"
            )
        ]
        permissions.append(dict(WILDCARD_ALLOW))
        # Keep .env reads guarded behind the wildcard allow.
        for guard in ENV_GUARDS:
            if not any(isinstance(r, dict) and _same_rule(r, guard) for r in permissions):
                permissions.append(dict(guard))
        print("  + Bypass permissions enabled (wildcard allow, .env reads still ask)")
        changed = True
    elif enable_bypass == "skip":
        # Still ensure the .env guards exist behind the existing wildcard allow.
        for guard in ENV_GUARDS:
            if not any(isinstance(r, dict) and _same_rule(r, guard) for r in permissions):
                permissions.append(dict(guard))
                changed = True
        if changed:
            print("  + Bypass permissions already configured — added missing .env guards")
        else:
            print("  = Bypass permissions already configured — skipping")
    else:
        print("  - Bypass permissions declined")

    if not changed:
        print()
        print("  No changes needed — all settings already configured")
        return 0

    # Backup before writing.
    if config_path.exists():
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = config_path.with_name(f"{config_path.name}.bak-{stamp}")
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(config_path, backup)
        print(f"  Backup created: {backup}")

    # Keep $schema first for editor validation, preserve everything else in order.
    ordered: dict = {}
    if "$schema" in config:
        ordered["$schema"] = config["$schema"]
    elif not config_path.exists():
        ordered["$schema"] = "https://opencode.ai/config.json"
    for key, value in config.items():
        if key not in ordered:
            ordered[key] = value

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(ordered, indent=2) + "\n", encoding="utf-8")
    print()
    print(f"  Settings written to {config_path}")
    print("  Restart OpenCode (or run `opencode reload`) for changes to take effect.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
