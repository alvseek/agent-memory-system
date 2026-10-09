#!/usr/bin/env python3
"""Remove the agent-memory CORE markdown install for OpenCode.

The inverse of ``setup-opencode.py``, scoped to the **core only**. It removes exactly the
markdown-backend artifacts the core installer writes for this harness, and nothing the
sibling overlay (``agent-memory-project``, "Hermod") owns:

  1. Core skills -- ``~/.config/opencode/skills/agent-memory-*/`` -- the set the core manifest
     (``.agent-memory-opencode-manifest``) claims, never a folder the overlay manifest claims.
  2. Core memory -- the compiled memory content in ``~/.config/opencode/AGENTS.md`` (the user
     profile, the RAS triggers and the reasoning digest). What survives is what Hermod owns:
     the ``[CORE-ACCESS]`` and ``[CORE-MCP-URL]`` declarations, and the overlay's appended
     ``[path-to-agent-memory-project]`` line.

Left in place on purpose:

  - the overlay's skills + manifest (Hermod still uses the markdown version),
  - the ``opencode.jsonc`` settings (generic permissions, not core memory, and the overlay
    relies on the same bypass),
  - the data store (``~/.claude/@agent-memory``) -- that is the memory, not an install.

A timestamped backup of ``AGENTS.md`` is written before it is touched. Idempotent: a second
run finds nothing left to remove.

Usage:        python control-files/setup-scripts/uninstall-opencode.py [--yes]
Env override: AGENT_MEMORY_TARGET_DIR   (default: ~/.config/opencode/skills)
              AGENT_MEMORY_AGENTS_FILE  (default: ~/.config/opencode/AGENTS.md)
"""

from __future__ import annotations

import datetime
import os
import shutil
import sys
from pathlib import Path

_CORE_MANIFEST_NAME = ".agent-memory-opencode-manifest"
_SIBLING_MANIFEST_NAME = ".agent-memory-project-opencode-manifest"
_CORE_SKILL_PREFIX = "agent-memory-"
_CORE_HEADER = "<!-- COMPILED CORE MEMORY FILE -->"
_OVERLAY_MARKER = "overlay-path-def"
_KEEP_MARKERS = ("**[CORE-ACCESS]**", "**[CORE-MCP-URL]**")

DEFAULT_SKILLS_DIR = Path.home() / ".config" / "opencode" / "skills"
DEFAULT_AGENTS_FILE = Path.home() / ".config" / "opencode" / "AGENTS.md"


def _read_lines(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def remove_core_skills(target_dir: Path) -> list[str]:
    """Remove core skill folders -- those the core manifest claims, plus any orphan carrying
    the core prefix -- never one the sibling overlay manifest claims. Returns the names removed."""
    if not target_dir.is_dir():
        return []
    sibling = set(_read_lines(target_dir / _SIBLING_MANIFEST_NAME))

    claimed = set(_read_lines(target_dir / _CORE_MANIFEST_NAME))
    # Also catch core-prefixed orphans a lost or partial manifest would miss.
    for entry in target_dir.iterdir():
        if entry.is_dir() and entry.name.startswith(_CORE_SKILL_PREFIX):
            claimed.add(entry.name)

    removed: list[str] = []
    for name in sorted(claimed):
        if name in sibling:
            continue
        folder = target_dir / name
        if folder.is_dir():
            shutil.rmtree(folder)
            removed.append(name)

    manifest = target_dir / _CORE_MANIFEST_NAME
    if manifest.is_file():
        manifest.unlink()
    return removed


def strip_core_memory(agents_file: Path) -> str:
    """Remove the compiled core memory from AGENTS.md, keeping the two declarations Hermod owns
    ([CORE-ACCESS], [CORE-MCP-URL]) and the overlay's own path definition. Backs up first."""
    if not agents_file.is_file():
        return f"no {agents_file.name} found -- nothing to strip"
    text = agents_file.read_text(encoding="utf-8")
    if _CORE_HEADER not in text:
        return f"{agents_file.name} has no compiled core-memory block -- left untouched"

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = agents_file.with_name(f"{agents_file.name}.bak-{stamp}")
    shutil.copyfile(agents_file, backup)

    lines = text.splitlines(keepends=True)
    declarations = [ln.rstrip() for ln in lines if any(m in ln for m in _KEEP_MARKERS)]
    keep_from = next((i for i, ln in enumerate(lines) if _OVERLAY_MARKER in ln), None)
    overlay = [ln.rstrip() for ln in lines[keep_from:]] if keep_from is not None else []

    parts = [part for part in ("\n".join(declarations), "\n".join(overlay)) if part]
    kept = "\n\n".join(parts)

    if not kept.strip():
        # The file held only the core memory; nothing of Hermod's to keep.
        agents_file.unlink()
        return f"removed {agents_file.name} (it held only the core memory); backup at {backup.name}"

    agents_file.write_text(kept.rstrip("\n") + "\n", encoding="utf-8", newline="\n")
    return (
        f"stripped the core memory from {agents_file.name} "
        f"(kept [CORE-ACCESS] + [CORE-MCP-URL] and the overlay path line); "
        f"backup at {backup.name}"
    )


def main(argv: list[str] | None = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]
    auto_yes = "--yes" in args

    skills_dir = Path(os.environ.get("AGENT_MEMORY_TARGET_DIR") or DEFAULT_SKILLS_DIR)
    agents_file = Path(os.environ.get("AGENT_MEMORY_AGENTS_FILE") or DEFAULT_AGENTS_FILE)

    print("=== Uninstall agent-memory CORE (OpenCode, markdown) ===\n")
    print(f"Skills dir:   {skills_dir}")
    print(f"Instructions: {agents_file}\n")

    if not auto_yes:
        try:
            answer = input(
                "Remove the core markdown install for this harness? (y/N) "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return 1
        if answer.lower() not in ("y", "yes"):
            print("Cancelled.")
            return 1
        print()

    removed = remove_core_skills(skills_dir)
    if removed:
        print(f"Removed {len(removed)} core skills:")
        for name in removed:
            print(f"  - {name}")
    else:
        print("No core skills to remove.")

    print()
    print(f"Core memory: {strip_core_memory(agents_file)}")
    print()
    print("Left in place: the overlay (agent-memory-project) skills and its path line,")
    print("the opencode.jsonc settings, and the data store (~/.claude/@agent-memory).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
