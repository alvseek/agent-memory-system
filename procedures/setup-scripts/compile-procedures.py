"""Compile every seam-bearing memory procedure into self-contained previews.

A standalone verification tool for the control-files framework — **no Munnin /
server dependency**. For each procedure that carries a ``## Storage Mechanics``
seam, it emits the procedure composed with **each** storage backend
(markdown + db): the ``## Storage Mechanics`` body is swapped for the backend's
``## [procedure]`` section (the seam substitution documented in
``procedures/memory/storage-backends/README.md``). The output mirrors exactly what
Munnin serves — ``§ template`` stays a **reference** (templates are a separate
Resource / file, single source of truth), never inlined into the procedure.

It also reports **coverage**: any ``§ op`` a procedure references that the chosen
backend does not define. The seam contract requires both backends to implement
the same op set a procedure references, so an unresolved op is a real gap.

The seam substitution itself lives once in ``../memory/storage-backends/seam.py``
(beside the seam contract README); this script imports it. Deliberately independent
of Munnin so the public framework tree can be verified without the server.

Run (from the control-files root)::

    python procedures/setup-scripts/compile-procedures.py \
        [--backend {markdown,db}] [--content-root DIR] [--out DIR] [--strict]

Output: with no ``--backend``, ``<out>/<procedure>.<backend>.md`` for every seam
procedure x backend — a faithful dual preview. With ``--backend NAME``, the installable
command set as plain ``<out>/<procedure>.md`` (seam commands composed with that one
backend, non-seam commands copied as-is) — what the Claude Code installer consumes.
Default out: ``procedures/output/``. ``--strict`` exits non-zero when any op is unresolved.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
from dataclasses import dataclass, field
from pathlib import Path

# control-files/ root (this script lives at procedures/setup-scripts/compile-procedures.py).
_CF_ROOT = Path(__file__).resolve().parents[2]

# The seam substitution lives once, beside the contract; import it from there.
_spec = importlib.util.spec_from_file_location(
    "cf_seam", _CF_ROOT / "procedures/memory/storage-backends/seam.py"
)
_seam = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_seam)
STORAGE_MARKER = _seam.STORAGE_MARKER
extract_section = _seam.extract_section
substitute_storage_mechanics = _seam.substitute_storage_mechanics

BACKENDS = ("markdown", "db")
_BACKEND_REL = "procedures/memory/storage-backends/{name}.md"

# `§ op-name` — the abstract op reference/definition token used across the seam.
_OP_RE = re.compile(r"§\s*([a-z][a-z0-9-]*)")
_OP_DEF_RE = re.compile(r"^#{1,6}\s*§\s*([a-z][a-z0-9-]*)", re.MULTILINE)


# --- compile ---


@dataclass
class ProcedureReport:
    """Per (procedure, backend) compile outcome."""

    name: str
    backend: str
    out_path: Path
    unresolved_ops: list[str] = field(default_factory=list)
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


# The dirs whose ``*.md`` install as slash commands: top-level ``procedures/`` and
# ``procedures/memory/`` (non-recursive) — the exact set the Claude Code installer copies.
_COMMAND_SUBDIRS = ("", "memory")


def _command_procedures(proc_dir: Path) -> list[Path]:
    """The installable command set — ``*.md`` directly in ``procedures/`` and
    ``procedures/memory/``, sorted.

    Used for single-backend output: seam-bearing commands get composed, the rest are
    copied as-is, so the output equals the command set with no extras (the installer can
    then copy every plain ``<name>.md`` blindly).
    """
    files: list[Path] = []
    for sub in _COMMAND_SUBDIRS:
        files.extend((proc_dir / sub).glob("*.md"))
    return sorted(files)


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


def compile_procedure(
    core: str, backend_doc: str, name: str, backend: str
) -> tuple[str, list[str], str]:
    """Compose ``core`` with one backend's ``## [procedure]`` section.

    Returns (text, unresolved_ops, note). ``§ template`` is left as a reference —
    templates live once as a separate Resource / file, never inlined here.
    """
    referenced = _referenced_ops(core)
    try:
        section = extract_section(backend_doc, name)
    except KeyError:
        note = f"no '## {name}' section in {backend}.md — core served verbatim"
        return core, sorted(referenced), note
    composed = substitute_storage_mechanics(core, section)
    unresolved = sorted(referenced - set(_OP_DEF_RE.findall(section)))
    return composed, unresolved, ""


def _defines(backend_doc: str, name: str) -> bool:
    """True when a backend doc has a ``## {name}`` section for this procedure."""
    header = f"## {name}"
    return any(line.strip() == header for line in backend_doc.splitlines())


