"""The installable command set — the reference definition.

A **command** is a procedure that installs as a slash command (or its equivalent on
another host): every ``*.md`` directly in ``procedures/`` and ``procedures/memory/``.
Nothing deeper counts — ``components/`` are inlined into their callers, ``resources/``
are served as templates, ``storage-backends/`` hold the seam definitions, ``external/``
declares legacy dependencies and ``output*/`` is generated.

This is the framework's single home for that definition, beside the directory it
describes — the same rule ``memory/storage-backends/seam.py`` and ``components/inline.py``
follow. Every consumer imports it rather than keeping a copy:

- ``setup-scripts/compile-procedures.py``, and through it the host installers;
- Munnin's ``ContentLoader``, which serves the same set and reads this module from the
  checked-out submodule.
"""

from __future__ import annotations

from pathlib import Path

# Non-recursive, in this order: top-level ``procedures/`` first, then ``procedures/memory/``.
COMMAND_SUBDIRS: tuple[str, ...] = ("", "memory")


def command_procedures(proc_dir: Path) -> list[Path]:
    """Every command's source file under ``proc_dir``, sorted by path.

    Raises ``ValueError`` when two files share a stem across the command dirs: a command
    is addressed by its stem alone, so a duplicate could only be resolved by a precedence
    rule nobody stated — and silently picking one is how the wrong procedure ships.
    A superseded ``<!-- composed-procedure: -->`` pointer is refused rather than
    installed as a command: the complete document is the command now.
    """
    files: list[Path] = []
    for sub in COMMAND_SUBDIRS:
        files.extend((proc_dir / sub).glob("*.md"))
    selected = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        if text.startswith("<!-- composed-procedure:"):
            raise ValueError(f"superseded composed-procedure pointer: {path}")
        selected.append(path)
    files = sorted(selected)
    seen: dict[str, Path] = {}
    for f in files:
        if f.stem in seen:
            raise ValueError(f"duplicate command stem {f.stem!r}: {seen[f.stem]} and {f}")
        seen[f.stem] = f
    return files
