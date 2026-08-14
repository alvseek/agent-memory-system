"""Install the agent-memory CORE procedures as ``~/.claude/commands/`` slash commands.

Compiles every command with the **markdown** storage backend (via ``compile-procedures.py``)
into ``procedures/output/`` — seam procedures composed + decluttered, non-seam procedures
copied as-is — then installs the resulting self-contained ``<name>.md`` files. So the
installed command is the *compiled* procedure (mechanics inlined), not the raw seam source.

Installs ONLY the memory core (this repo). The coding overlay (agent-memory-coding-skill) is
a separate repo with its OWN installer; each installer owns its own manifest and cleans up
independently, so they coexist in the same target dir. This installer never deletes a command
the sibling overlay manifest claims.

Cross-platform (replaces the old ``.sh``): run directly on macOS/Linux, or via the ``.bat``
wrapper on Windows.

Usage:        python control-files/procedures/setup-scripts/setup-all-claude-code.py
Env override: AGENT_MEMORY_TARGET_DIR (default: ~/.claude/commands)
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import sys
from pathlib import Path

# control-files/ root (this script lives at procedures/setup-scripts/setup-all-claude-code.py).
_CF_ROOT = Path(__file__).resolve().parents[2]

_MANIFEST_NAME = ".agent-memory-manifest"
_SIBLING_MANIFEST_NAME = ".agent-memory-coding-skill-manifest"


def _load(name: str, path: Path):
    """Load a hyphen-named sibling script by file path (reusing an already-loaded copy)."""
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_cc = _load("cf_compile", _CF_ROOT / "procedures" / "setup-scripts" / "compile-procedures.py")


def _cleanup(target_dir: Path, manifest: Path, sibling_manifest: Path) -> int:
    """Remove previously installed core commands (per the core manifest), never touching a
    file the sibling overlay manifest claims. Returns the count removed."""
    if not manifest.exists():
        return 0
    sibling: set[str] = set()
    if sibling_manifest.exists():
        raw = sibling_manifest.read_text(encoding="utf-8").splitlines()
        sibling = {ln.strip() for ln in raw if ln.strip()}
    removed = 0
    for ln in manifest.read_text(encoding="utf-8").splitlines():
        fname = ln.strip()
        if not fname or fname in sibling:
            continue
        f = target_dir / fname
        if f.is_file():
            f.unlink()
            removed += 1
    return removed


def install(
    target_dir: Path | str,
    content_root: Path | str = _CF_ROOT,
    output_dir: Path | str | None = None,
) -> tuple[list[str], list[str], int]:
    """Compile the markdown command set and install it into ``target_dir``.

    Returns ``(installed_command_names, skipped_names, removed_count)``.
    """
    content_root = Path(content_root)
    target_dir = Path(target_dir)
    output_dir = Path(output_dir) if output_dir else content_root / "procedures" / "output"
    target_dir.mkdir(parents=True, exist_ok=True)
    manifest = target_dir / _MANIFEST_NAME
    sibling_manifest = target_dir / _SIBLING_MANIFEST_NAME

    # Compile markdown backend → output/. The reports are exactly the plain <name>.md files
    # produced this run (seam composed + non-seam as-is) — no stale/dual files, so we copy
    # those precisely rather than globbing the shared, persistent output dir.
    reports, skipped = _cc.compile_all(content_root, output_dir, backend="markdown")

    removed = _cleanup(target_dir, manifest, sibling_manifest)

    installed: list[str] = []
    manifest_lines: list[str] = []
    for r in reports:
        shutil.copyfile(r.out_path, target_dir / r.out_path.name)
        installed.append(r.name)
        manifest_lines.append(r.out_path.name)
    manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8", newline="\n")
    return installed, skipped, removed


def main(argv: list[str] | None = None) -> int:
    target = os.environ.get("AGENT_MEMORY_TARGET_DIR") or str(Path.home() / ".claude" / "commands")

    print("=== Setup agent-memory CORE Slash Commands ===\n")
    print(f"Source (compiled): {_CF_ROOT / 'procedures' / 'output'}")
    print(f"Target:            {target}\n")

    installed, skipped, removed = install(target)

    if removed:
        print(f"Cleaned up {removed} previously installed core commands.\n")
    if not installed:
        print("Error: no procedures compiled — nothing installed.")
        return 1

    print(f"Successfully installed {len(installed)} core procedures!\n")
    print("Installed core commands:")
    for name in installed:
        print(f"  /{name}")
    if skipped:
        print(f"\nSkipped (seam marker, but no markdown section): {', '.join(sorted(skipped))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
