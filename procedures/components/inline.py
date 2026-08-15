"""Component inlining — the reference implementation.

A **component** is a reusable procedural fragment under ``procedures/components/``.
It is never installed as a slash command and never served on its own: a procedure
references one by markdown link, and at delivery the link is replaced by its label
text and the component's body is inserted right after. The delivered procedure is
therefore self-contained — it carries no reference to a file the agent cannot reach.

Reference form (the path prefix is free — relative for dev-time click-through, or a
placeholder path; only the ``components/<name>.md`` tail is matched)::

    [🚨 **Load-into-own-context rule**](components/no-subagent-load.md)

This is the framework's single home for that logic, defined once beside the components
it serves — the same rule ``seam.py`` follows for the storage seam. Every consumer
imports it rather than keeping a copy:

- the standalone ``procedures/setup-scripts/compile-procedures.py`` tool, which produces
  the installed slash commands;
- Munnin's ``ContentLoader``, which serves the same procedures as MCP Prompts and reads
  this module from the checked-out submodule.

**Ordering**: inline components BEFORE seam substitution. The seam's coverage check
counts the ``§ op`` references in the procedure body, so an op that arrives inside a
component has to be part of that body before the check runs.
"""

from __future__ import annotations

import re
from pathlib import Path

# `[label](<anything>/components/<name>.md)` — the prefix is ignored so a relative
# dev-time link and a placeholder-rooted one both resolve to the same component.
_COMPONENT_LINK = re.compile(r"\[([^\]]*)\]\((?:[^)\s]*/)?components/([a-z][a-z0-9-]*)\.md\)")


def component_body(text: str) -> str:
    """The inlinable body of a component document.

    A component opens with a header block (title + a note that it is a component, not a
    standalone skill) separated from the body by a standalone ``---`` rule; only what
    follows that rule is inlined. Without the rule, the whole document is used minus a
    leading ``# `` title — so a header-less fragment still inlines sensibly.
    """
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.strip() == "---":
            return "".join(lines[i + 1 :]).strip("\n")
    if lines and lines[0].startswith("# "):
        return "".join(lines[1:]).strip("\n")
    return text.strip("\n")


def inline_components(
    text: str, components_dir: Path, _stack: tuple[str, ...] = ()
) -> tuple[str, list[str], list[str]]:
    """Inline every component reference in ``text`` at its reference point.

    Returns ``(text, missing, used)``. For each referencing line the links are replaced
    by their label text (so a caller's own wording in the sentence survives) and each
    component body is inserted right after, in reference order. Components may reference
    other components; recursion is cycle-guarded.

    A component whose file is absent — or that would close a cycle — leaves its line
    **untouched**, so the unresolved link stays visible, and its name is returned in
    ``missing`` for the caller to surface. Nothing fails silently.
    """
    out: list[str] = []
    missing: list[str] = []
    used: list[str] = []

    for line in text.splitlines(keepends=True):
        matches = list(_COMPONENT_LINK.finditer(line))
        if not matches:
            out.append(line)
            continue

        names = [m.group(2) for m in matches]
        resolved: list[tuple[str, str]] = []
        for name in names:
            if name in _stack:
                missing.append(f"{name} (circular reference)")
                continue
            path = components_dir / f"{name}.md"
            if not path.is_file():
                missing.append(name)
                continue
            body, sub_missing, sub_used = inline_components(
                component_body(path.read_text(encoding="utf-8")),
                components_dir,
                _stack + (name,),
            )
            missing.extend(sub_missing)
            used.extend(sub_used)
            used.append(name)
            resolved.append((name, body))

        if len(resolved) != len(names):
            out.append(line)  # unresolved reference — leave it visible
            continue

        delinked = _COMPONENT_LINK.sub(r"\1", line)
        out.append(delinked if delinked.endswith("\n") else delinked + "\n")
        for _, body in resolved:
            out.append("\n" + body + "\n")

    return "".join(out), missing, used
