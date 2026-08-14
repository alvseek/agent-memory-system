"""Seam substitution — the reference implementation.

Each memory procedure carries one ``## Storage Mechanics`` section; serving/preview
swaps that section's body for a backend's ``## [procedure]`` section — markdown
mechanics for the native fleet, DB tools for Munnin. Pure text ops.

This is the framework's single home for that logic, defined once beside the seam
contract (``README.md``). It is Munnin-agnostic. Every consumer imports it:

- the standalone ``procedures/setup-scripts/compile-procedures.py`` preview tool (this repo);
- Munnin's ``ContentLoader`` + markdown-fidelity gate, which import this module
  from the checked-out submodule at runtime (Munnin keeps no copy of its own).
"""

from __future__ import annotations

import re

STORAGE_MARKER = "## Storage Mechanics"

# The `§` op sigil is KEPT in the composed output — it signals to the reader that a step
# was provided by the storage backend (a seam swap point), useful provenance.

# The composed procedure inlines the mechanics, so a "(see [Storage Mechanics](#…))"
# back-reference to the now-removed section is dangling + stale — drop the parenthetical;
# as a safety net, unlink any other reference to that anchor (keeping its text).
_SEAM_XREF = re.compile(r"[ \t]*\(see \[[^\]]*\]\(#storage-mechanics\)\)")
_SEAM_ANCHOR = re.compile(r"\[([^\]]*)\]\(#storage-mechanics\)")


def extract_section(doc: str, title: str) -> str:
    """Return the body under ``## {title}`` up to the next ``## `` header or EOF.

    Matches the level-2 header exactly. Raises ``KeyError`` if absent.
    """
    lines = doc.splitlines(keepends=True)
    header = f"## {title}"
    start = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            start = i + 1
            break
    if start is None:
        raise KeyError(f"section not found: {header}")
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "".join(lines[start:end]).strip("\n")


def substitute_storage_mechanics(core: str, backend_section: str) -> str:
    """Replace the core's ``## Storage Mechanics`` section with ``backend_section``.

    The seam scaffolding is trimmed from the result: the ``## Storage Mechanics`` marker
    header is **dropped** (the backend section brings its own headers) and the now-stale
    ``(see [Storage Mechanics](#…))`` back-reference is dropped (the mechanics are inlined
    here). The ``§`` op sigils are **kept** — they signal to the reader that a step is
    storage-backend-provided. So the composed procedure reads as plain content, the same
    on both faces (installed markdown command and Munnin-served prompt). Everything after
    the section up to the next ``## `` header or standalone rule is preserved (so a
    trailing footer note survives). Raises ``KeyError`` if the marker is absent.
    """
    lines = core.splitlines(keepends=True)
    start = None
    for i, line in enumerate(lines):
        if line.strip() == STORAGE_MARKER:
            start = i
            break
    if start is None:
        raise KeyError("no '## Storage Mechanics' marker in procedure")
    end = len(lines)
    for j in range(start + 1, len(lines)):
        # The mechanics body ends at the next section header or a standalone rule,
        # so trailing content (e.g. a footer note after the section) is preserved.
        if lines[j].startswith("## ") or lines[j].strip() == "---":
            end = j
            break
    head = "".join(lines[:start]).rstrip("\n")  # drop the marker header line itself
    tail = "".join(lines[end:])
    body = backend_section.strip("\n")
    composed = f"{head}\n\n{body}\n\n{tail}" if tail.strip() else f"{head}\n\n{body}\n"
    composed = _SEAM_XREF.sub("", composed)
    return _SEAM_ANCHOR.sub(r"\1", composed)
