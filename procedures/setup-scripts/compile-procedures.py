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

Before the seam is composed, every **component** reference is inlined (a shared fragment
under ``procedures/components/``, replaced at its reference point so the delivered
procedure is self-contained). Components are inlined first so an ``§ op`` arriving inside
one is counted by the coverage check below.

None of the framework's definitions are implemented here: the seam lives once in
``../memory/storage-backends/seam.py``, component inlining once in
``../components/inline.py``, and the command set — which ``*.md`` files install as
commands — once in ``../command_set.py``, each beside its own contract; this script
imports all three, as Munnin's ``ContentLoader`` does. Deliberately independent of Munnin
so the public framework tree can be verified without the server.

Run (from the control-files root)::

    python procedures/setup-scripts/compile-procedures.py \
        [--backend {markdown,db}] [--content-root DIR] [--out DIR] \
        [--emit-inline DIR] [--strict]

Output: with no ``--backend``, ``<out>/<procedure>.<backend>.md`` for every seam
procedure x backend — a faithful dual preview. With ``--backend NAME``, the installable
command set as plain ``<out>/<procedure>.md`` (seam commands composed with that one
backend, non-seam commands copied as-is) — what the Claude Code installer consumes.
Default out: ``procedures/output/``. Each run **also** writes the intermediate stage — every
procedure after component inlining but before seam composition — to the sibling
``procedures/output-inline/``, so what a component contributed is always inspectable and
can never lag behind the compiled output. ``--emit-inline DIR`` relocates it. ``--strict``
exits non-zero when any op is unresolved or any referenced component is missing.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
from dataclasses import dataclass, field
from pathlib import Path

# control-files/ root (this script lives at procedures/setup-scripts/compile-procedures.py).
_CF_ROOT = Path(__file__).resolve().parents[2]

