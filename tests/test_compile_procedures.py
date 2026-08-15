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

# command procedures with no seam — compiled without seam composition.
_NON_SEAM = {"refresh-memory", "push-memory", "pull-memory"}

# the subset of those that reference no component either, so compiling is a byte-for-byte
# copy. (`refresh-memory` pulls in a component, so its output legitimately differs.)
_VERBATIM = {"push-memory", "pull-memory"}


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
    for name in _VERBATIM:
        out = (tmp_path / f"{name}.md").read_text(encoding="utf-8")
        src = (CF / "procedures" / f"{name}.md").read_text(encoding="utf-8")
        assert out == src  # no seam, no components → byte-for-byte copy


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


# --- component inlining (runs before seam composition) ---

# the shared no-sub-agent rule, referenced by /awaken-agent and /refresh-memory
_COMPONENT_MARKER = "sub-agents return summaries"


def test_components_are_inlined_into_compiled_commands(tmp_path: Path) -> None:
    cc.compile_all(CF, tmp_path, backend="markdown")
    for name in ("awaken-agent", "refresh-memory"):  # seam and non-seam caller
        text = (tmp_path / f"{name}.md").read_text(encoding="utf-8")
        assert _COMPONENT_MARKER in text.lower(), name  # body pulled in
        assert "CRITICAL" in text, name  # caller's own label survives the de-link


def test_no_component_reference_survives_compilation(tmp_path: Path) -> None:
    # an installed command must not point at a components/ file the agent can't reach
    for backend in (None, "markdown", "db"):
        out = tmp_path / (backend or "dual")
        cc.compile_all(CF, out, backend=backend)
        for path in out.glob("*.md"):
            assert "components/" not in path.read_text(encoding="utf-8"), path.name


def test_components_are_not_compiled_as_procedures(tmp_path: Path) -> None:
    # components/ is machinery: never a seam procedure, never an installed command
    assert not any(
        p.parent.name == "components" for p in cc._seam_procedures(CF / "procedures")
    )
    reports, _ = cc.compile_all(CF, tmp_path, backend="markdown")
    assert "inline" not in {r.name for r in reports}
    assert "no-subagent-load" not in {r.name for r in reports}


def test_generated_output_is_never_recompiled_as_source(tmp_path: Path) -> None:
    # --out / --emit-inline may point inside the source tree; the emitted files carry the
    # seam marker, so a later run must not mistake them for procedures and double-compile.
    out, mid = CF / "procedures" / "output", CF / "procedures" / "output-inline"
    discovered = cc._seam_procedures(CF / "procedures", (out, mid))
    assert len(discovered) == len({p.stem for p in discovered})  # no duplicate stems
    assert not any("output" in p.parts[-2] for p in discovered)

    reports, _ = cc.compile_all(CF, tmp_path / "o", emit_inline=tmp_path / "i")
    per_name = Counter(r.name for r in reports)
    assert all(count == 2 for count in per_name.values())  # exactly one pair per procedure


def test_intermediate_defaults_beside_the_output_and_is_always_written(tmp_path: Path) -> None:
    # not opt-in: a run that never asked for it still refreshes the intermediate, so it
    # can't sit stale beside a newer compiled output.
    out = tmp_path / "output"
    cc.compile_all(CF, out, backend="markdown")
    assert (tmp_path / "output-inline" / "awaken-agent.md").exists()


def test_emit_inline_writes_the_pre_seam_intermediate(tmp_path: Path) -> None:
    out, mid = tmp_path / "out", tmp_path / "inline"
    cc.compile_all(CF, out, backend="markdown", emit_inline=mid)
    staged = mid / "awaken-agent.md"
    assert staged.exists()
    text = staged.read_text(encoding="utf-8")
    assert _COMPONENT_MARKER in text.lower()  # component already inlined
    assert "## Storage Mechanics" in text  # seam not yet composed
    assert (mid / "memory" / "update-episodic.md").exists()  # source tree mirrored


# --- component-contributed storage ops (backend section composed from procedure + components) ---


def test_component_ops_are_defined_once_and_serve_every_caller(tmp_path: Path) -> None:
    # the awakening-protocol component is inlined into two procedures; its ops live in ONE
    # backend section (`## core-instruction-control-files`), not repeated under each caller.
    backend = (CF / "procedures/memory/storage-backends/markdown.md").read_text(encoding="utf-8")
    headers = [ln.strip() for ln in backend.splitlines() if ln.startswith("## ")]
    assert headers.count("## core-instruction-control-files") == 1
    assert "## awaken-agent" not in headers  # not restated per caller
    assert "## refresh-memory" not in headers

    cc.compile_all(CF, tmp_path, backend="markdown")
    for name in ("awaken-agent", "refresh-memory"):
        text = (tmp_path / f"{name}.md").read_text(encoding="utf-8")
        assert "§ load-agent-memory" in text, name
        assert "§ recover-missing-foundations" in text, name  # arrived via the component
        assert "## Storage Mechanics" not in text, name


def test_backends_disagree_on_the_component_ops(tmp_path: Path) -> None:
    # the point of decoupling: the same op means different things per backend
    cc.compile_all(CF, tmp_path)
    md = (tmp_path / "awaken-agent.markdown.md").read_text(encoding="utf-8")
    db = (tmp_path / "awaken-agent.db.md").read_text(encoding="utf-8")
    assert "new-agent-template/shared-memory/" in md  # markdown recovers by copying files
    assert "new-agent-template/shared-memory/" not in db
    assert "truncated in transit" in db  # db's failure mode is a silent payload cap
    assert "latest_episode" in db  # db already has the episode; markdown must read it
    assert "episodes/" in md


def test_component_can_supply_ops_for_a_procedure_the_backend_never_names(tmp_path: Path) -> None:
    root = tmp_path / "cf"
    procs = root / "procedures"
    comps = procs / "components"
    backends = procs / "memory" / "storage-backends"
    backends.mkdir(parents=True)
    comps.mkdir(parents=True)
    (comps / "shared-step.md").write_text(
        "# Shared Step (component)\n\nx\n\n---\n\nDo it (**§ shared-op**).\n", encoding="utf-8"
    )
    (procs / "foo.md").write_text(
        "# Foo\n\n[Shared step](components/shared-step.md)\n\n## Storage Mechanics\n\n(swapped)\n",
        encoding="utf-8",
    )
    # the backend names the COMPONENT only — never `## foo`
    (backends / "markdown.md").write_text(
        "## shared-step\n\n### § shared-op\n\nread the file\n", encoding="utf-8"
    )

    reports, skipped = cc.compile_all(root, tmp_path / "out", backend="markdown")
    assert skipped == []  # covered by the component, so not skipped
    assert [r.unresolved_ops for r in reports] == [[]]  # and the op resolves
    text = (tmp_path / "out" / "foo.md").read_text(encoding="utf-8")
    assert "read the file" in text


def test_missing_component_is_reported_and_fails_strict(tmp_path: Path) -> None:
    root = tmp_path / "cf"
    mem = root / "procedures" / "memory"
    backends = mem / "storage-backends"
    backends.mkdir(parents=True)
    (root / "procedures" / "foo.md").write_text(
        "# Foo\n\n[label](components/ghost.md)\n", encoding="utf-8"
    )
    (backends / "markdown.md").write_text("## nothing\n", encoding="utf-8")

    reports, _ = cc.compile_all(root, tmp_path / "out", backend="markdown")
    assert [r.missing_components for r in reports] == [["ghost"]]
    rc = cc.main(
        ["--backend", "markdown", "--content-root", str(root),
         "--out", str(tmp_path / "out2"), "--strict"]
    )
    assert rc == 1