def compile_all(
    content_root: Path, out_dir: Path, backend: str | None = None
) -> tuple[list[ProcedureReport], list[str]]:
    """Compile procedures into ``out_dir``. Returns ``(reports, skipped_names)``.

    ``backend=None`` (dual / preview): every wired seam procedure found recursively is
    composed against **both** backends → ``<name>.<backend>.md``. A seam procedure no
    backend defines (a WIP/experimental copy) is skipped + reported.

    ``backend='markdown'|'db'`` (single / install-ready): the installable command set
    (``procedures/*.md`` + ``procedures/memory/*.md``) is emitted as plain ``<name>.md`` —
    seam commands composed against the one backend, non-seam commands copied as-is. A
    seam command this backend defines no section for is skipped + reported.
    """
    proc_dir = content_root / "procedures"
    out_dir.mkdir(parents=True, exist_ok=True)

    reports: list[ProcedureReport] = []
    skipped: list[str] = []

    if backend is None:
        backend_docs = {
            b: (content_root / _BACKEND_REL.format(name=b)).read_text(encoding="utf-8")
            for b in BACKENDS
        }
        for proc in _seam_procedures(proc_dir):
            name = proc.stem
            if not any(_defines(backend_docs[b], name) for b in BACKENDS):
                skipped.append(name)  # seam marker but no backend implements it
                continue
            core = proc.read_text(encoding="utf-8")
            for b in BACKENDS:
                text, unresolved, note = compile_procedure(core, backend_docs[b], name, b)
                out_path = out_dir / f"{name}.{b}.md"
                out_path.write_text(text, encoding="utf-8", newline="\n")
                reports.append(ProcedureReport(name, b, out_path, unresolved, note))
        return reports, skipped

    backend_doc = (content_root / _BACKEND_REL.format(name=backend)).read_text(encoding="utf-8")
    for proc in _command_procedures(proc_dir):
        name = proc.stem
        core = proc.read_text(encoding="utf-8")
        if _has_seam(core):
            if not _defines(backend_doc, name):
                skipped.append(name)  # seam marker but this backend has no section
                continue
            text, unresolved, note = compile_procedure(core, backend_doc, name, backend)
        else:
            text, unresolved, note = core, [], "copied as-is (no seam)"
        out_path = out_dir / f"{name}.md"
        out_path.write_text(text, encoding="utf-8", newline="\n")
        reports.append(ProcedureReport(name, backend, out_path, unresolved, note))
    return reports, skipped


def _print_summary(
    reports: list[ProcedureReport], skipped: list[str], out_dir: Path, backend: str | None = None
) -> int:
    """Print a per-procedure table + coverage warnings. Returns unresolved count."""
    cols = (backend,) if backend else BACKENDS
    procs = sorted({r.name for r in reports})
    label = backend if backend else f"{len(BACKENDS)} backends"
    print(f"\nCompiled {len(procs)} procedures ({label}) -> {out_dir}\n")
    if skipped:
        print(f"Skipped (seam marker, but no backend section): {', '.join(sorted(skipped))}\n")
    print(f"{'procedure':<24} " + " ".join(f"{c:<12}" for c in cols))
    print(f"{'-' * 24} " + " ".join("-" * 12 for _ in cols))
    by_key = {(r.name, r.backend): r for r in reports}
    total_unresolved = 0
    for name in procs:
        cells = []
        for c in cols:
            r = by_key.get((name, c))
            if r is None:
                cells.append("-")
            elif r.unresolved_ops:
                cells.append(f"{len(r.unresolved_ops)} UNRESOLVED")
                total_unresolved += len(r.unresolved_ops)
            elif r.note.startswith("copied"):
                cells.append("as-is")
            else:
                cells.append("ok")
        print(f"{name:<24} " + " ".join(f"{c:<12}" for c in cells))

    warned = [
        r
        for r in reports
        if r.unresolved_ops or (r.note and not r.note.startswith("copied"))
    ]
    if warned:
        print("\nDetails:")
        for r in warned:
            if r.unresolved_ops:
                print(f"  ! {r.name} [{r.backend}] unresolved ops: {', '.join(r.unresolved_ops)}")
            if r.note and not r.note.startswith("copied"):
                print(f"  * {r.name} [{r.backend}] {r.note}")
    print()
    return total_unresolved


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--backend", choices=BACKENDS, default=None,
        help="compile a single backend to <procedure>.md (default: both backends, as "
             "<procedure>.<backend>.md — a faithful dual preview)",
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

    reports, skipped = compile_all(args.content_root, out_dir, args.backend)
    unresolved = _print_summary(reports, skipped, out_dir, args.backend)
    return 1 if args.strict and unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
