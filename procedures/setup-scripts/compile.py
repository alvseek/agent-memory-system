"""Compile every seam-bearing memory procedure into self-contained previews.

A standalone verification tool for the control-files framework — **no Munnin /
server dependency**. For each procedure that carries a ``## Storage Mechanics``
seam, it emits the procedure composed with **each** storage backend
(markdown + db):

- the ``## Storage Mechanics`` body is swapped for the backend's ``## [procedure]``
  section (the seam substitution documented in
  ``procedures/memory/storage-backends/README.md``);
- referenced ``resources/*.md`` templates are inlined as a bottom appendix and
  their references rewritten to in-doc anchors, so the whole resolved procedure
  reads top-to-bottom with no pointers to chase.

It also reports **coverage**: any ``§ op`` a procedure references that the chosen
backend does not define. The seam contract requires both backends to implement
the same op set a procedure references, so an unresolved op is a real gap.

The seam substitution itself lives once in ``../memory/storage-backends/compose.py``
(beside the seam contract README); this script imports it. Deliberately independent
of Munnin so the public framework tree can be verified without the server.

Run (from the control-files root)::

    python procedures/setup-scripts/compile.py [--content-root DIR] [--out DIR] [--strict]

Output: ``<out>/<procedure>.<backend>.md`` for every procedure x backend (default
``procedures/output/``), plus a printed summary. ``--strict`` exits non-zero when
any op is unresolved.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
from dataclasses import dataclass, field
from pathlib import Path

# control-files/ root (this script lives at procedures/setup-scripts/compile.py).
_CF_ROOT = Path(__file__).resolve().parents[2]

# The seam substitution lives once, beside the contract; import it from there.
_spec = importlib.util.spec_from_file_location(
    "cf_seam_compose", _CF_ROOT / "procedures/memory/storage-backends/compose.py"
)
_compose = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_compose)
STORAGE_MARKER = _compose.STORAGE_MARKER
extract_section = _compose.extract_section
substitute_storage_mechanics = _compose.substitute_storage_mechanics

BACKENDS = ("markdown", "db")
_BACKEND_REL = "procedures/memory/storage-backends/{name}.md"
_RESOURCES_REL = "procedures/memory/resources"

# `§ op-name` — the abstract op reference/definition token used across the seam.
_OP_RE = re.compile(r"§\s*([a-z][a-z0-9-]*)")
_OP_DEF_RE = re.compile(r"^#{1,6}\s*§\s*([a-z][a-z0-9-]*)", re.MULTILINE)
# A `resources/<stem>.md` path (markdown backend + create-episode `cp`).
_RES_PATH_RE = re.compile(r"resources/([a-z0-9-]+)\.md")


# --- compile ---


@dataclass
class ProcedureReport:
    """Per (procedure, backend) compile outcome."""

    name: str
    backend: str
    out_path: Path
    unresolved_ops: list[str] = field(default_factory=list)
    inlined_templates: list[str] = field(default_factory=list)
    note: str = ""


def _has_seam(text: str) -> bool:
    """True when a doc carries the seam as an actual ``## Storage Mechanics`` header
    (not merely the phrase in prose, as the backend contract README does)."""
    return any(line.strip() == STORAGE_MARKER for line in text.splitlines())


def _seam_procedures(proc_dir: Path) -> list[Path]:
    """Every procedure ``*.md`` that carries the storage seam, sorted.

    Excludes the seam's own machinery — ``storage-backends/`` (the backend
    definitions + contract), ``resources/`` (the templates), and ``output/``
    (this tool's own generated previews, which also carry the marker).
    """
    skip = {"storage-backends", "resources", "output"}
    return sorted(
        p
        for p in proc_dir.rglob("*.md")
        if not skip & set(p.parts) and _has_seam(p.read_text(encoding="utf-8"))
    )


def _core_without_mechanics(core: str) -> str:
    """The procedure text with its ``## Storage Mechanics`` section removed.

    Used for coverage: it isolates the ops the *procedure body* references from
    the ops the backend section *defines*.
    """
    lines = core.splitlines(keepends=True)
    start = next(
        (i for i, ln in enumerate(lines) if ln.strip() == STORAGE_MARKER), None
    )
    if start is None:
        return core
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].strip() == "---":
            end = j
            break
    return "".join(lines[:start] + lines[end:])


def _referenced_ops(core: str) -> set[str]:
    """Ops the procedure body references (mechanics section excluded)."""
    return set(_OP_RE.findall(_core_without_mechanics(core)))


def _referenced_resources(text: str, known: set[str]) -> list[str]:
    """Resource stems referenced in ``text``, unique, in first-seen order.

    Two reference shapes: a ``resources/<stem>.md`` path (markdown backend) and a
    backticked bare ``<stem>`` naming an MCP Resource (db backend).
    """
    order: list[str] = []
    seen: set[str] = set()

    def add(stem: str) -> None:
        if stem in known and stem not in seen:
            seen.add(stem)
            order.append(stem)

    for m in _RES_PATH_RE.finditer(text):
        add(m.group(1))
    for m in re.finditer(r"`([a-z0-9-]+)`", text):
        add(m.group(1))
    return order


def _inline_templates(composed: str, resources_dir: Path, known: set[str]) -> tuple[str, list[str]]:
    """Append referenced templates as an appendix and rewrite refs to anchors.

    Returns the self-contained text and the list of inlined template stems.
    """
    stems = _referenced_resources(composed, known)
    if not stems:
        return composed, []

    # Rewrite references -> in-doc anchors (path forms first, then bare backticks).
    def rewrite(text: str) -> str:
        text = re.sub(
            r"\[([^\]]+)\]\([^)]*resources/([a-z0-9-]+)\.md\)",
            lambda m: f"[{m.group(1)}](#{m.group(2)})" if m.group(2) in known else m.group(0),
            text,
        )
        text = re.sub(
            r"`[^`]*resources/([a-z0-9-]+)\.md`",
            lambda m: f"[{m.group(1)}](#{m.group(1)})" if m.group(1) in known else m.group(0),
            text,
        )
        alt = "|".join(re.escape(s) for s in stems)
        text = re.sub(rf"`({alt})`", lambda m: f"[{m.group(1)}](#{m.group(1)})", text)
        return text

    # Drop a trailing rule the backend section may carry, so the appendix adds only one.
    body = re.sub(r"(?:\n+-{3,})\s*$", "", rewrite(composed).rstrip())
    parts = [body, "", "---", "", "## Templates (inlined)", "",
             "*Inlined at compile time — the procedure above references these by anchor.*"]
    for stem in stems:
        tpl = (resources_dir / f"{stem}.md").read_text(encoding="utf-8")
        tpl = re.sub(r"\A# .*\n", "", tpl).strip("\n")  # drop a leading H1 title
        parts += ["", f"### {stem}", "", tpl]
    return "\n".join(parts) + "\n", stems


def compile_procedure(
    core: str, backend_doc: str, name: str, resources_dir: Path, known: set[str], backend: str
) -> tuple[str, list[str], list[str], str]:
    """Compose ``core`` with one backend's section + inline templates.

    Returns (text, unresolved_ops, inlined_templates, note).
    """
    referenced = _referenced_ops(core)
    try:
        section = extract_section(backend_doc, name)
    except KeyError:
        note = f"no '## {name}' section in {backend}.md — core served verbatim"
        return core, sorted(referenced), [], note
    composed = substitute_storage_mechanics(core, section)
    text, inlined = _inline_templates(composed, resources_dir, known)
    unresolved = sorted(referenced - set(_OP_DEF_RE.findall(section)))
    return text, unresolved, inlined, ""


def compile_all(content_root: Path, out_dir: Path) -> list[ProcedureReport]:
    """Compile every seam procedure x backend into ``out_dir``. Returns reports."""
    proc_dir = content_root / "procedures"
    resources_dir = content_root / _RESOURCES_REL
    known = {p.stem for p in resources_dir.glob("*.md")} if resources_dir.exists() else set()

    out_dir.mkdir(parents=True, exist_ok=True)
    backend_docs = {
        b: (content_root / _BACKEND_REL.format(name=b)).read_text(encoding="utf-8")
        for b in BACKENDS
    }

    reports: list[ProcedureReport] = []
    for proc in _seam_procedures(proc_dir):
        name = proc.stem
        core = proc.read_text(encoding="utf-8")
        for backend in BACKENDS:
            text, unresolved, inlined, note = compile_procedure(
                core, backend_docs[backend], name, resources_dir, known, backend
            )
            out_path = out_dir / f"{name}.{backend}.md"
            out_path.write_text(text, encoding="utf-8")
            reports.append(
                ProcedureReport(
                    name=name,
                    backend=backend,
                    out_path=out_path,
                    unresolved_ops=unresolved,
                    inlined_templates=inlined,
                    note=note,
                )
            )
    return reports


def _print_summary(reports: list[ProcedureReport], out_dir: Path) -> int:
    """Print a per-procedure table + coverage warnings. Returns unresolved count."""
    procs = sorted({r.name for r in reports})
    print(f"\nCompiled {len(procs)} procedures x {len(BACKENDS)} backends -> {out_dir}\n")
    print(f"{'procedure':<24} {'markdown':<10} {'db':<10}")
    print(f"{'-' * 24} {'-' * 10} {'-' * 10}")
    by_key = {(r.name, r.backend): r for r in reports}
    total_unresolved = 0
    for name in procs:
        cells = []
        for b in BACKENDS:
            r = by_key.get((name, b))
            if r is None:
                cells.append("-")
            elif r.unresolved_ops:
                cells.append(f"{len(r.unresolved_ops)} UNRESOLVED")
                total_unresolved += len(r.unresolved_ops)
            else:
                cells.append("ok")
        print(f"{name:<24} {cells[0]:<10} {cells[1]:<10}")

    warned = [r for r in reports if r.unresolved_ops or r.note]
    if warned:
        print("\nDetails:")
        for r in warned:
            if r.unresolved_ops:
                print(f"  ! {r.name} [{r.backend}] unresolved ops: {', '.join(r.unresolved_ops)}")
            if r.note:
                print(f"  * {r.name} [{r.backend}] {r.note}")
    print()
    return total_unresolved


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--content-root", type=Path, default=_CF_ROOT,
        help="control-files root (default: resolved from this script's location)",
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="output directory (default: <content-root>/procedures/output)",
    )
    parser.add_argument(
        "--strict", action="store_true", help="exit non-zero if any op is unresolved"
    )
    args = parser.parse_args(argv)

    if not (args.content_root / "procedures").exists():
        parser.error(f"no procedures/ under content root: {args.content_root}")
    out_dir = args.out or (args.content_root / "procedures" / "output")

    reports = compile_all(args.content_root, out_dir)
    unresolved = _print_summary(reports, out_dir)
    return 1 if args.strict and unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
