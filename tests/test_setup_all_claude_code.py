"""Tests for setup-all-claude-code.py — the Python slash-command installer.

Loaded by file path (hyphenated name). Every install() call is pointed at tmp dirs so the
real ~/.claude/commands and the shared procedures/output/ are never touched.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

CF = Path(__file__).resolve().parents[1]  # control-files/
_SCRIPT = CF / "procedures" / "setup-scripts" / "setup-all-claude-code.py"

_spec = importlib.util.spec_from_file_location("cf_setup", _SCRIPT)
si = importlib.util.module_from_spec(_spec)
sys.modules["cf_setup"] = si
_spec.loader.exec_module(si)

_KNOWN = {
    "awaken-agent", "wrap-up", "add-reasoning", "update-episodic",
    "load-knowledge", "create-agent",
}
_NON_SEAM = {"refresh-memory", "push-memory", "pull-memory", "wait-options"}

# of those, the ones referencing no component either — installing is then a pure copy.
# (`refresh-memory` inlines a component, so its installed form legitimately differs.)
_VERBATIM = {"push-memory", "pull-memory", "wait-options"}


def test_installs_full_command_set(tmp_path: Path) -> None:
    target = tmp_path / "commands"
    installed, _, _ = si.install(target, content_root=CF, output_dir=tmp_path / "out")
    names = set(installed)
    assert _KNOWN <= names
    assert _NON_SEAM <= names
    for name in installed:
        assert (target / f"{name}.md").is_file()
    # manifest records exactly what was installed, as <name>.md
    manifest = (target / ".agent-memory-manifest").read_text(encoding="utf-8").split()
    assert sorted(manifest) == sorted(f"{n}.md" for n in installed)


def test_seam_command_is_compiled_not_raw(tmp_path: Path) -> None:
    target = tmp_path / "commands"
    si.install(target, content_root=CF, output_dir=tmp_path / "out")
    text = (target / "awaken-agent.md").read_text(encoding="utf-8")
    assert "## Storage Mechanics" not in text  # compiled, not the raw seam source
    assert "§" in text  # provenance sigils kept
    assert "agent-core-memory.md" in text  # mechanics inlined


def test_non_seam_command_is_verbatim_source(tmp_path: Path) -> None:
    target = tmp_path / "commands"
    si.install(target, content_root=CF, output_dir=tmp_path / "out")
    for name in _VERBATIM:
        installed = (target / f"{name}.md").read_bytes()
        source = (CF / "procedures" / f"{name}.md").read_bytes()
        assert installed == source  # byte-for-byte, LF preserved


def test_installed_command_carries_no_component_reference(tmp_path: Path) -> None:
    # components are dev-time source: the installed command must be self-contained
    target = tmp_path / "commands"
    installed, _, _ = si.install(target, content_root=CF, output_dir=tmp_path / "out")
    for name in installed:
        assert "components/" not in (target / f"{name}.md").read_text(encoding="utf-8"), name
    text = (target / "refresh-memory.md").read_text(encoding="utf-8")
    assert "sub-agents return summaries" in text.lower()  # component body inlined instead


def test_reinstall_cleans_stale_and_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / "commands"
    out = tmp_path / "out"
    first, _, _ = si.install(target, content_root=CF, output_dir=out)
    # a command from a prior run that no longer exists must be removed on reinstall
    (target / "gone-command.md").write_text("stale\n", encoding="utf-8")
    manifest = target / ".agent-memory-manifest"
    manifest.write_text(
        manifest.read_text(encoding="utf-8") + "gone-command.md\n", encoding="utf-8"
    )
    second, _, removed = si.install(target, content_root=CF, output_dir=out)
    assert set(second) == set(first)
    assert not (target / "gone-command.md").exists()
    assert removed >= 1


def test_sibling_overlay_command_is_never_deleted(tmp_path: Path) -> None:
    target = tmp_path / "commands"
    out = tmp_path / "out"
    si.install(target, content_root=CF, output_dir=out)
    # a command that moved to the overlay: still in the core manifest, owned by the
    # sibling manifest, and no longer installed by core — cleanup must leave it alone.
    moved = target / "moved-to-overlay.md"
    moved.write_text("overlay-owned\n", encoding="utf-8")
    manifest = target / ".agent-memory-manifest"
    manifest.write_text(
        manifest.read_text(encoding="utf-8") + "moved-to-overlay.md\n", encoding="utf-8"
    )
    (target / ".agent-memory-coding-skill-manifest").write_text(
        "moved-to-overlay.md\n", encoding="utf-8"
    )
    si.install(target, content_root=CF, output_dir=out)
    assert moved.exists()  # protected by the sibling manifest
    assert moved.read_text(encoding="utf-8") == "overlay-owned\n"  # untouched
