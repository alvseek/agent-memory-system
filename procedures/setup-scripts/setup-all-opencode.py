"""Install the agent-memory CORE procedures as ``~/.config/opencode/skills/`` skills.

Compiles every command with the **markdown** storage backend (via ``compile-procedures.py``)
into ``procedures/output/`` — seam procedures composed + decluttered, non-seam procedures
copied as-is — then wraps each resulting self-contained ``<name>.md`` file as an OpenCode
skill: ``~/.config/opencode/skills/agent-memory-<name>/SKILL.md``. So the installed skill
is the *compiled* procedure (mechanics inlined), not the raw seam source.

OpenCode skills are the closest equivalent to Claude slash commands here: each skill has a
``description`` the model uses for discovery (``Use when the user wants the "<Title>"
procedure ...``), and skills also surface in the interactive command catalog.

Installs ONLY the memory core (this repo). A sibling overlay installer (if any) owns its
own manifest and cleans up independently, so they coexist in the same target dir. This
installer never deletes a skill the sibling manifest claims.

Cross-platform: run directly on macOS/Linux, or via the ``.bat`` wrapper on Windows.

Usage:        python control-files/procedures/setup-scripts/setup-all-opencode.py [--yes]
Env override: AGENT_MEMORY_TARGET_DIR (default: ~/.config/opencode/skills)
"""

from __future__ import annotations

import importlib.util
import os
import re
import shutil
import sys
from pathlib import Path

# control-files/ root (this script lives at procedures/setup-scripts/setup-all-opencode.py).
_CF_ROOT = Path(__file__).resolve().parents[2]

_MANIFEST_NAME = ".agent-memory-opencode-manifest"
_SIBLING_MANIFEST_NAME = ".agent-memory-coding-skill-manifest"

_TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


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


def _skill_title(name: str, compiled_text: str) -> str:
    """First ``# `` heading of the compiled procedure, falling back to the file stem."""
    m = _TITLE_RE.search(compiled_text)
    return m.group(1).strip() if m else name


def _cleanup(target_dir: Path, manifest: Path, sibling_manifest: Path) -> int:
    """Remove previously installed core skills (per the core manifest), never touching a
    directory the sibling overlay manifest claims. Returns the count removed."""
    if not manifest.exists():
        return 0
    sibling: set[str] = set()
    if sibling_manifest.exists():
        raw = sibling_manifest.read_text(encoding="utf-8").splitlines()
        sibling = {ln.strip() for ln in raw if ln.strip()}
    removed = 0
    for ln in manifest.read_text(encoding="utf-8").splitlines():
        dirname = ln.strip()
        if not dirname or dirname in sibling:
            continue
        d = target_dir / dirname
        if d.is_dir():
            shutil.rmtree(d)
            removed += 1
    return removed


def install(
    target_dir: Path | str,
    content_root: Path | str = _CF_ROOT,
    output_dir: Path | str | None = None,
) -> tuple[list[str], list[str], int]:
    """Compile the markdown command set and install it as OpenCode skills.

    Returns ``(installed_skill_ids, skipped_names, removed_count)``.
    """
    content_root = Path(content_root)
    target_dir = Path(target_dir)
    output_dir = Path(output_dir) if output_dir else content_root / "procedures" / "output"
    target_dir.mkdir(parents=True, exist_ok=True)
    manifest = target_dir / _MANIFEST_NAME
    sibling_manifest = target_dir / _SIBLING_MANIFEST_NAME

    # Compile markdown backend → output/. The reports are exactly the plain <name>.md files
    # produced this run (seam composed + non-seam as-is) — no stale/dual files, so we wrap
    # those precisely rather than globbing the shared, persistent output dir.
    reports, skipped = _cc.compile_all(content_root, output_dir, backend="markdown")

    removed = _cleanup(target_dir, manifest, sibling_manifest)

    installed: list[str] = []
    manifest_lines: list[str] = []
    for r in reports:
        skill_id = f"agent-memory-{r.name}"
        skill_dir = target_dir / skill_id
        skill_dir.mkdir(parents=True, exist_ok=True)
        compiled_text = r.out_path.read_text(encoding="utf-8")
        title = _skill_title(r.name, compiled_text)
        description = (
            f'Use when the user wants the "{title}" procedure'
            f" or explicitly mentions {r.name}."
        )
        skill_md = (
            "---\n"
            f"name: {title}\n"
            f"description: {description}\n"
            "---\n"
            "\n"
            "Follow this procedure exactly. Treat the content below as the canonical workflow.\n"
            "\n"
            f"{compiled_text}"
        )
        (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8", newline="\n")
        installed.append(skill_id)
        manifest_lines.append(skill_id)
    manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8", newline="\n")
    return installed, skipped, removed


def main(argv: list[str] | None = None) -> int:
    target = os.environ.get("AGENT_MEMORY_TARGET_DIR") or str(
        Path.home() / ".config" / "opencode" / "skills"
    )

    print("=== Setup agent-memory CORE OpenCode Skills ===\n")
    print(f"Source (compiled): {_CF_ROOT / 'procedures' / 'output'}")
    print(f"Target:            {target}\n")

    installed, skipped, removed = install(target)

    if removed:
        print(f"Cleaned up {removed} previously installed core skills.\n")
    if not installed:
        print("Error: no procedures compiled — nothing installed.")
        return 1

    print(f"Successfully installed {len(installed)} core procedures!\n")
    print("Installed core skills:")
    for skill_id in installed:
        print(f"  ${skill_id}")
    if skipped:
        print(f"\nSkipped (seam marker, but no markdown section): {', '.join(sorted(skipped))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
