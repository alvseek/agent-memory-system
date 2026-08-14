"""compile-procedures — self-contained previews of every seam procedure x both backends.

Lives beside the tool it tests, inside control-files. The tool (``procedures/
setup-scripts/compile-procedures.py``) has a hyphen in its name, so it is loaded by
file path rather than imported as a module.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path

CF = Path(__file__).resolve().parents[1]  # control-files/
_SCRIPT = CF / "procedures" / "setup-scripts" / "compile-procedures.py"

_spec = importlib.util.spec_from_file_location("cf_compile", _SCRIPT)
cc = importlib.util.module_from_spec(_spec)
sys.modules["cf_compile"] = cc  # dataclass field resolution needs the module registered
_spec.loader.exec_module(cc)

# procedures every healthy tree carries — asserted by presence, not exact count (a WIP
# copy or a newly-added procedure shouldn't break the suite).
_KNOWN = {"add-reasoning", "awaken-agent", "wrap-up", "update-episodic", "load-knowledge"}

# command procedures with no seam — installed/compiled as-is, byte-for-byte from source.
_NON_SEAM = {"refresh-memory", "push-memory", "pull-memory"}


def test_discovers_seam_procedures_and_excludes_machinery() -> None:
    procs = {p.stem for p in cc._seam_procedures(CF / "procedures")}
    assert _KNOWN <= procs
    # the seam's own machinery must be excluded, even though it names the marker in prose
    assert "README" not in procs
    assert "markdown" not in procs
    assert "db" not in procs


def test_wired_procedures_compile_both_backends(tmp_path: Path) -> None:
    reports, _ = cc.compile_all(CF, tmp_path)
    names = {r.name for r in reports}
    assert _KNOWN <= names
    # every compiled procedure emits exactly its two backends
    per_backend = Counter(r.name for r in reports)
    assert all(count == 2 for count in per_backend.values())
    assert len(reports) == 2 * len(names)
    for r in reports:
        assert r.out_path.exists()


def test_every_wired_op_resolves_in_both_backends(tmp_path: Path) -> None:
    # the seam contract requires both backends to define every op a wired procedure references
    reports, _ = cc.compile_all(CF, tmp_path)
    offenders = {(r.name, r.backend): r.unresolved_ops for r in reports if r.unresolved_ops}
    assert offenders == {}


def test_unwired_procedure_is_skipped(tmp_path: Path) -> None:
    # a seam-bearing procedure that NO backend defines is ignored (not compiled), and reported.
    root = tmp_path / "cf"
    mem = root / "procedures" / "memory"
    backends = mem / "storage-backends"
    backends.mkdir(parents=True)
    seam = "## Storage Mechanics\n\n(placeholder)\n"
    (mem / "foo.md").write_text(f"# Foo\n\n{seam}", encoding="utf-8")       # wired
    (mem / "ghost.md").write_text(f"# Ghost\n\n{seam}", encoding="utf-8")   # unwired
    (backends / "markdown.md").write_text("## foo\n\n### § x\ndo x\n", encoding="utf-8")
    (backends / "db.md").write_text("## foo\n\n### § x\ntool x\n", encoding="utf-8")

    reports, skipped = cc.compile_all(root, tmp_path / "out")
    names = {r.name for r in reports}
    assert "foo" in names
    assert "ghost" not in names
    assert "ghost" in skipped


def test_markdown_and_db_swap_the_right_mechanics(tmp_path: Path) -> None:
    cc.compile_all(CF, tmp_path)
    md = (tmp_path / "add-reasoning.markdown.md").read_text(encoding="utf-8")
    db = (tmp_path / "add-reasoning.db.md").read_text(encoding="utf-8")
    # markdown backend = file/shell mechanics; db backend = tool calls.
    assert "agent-core-memory.md" in md
    assert 'powershell -c "[guid]' in md  # markdown-only generate-uuid shell op
    assert "insert(agent_id=" in db  # db-only persist tool call
    assert "insert(agent_id=" not in md


def test_templates_stay_a_reference_not_inlined(tmp_path: Path) -> None:
    # templates live once as a separate Resource/file; the output references them, never inlines.
    cc.compile_all(CF, tmp_path)
    md = (tmp_path / "add-reasoning.markdown.md").read_text(encoding="utf-8")
    db = (tmp_path / "add-reasoning.db.md").read_text(encoding="utf-8")
    for text in (md, db):
        assert "## Templates (inlined)" not in text
    # markdown references the template by path; db names it as an MCP Resource
    assert "resources/reasoning-pattern-template.md" in md
    assert "reasoning-pattern-template" in db
    # the template body itself must not be pasted into the procedure
    assert "[SHORT MEMORABLE TITLE]" not in md
    assert "[SHORT MEMORABLE TITLE]" not in db


def test_strict_exit_is_clean_on_healthy_tree(tmp_path: Path) -> None:
    rc = cc.main(["--content-root", str(CF), "--out", str(tmp_path), "--strict"])
    assert rc == 0


# --- single-backend mode: the install-ready command set ---


def test_single_backend_emits_plain_command_md(tmp_path: Path) -> None:
    # one backend → the installable command set as plain <name>.md (seam composed,
    # non-seam copied as-is), no dual-style backend infix.
    reports, _ = cc.compile_all(CF, tmp_path, backend="markdown")
    names = {r.name for r in reports}
    assert _KNOWN <= names
    assert _NON_SEAM <= names
    for r in reports:
        assert r.out_path.name == f"{r.name}.md"
        assert r.out_path.exists()
    assert not list(tmp_path.glob("*.markdown.md"))
    assert not list(tmp_path.glob("*.db.md"))


def test_single_backend_non_seam_copied_verbatim(tmp_path: Path) -> None:
    cc.compile_all(CF, tmp_path, backend="markdown")
    for name in _NON_SEAM:
        out = (tmp_path / f"{name}.md").read_text(encoding="utf-8")
        src = (CF / "procedures" / f"{name}.md").read_text(encoding="utf-8")
        assert out == src  # no seam → byte-for-byte copy


def test_single_backend_seam_is_decluttered(tmp_path: Path) -> None:
    # the compiled command has the mechanics inlined and the seam scaffolding stripped.
    cc.compile_all(CF, tmp_path, backend="markdown")
    text = (tmp_path / "awaken-agent.md").read_text(encoding="utf-8")
    assert "## Storage Mechanics" not in text  # marker header dropped
    assert "#storage-mechanics" not in text  # no dangling anchor/xref
    assert "§" in text  # op sigils kept as storage-provenance signal
    assert "agent-core-memory.md" in text  # real inlined markdown mechanics survive


def test_single_backend_db_composes_tool_calls(tmp_path: Path) -> None:
    cc.compile_all(CF, tmp_path, backend="db")
    text = (tmp_path / "add-reasoning.md").read_text(encoding="utf-8")
    assert "insert(agent_id=" in text  # db tool call inlined
    assert 'powershell -c "[guid]' not in text  # markdown-only shell op absent


def test_single_backend_main_strict_is_clean(tmp_path: Path) -> None:
    rc = cc.main(
        ["--backend", "markdown", "--content-root", str(CF), "--out", str(tmp_path), "--strict"]
    )
    assert rc == 0
