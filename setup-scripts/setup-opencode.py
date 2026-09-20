#!/usr/bin/env python3
"""setup-opencode.py - Complete OpenCode setup: user config + core memory + skills + settings.

Usage: python control-files/setup-scripts/setup-opencode.py [--yes]
       bash control-files/setup-scripts/setup-opencode.sh [--yes]

This script orchestrates:
  0. User configuration (identity + OS) — shows defaults, press Enter to keep
  1. Compile core memory and write to ~/.config/opencode/AGENTS.md
     (OpenCode V2's global instruction file — the equivalent of Claude's CLAUDE.md;
     OpenCode does NOT fall back to CLAUDE.md)
  2. Setup all procedures as OpenCode skills in ~/.config/opencode/skills/
     (model-discoverable via description; also surfaces in the slash catalog)
  3. Configure opencode.jsonc (wildcard allow = bypass permissions, .env still asks)

Notes:
  - The user configurator is shared with Claude Code: what it writes (profile + env)
    is platform-agnostic today.
  - Steps 0-1 need `bash` (they run the existing .sh pipeline). On Windows this is
    Git Bash. Steps 2-3 are pure Python and need no bash.
  - `--yes` auto-accepts the bypass-permissions prompt in step 3.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CONTROL_FILES_DIR = SCRIPT_DIR.parent
USER_CONFIG_SCRIPT = (
    CONTROL_FILES_DIR / "core-memory" / "compile-scripts" / "user-config-claude.sh"
)
COMPILE_WRITE_SCRIPT = (
    CONTROL_FILES_DIR
    / "core-memory"
    / "compile-scripts"
    / "compile-write-to-opencode.sh"
)
SETUP_SKILLS_SCRIPT = (
    CONTROL_FILES_DIR / "procedures" / "setup-scripts" / "setup-all-opencode.py"
)
SETUP_SETTINGS_SCRIPT = (
    CONTROL_FILES_DIR / "scripts" / "setup-scripts" / "setup-settings-opencode.py"
)


def _find_bash() -> str | None:
    if os.name == "nt":
        # Prefer Git Bash: C:\Windows\system32\bash.exe is a WSL shim that cannot
        # run our .sh scripts (execvpe(/bin/bash) failure), and it shadows Git Bash
        # when system32 comes first in PATH — so never trust bare PATH order here.
        candidates = [
            os.path.expandvars(r"%ProgramFiles%\Git\bin\bash.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Git\bin\bash.exe"),
            r"C:\Program Files\Git\bin\bash.exe",
        ]
        for candidate in candidates:
            if candidate and Path(candidate).is_file():
                return candidate
        # Fall back to PATH, but skip the WSL shim.
        where = shutil.which("bash")
        if where and "system32" not in where.lower():
            return where
        return None
    return shutil.which("bash")


def _run_bash(script: Path, bash: str) -> int:
    # Git Bash on Windows understands POSIX paths; pass as-is via bash.
    return subprocess.call([bash, str(script)])


def _run_python(script: Path, extra_args: list[str]) -> int:
    return subprocess.call([sys.executable, str(script), *extra_args])


def main(argv: list[str] | None = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]

    print("==========================================")
    print("  OpenCode - Complete Setup")
    print("==========================================")
    print("")

    # Step 0: User configuration (identity + OS) — always runs, Enter keeps existing.
    print("Step 0/4: Configure user identity and OS")
    print("------------------------------------------")

    if not USER_CONFIG_SCRIPT.is_file():
        print(f"ERROR: user-config-claude.sh not found at {USER_CONFIG_SCRIPT}")
        return 1

    bash = _find_bash()
    if bash is None:
        print("ERROR: bash not found (needed for steps 0-1).")
        if os.name == "nt":
            print("Install Git for Windows (includes Git Bash) and re-run.")
        return 1

    if _run_bash(USER_CONFIG_SCRIPT, bash) != 0:
        print("")
        print("ERROR: User configuration failed. Aborting.")
        return 1

    print("")

    # Step 1: Compile core memory and write to AGENTS.md
    print("Step 1/4: Compile core memory -> ~/.config/opencode/AGENTS.md")
    print("------------------------------------------")

    if not COMPILE_WRITE_SCRIPT.is_file():
        print(f"ERROR: compile-write-to-opencode.sh not found at {COMPILE_WRITE_SCRIPT}")
        return 1

    if _run_bash(COMPILE_WRITE_SCRIPT, bash) != 0:
        print("")
        print("ERROR: Core memory compilation failed. Aborting.")
        return 1

    print("")

    # Step 2: Setup all procedures as OpenCode skills
    print("Step 2/4: Setup procedures -> ~/.config/opencode/skills/")
    print("------------------------------------------")

    if not SETUP_SKILLS_SCRIPT.is_file():
        print(f"ERROR: setup-all-opencode.py not found at {SETUP_SKILLS_SCRIPT}")
        return 1

    if _run_python(SETUP_SKILLS_SCRIPT, []) != 0:
        print("")
        print("ERROR: Procedure setup failed.")
        return 1

    print("")

    # Step 3: Configure opencode.jsonc (bypass permissions)
    print("Step 3/4: Configure settings -> ~/.config/opencode/opencode.jsonc")
    print("------------------------------------------")

    if not SETUP_SETTINGS_SCRIPT.is_file():
        print(f"ERROR: setup-settings-opencode.py not found at {SETUP_SETTINGS_SCRIPT}")
        return 1

    passthrough = ["--yes"] if "--yes" in args else []
    if _run_python(SETUP_SETTINGS_SCRIPT, passthrough) != 0:
        print("")
        print("ERROR: Settings setup failed.")
        return 1

    print("")
    print("==========================================")
    print("  Setup Complete!")
    print("==========================================")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