def _load(name: str, rel: str):
    """Import a framework module that lives beside its own contract, by file path."""
    spec = importlib.util.spec_from_file_location(name, _CF_ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Every definition lives once, beside its contract; import them from there.
_seam = _load("cf_seam", "procedures/memory/storage-backends/seam.py")
STORAGE_MARKER = _seam.STORAGE_MARKER
extract_section = _seam.extract_section
substitute_storage_mechanics = _seam.substitute_storage_mechanics
compose_backend_section = _seam.compose_backend_section
defines_section = _seam.defines_section
has_seam = _seam.has_seam

_inline = _load("cf_inline", "procedures/components/inline.py")
inline_components = _inline.inline_components

_command_set = _load("cf_command_set", "procedures/command_set.py")
command_procedures = _command_set.command_procedures

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
    missing_components: list[str] = field(default_factory=list)


def _seam_procedures(proc_dir: Path, generated: tuple[Path, ...] = ()) -> list[Path]:
    """Every procedure ``*.md`` that carries the storage seam, sorted.

    Excludes the framework's own machinery — ``storage-backends/`` (the backend
    definitions + contract), ``resources/`` (the templates), and ``components/`` (shared
    fragments, inlined into their callers rather than compiled).

    Also excludes this tool's **own generated output**, which carries the marker too and
    would otherwise be recompiled as if it were source: any ``output*`` directory by name,
    plus whatever ``generated`` paths the caller was pointed at (``--out`` / ``--emit-inline``
    can be written anywhere, including inside the source tree).
    """
    skip = {"storage-backends", "resources", "components"}
    roots = tuple(p.resolve() for p in generated)

    def _is_generated(path: Path) -> bool:
        if any(part.startswith("output") for part in path.parts):
            return True
        resolved = path.resolve()
        return any(resolved.is_relative_to(root) for root in roots)

    return sorted(
        p
        for p in proc_dir.rglob("*.md")
        if not skip & set(p.parts)
        and not _is_generated(p)
        and has_seam(p.read_text(encoding="utf-8"))
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


def compile_procedure(
    core: str, backend_doc: str, name: str, backend: str, components: tuple[str, ...] = ()
) -> tuple[str, list[str], str]:
    """Compose ``core`` with one backend's section for this procedure.

    The backend body is the procedure's own ``## [procedure]`` section plus a
    ``## [component]`` section for each component inlined into it, so ops arriving via a
    component resolve without being restated under every caller.

    Returns (text, unresolved_ops, note). ``§ template`` is left as a reference —
    templates live once as a separate Resource / file, never inlined here.
    """
    referenced = _referenced_ops(core)
    try:
        section = compose_backend_section(backend_doc, name, components)
    except KeyError:
        note = f"no '## {name}' section in {backend}.md — core served verbatim"
        return core, sorted(referenced), note
    composed = substitute_storage_mechanics(core, section)
    unresolved = sorted(referenced - set(_OP_DEF_RE.findall(section)))
    return composed, unresolved, ""


def _backend_covers(backend_doc: str, name: str, components: tuple[str, ...]) -> bool:
    """True when a backend says anything about this procedure — under its own name, or
    under one of the components inlined into it."""
    return defines_section(backend_doc, name) or any(
        defines_section(backend_doc, c) for c in components
    )


def _inline_source(
    proc: Path, comp_dir: Path, proc_dir: Path, emit_inline: Path
) -> tuple[str, list[str], tuple[str, ...]]:
    """Read a procedure and inline its components — the stage before seam composition.

    The inlined-but-not-yet-composed text is also written to ``emit_inline``, mirroring the
    source tree: the intermediate stage is a product of every run, not an opt-in, so it can
    never sit stale beside a newer compiled output.
    """
    core, missing, used = inline_components(proc.read_text(encoding="utf-8"), comp_dir)
    dest = emit_inline / proc.relative_to(proc_dir)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(core, encoding="utf-8", newline="\n")
    return core, missing, tuple(dict.fromkeys(used))  # de-duplicated, order preserved


def _inline_dir(out_dir: Path, emit_inline: Path | None) -> Path:
    """Where the pre-seam intermediate goes: ``<out>-inline`` beside the output by default."""
    return emit_inline or out_dir.parent / f"{out_dir.name}-inline"


def compile_all(
    content_root: Path,
    out_dir: Path,
    backend: str | None = None,
    emit_inline: Path | None = None,
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
    comp_dir = proc_dir / "components"
    emit_inline = _inline_dir(out_dir, emit_inline)
    out_dir.mkdir(parents=True, exist_ok=True)

    reports: list[ProcedureReport] = []
    skipped: list[str] = []

    if backend is None:
        backend_docs = {
            b: (content_root / _BACKEND_REL.format(name=b)).read_text(encoding="utf-8")
            for b in BACKENDS
        }
        for proc in _seam_procedures(proc_dir, (out_dir, emit_inline)):
            name = proc.stem
            # inline first: a component may be what brings this procedure's ops
            core, missing, used = _inline_source(proc, comp_dir, proc_dir, emit_inline)
            if not any(_backend_covers(backend_docs[b], name, used) for b in BACKENDS):
                skipped.append(name)  # seam marker but no backend implements it
                continue
            for b in BACKENDS:
                text, unresolved, note = compile_procedure(core, backend_docs[b], name, b, used)
                # a backend section may carry component references of its own
                text, from_backend, _ = inline_components(text, comp_dir)
                out_path = out_dir / f"{name}.{b}.md"
                out_path.write_text(text, encoding="utf-8", newline="\n")
                reports.append(
                    ProcedureReport(
                        name, b, out_path, unresolved, note, sorted(set(missing + from_backend))
                    )
                )
        return reports, skipped

    backend_doc = (content_root / _BACKEND_REL.format(name=backend)).read_text(encoding="utf-8")
    for proc in command_procedures(proc_dir):
        name = proc.stem
        core, missing, used = _inline_source(proc, comp_dir, proc_dir, emit_inline)
        if has_seam(core):
            if not _backend_covers(backend_doc, name, used):
                skipped.append(name)  # seam marker but this backend has no section
                continue
            text, unresolved, note = compile_procedure(core, backend_doc, name, backend, used)
            text, from_backend, _ = inline_components(text, comp_dir)
            missing = sorted(set(missing + from_backend))
        else:
            text, unresolved, note = core, [], "copied as-is (no seam)"
        out_path = out_dir / f"{name}.md"
        out_path.write_text(text, encoding="utf-8", newline="\n")
        reports.append(ProcedureReport(name, backend, out_path, unresolved, note, missing))
    return reports, skipped


def _print_summary(
    reports: list[ProcedureReport], skipped: list[str], out_dir: Path, backend: str | None = None
) -> int:
    """Print a per-procedure table + coverage warnings.

    Returns the problem count: unresolved seam ops plus unresolved component references.
    """
    cols = (backend,) if backend else BACKENDS
    procs = sorted({r.name for r in reports})
    label = backend if backend else f"{len(BACKENDS)} backends"
    print(f"\nCompiled {len(procs)} procedures ({label}) -> {out_dir}\n")
    if skipped:
        print(f"Skipped (seam marker, but no backend section): {', '.join(sorted(skipped))}\n")
    print(f"{'procedure':<24} " + " ".join(f"{c:<12}" for c in cols))
    print(f"{'-' * 24} " + " ".join("-" * 12 for _ in cols))
    by_key = {(r.name, r.backend): r for r in reports}
    problems = 0
    for name in procs:
        cells = []
        for c in cols:
            r = by_key.get((name, c))
            if r is None:
                cells.append("-")
            elif r.unresolved_ops or r.missing_components:
                problems += len(r.unresolved_ops) + len(r.missing_components)
                kinds = []
                if r.unresolved_ops:
                    kinds.append(f"{len(r.unresolved_ops)} OP")
                if r.missing_components:
                    kinds.append(f"{len(r.missing_components)} COMP")
                cells.append("/".join(kinds) + " MISSING")
            elif r.note.startswith("copied"):
                cells.append("as-is")
            else:
                cells.append("ok")
        print(f"{name:<24} " + " ".join(f"{c:<12}" for c in cells))

    warned = [
        r
        for r in reports
        if r.unresolved_ops
        or r.missing_components
        or (r.note and not r.note.startswith("copied"))
    ]
    if warned:
        print("\nDetails:")
        for r in warned:
            if r.unresolved_ops:
                print(f"  ! {r.name} [{r.backend}] unresolved ops: {', '.join(r.unresolved_ops)}")
            if r.missing_components:
                print(
                    f"  ! {r.name} [{r.backend}] missing components: "
                    f"{', '.join(r.missing_components)}"
                )
            if r.note and not r.note.startswith("copied"):
                print(f"  * {r.name} [{r.backend}] {r.note}")
    print()
    return problems


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
        "--emit-inline", type=Path, default=None,
        help="where to write the pre-seam intermediate — each procedure after component "
             "inlining, mirroring the source tree (default: <out>-inline, i.e. "
             "procedures/output-inline/). Always written, so it cannot go stale.",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="exit non-zero if any op is unresolved or any referenced component is missing",
    )
    args = parser.parse_args(argv)

    if not (args.content_root / "procedures").exists():
        parser.error(f"no procedures/ under content root: {args.content_root}")
    out_dir = args.out or (args.content_root / "procedures" / "output")

    reports, skipped = compile_all(args.content_root, out_dir, args.backend, args.emit_inline)
    problems = _print_summary(reports, skipped, out_dir, args.backend)
    print(f"Pre-seam intermediate -> {_inline_dir(out_dir, args.emit_inline)}\n")
    return 1 if args.strict and problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
