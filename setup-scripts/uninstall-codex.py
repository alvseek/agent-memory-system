#!/usr/bin/env python3
"""Remove the agent-memory CORE markdown install for Codex.

The inverse of ``setup-codex.sh``, scoped to the **core only**. It removes exactly the
markdown-backend artifacts the core Codex installer writes for this harness, and nothing the
sibling fleet repo (``agent-memory-fleet``) owns:

  1. Core skills -- ``~/.agents/skills/agent-memory-*/`` -- the set the core manifest
     (``.agent-memory-codex-manifest``) claims, never a folder the fleet manifest claims.
  2. Core memory -- the compiled memory content in ``~/.codex/AGENTS.md`` (the user profile, the
     RAS triggers and the reasoning digest). What survives is what the harness and the overlay
     own: the ``[CORE-ACCESS]`` / ``[CORE-MCP-URL]`` declarations and the appended path
     definitions.
  3. The core's Codex SessionStart hook -- the delimited block in ``~/.codex/config.toml`` that
     runs ``scripts/codex-agent-refresh.sh``. ``tool_output_token_limit`` and ``codex_hooks``
     are left alone: the first is a generic harness setting, the second is a Codex feature flag
     other hooks may rely on.

Left in place on purpose:

  - the fleet skills (``agent-fleet-*``) and ``.agent-memory-fleet-codex-manifest``,
  - the ``~/.config/opencode/skills/`` and ``~/.claude/commands/`` installs,
  - the data store (``~/.claude/@agent-memory``) -- that is the memory, not an install.

OpenCode reads ``~/.agents/skills`` as a global compatibility root, so this folder is visible to
both harnesses: running this removes the core from OpenCode's skill list as well. That is
intended, since this folder is the *Codex* install; a harness whose core is served over MCP does
not need it, and one that does (markdown ``[CORE-ACCESS]``) must keep it.

A timestamped backup is written before ``AGENTS.md`` and ``config.toml`` are touched.
Idempotent: a second run finds nothing left to remove.

Usage:        python control-files/setup-scripts/uninstall-codex.py [--yes]
Env override: AGENT_MEMORY_TARGET_DIR   (default: ~/.agents/skills)
              AGENT_MEMORY_AGENTS_FILE  (default: ~/.codex/AGENTS.md)
              AGENT_MEMORY_CODEX_CONFIG (default: ~/.codex/config.toml)
"""

from __future__ import annotations

import datetime
import os
import shutil
import sys
from pathlib import Path

_CORE_MANIFEST_NAME = ".agent-memory-codex-manifest"
_SIBLING_MANIFEST_NAME = ".agent-memory-fleet-codex-manifest"
_CORE_SKILL_PREFIX = "agent-memory-"
_CORE_HEADER = "<!-- COMPILED CORE MEMORY FILE -->"
_OVERLAY_MARKER = "overlay-path-def"
_KEEP_MARKERS = ("**[CORE-ACCESS]**", "**[CORE-MCP-URL]**")
_HOOK_START = "# AGENT-MEMORY-CODEX-HOOK-START"
_HOOK_END = "# AGENT-MEMORY-CODEX-HOOK-END"

DEFAULT_SKILLS_DIR = Path.home() / ".agents" / "skills"
DEFAULT_AGENTS_FILE = Path.home() / ".codex" / "AGENTS.md"
DEFAULT_CONFIG_FILE = Path.home() / ".codex" / "config.toml"


def _read_lines(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def _backup(path: Path) -> Path:
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.name}.bak-{stamp}")
    shutil.copyfile(path, backup)
    return backup


def remove_core_skills(target_dir: Path) -> list[str]:
    """Remove core skill folders -- those the core manifest claims, plus any orphan carrying
    the core prefix -- never one the sibling fleet manifest claims. Returns the names removed."""
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
    """Remove the compiled core memory from AGENTS.md, keeping the harness declarations
    ([CORE-ACCESS], [CORE-MCP-URL]) and the overlay's own path definitions. Backs up first."""
    if not agents_file.is_file():
        return f"no {agents_file.name} found -- nothing to strip"
    text = agents_file.read_text(encoding="utf-8")
    if _CORE_HEADER not in text:
        return f"{agents_file.name} has no compiled core-memory block -- left untouched"

    backup = _backup(agents_file)

    lines = text.splitlines(keepends=True)
    declarations = [ln.rstrip() for ln in lines if any(m in ln for m in _KEEP_MARKERS)]
    keep_from = next((i for i, ln in enumerate(lines) if _OVERLAY_MARKER in ln), None)
    overlay = [ln.rstrip() for ln in lines[keep_from:]] if keep_from is not None else []

    parts = [part for part in ("\n".join(declarations), "\n".join(overlay)) if part]
    kept = "\n\n".join(parts)

    if not kept.strip():
        # The file held only the core memory; nothing of the harness's to keep.
        agents_file.unlink()
        return f"removed {agents_file.name} (it held only the core memory); backup at {backup.name}"

    agents_file.write_text(kept.rstrip("\n") + "\n", encoding="utf-8", newline="\n")
    return (
        f"stripped the core memory from {agents_file.name} "
        f"(kept [CORE-ACCESS] + [CORE-MCP-URL] and the overlay path definitions); "
        f"backup at {backup.name}"
    )


def remove_hook_block(config_file: Path) -> str:
    """Remove the delimited AGENT-MEMORY-CODEX-HOOK block from config.toml. Backs up first.
    Generic settings (tool_output_token_limit, codex_hooks) are deliberately left alone."""
    if not config_file.is_file():
        return f"no {config_file.name} found -- nothing to remove"
    text = config_file.read_text(encoding="utf-8")
    if _HOOK_START not in text:
        return f"{config_file.name} has no agent-memory hook block -- left untouched"

    backup = _backup(config_file)

    kept: list[str] = []
    skipping = False
    for line in text.splitlines():
        if line.strip() == _HOOK_START:
            skipping = True
            continue
        if line.strip() == _HOOK_END:
            skipping = False
            continue
        if not skipping:
            kept.append(line)

    # Collapse the trailing blank run the removed block left behind.
    while kept and not kept[-1].strip():
        kept.pop()

    config_file.write_text("\n".join(kept) + "\n", encoding="utf-8", newline="\n")
    return f"removed the SessionStart hook block from {config_file.name}; backup at {backup.name}"


def main(argv: list[str] | None = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]
    auto_yes = "--yes" in args

    skills_dir = Path(os.environ.get("AGENT_MEMORY_TARGET_DIR") or DEFAULT_SKILLS_DIR)
    agents_file = Path(os.environ.get("AGENT_MEMORY_AGENTS_FILE") or DEFAULT_AGENTS_FILE)
    config_file = Path(
        os.environ.get("AGENT_MEMORY_CODEX_CONFIG") or DEFAULT_CONFIG_FILE
    )

    print("=== Uninstall agent-memory CORE (Codex, markdown) ===\n")
    print(f"Skills dir:   {skills_dir}")
    print(f"Instructions: {agents_file}")
    print(f"Settings:     {config_file}\n")

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
    print(f"Hook: {remove_hook_block(config_file)}")
    print()
    print("Left in place: the fleet skills and their manifest, the OpenCode and Claude Code")
    print("installs, and the data store (~/.claude/@agent-memory).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
