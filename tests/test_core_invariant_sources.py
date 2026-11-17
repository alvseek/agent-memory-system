"""The standalone-core guard must see moved canonical prose, not only old pointers."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_section_leak_fails_the_real_shell_guard(tmp_path):
    bash = (Path("C:/Program Files/Git/bin/bash.exe") if os.name == "nt"
            else Path(shutil.which("bash") or "/missing-bash"))
    if not bash.is_file():
        pytest.skip("bash unavailable; CI runs the real shell guard")
    script = tmp_path / "scripts/check-core-invariant.sh"
    script.parent.mkdir()
    shutil.copyfile(ROOT / "scripts/check-core-invariant.sh", script)
    names = (
        "awaken-agent", "refresh-memory", "wrap-up", "push-memory", "pull-memory",
        "create-agent", "list-agents", "wait-options", "anchor-memory", "register-core-access",
    )
    for name in names:
        path = tmp_path / "procedures" / f"{name}.md"
        path.parent.mkdir(exist_ok=True)
        path.write_text("# Placeholder\n", encoding="utf-8")
    for directory in ("memory", "components", "sections", "assemblies"):
        (tmp_path / "procedures" / directory).mkdir()
    (tmp_path / "core-memory").mkdir()

    def run():
        return subprocess.run([str(bash), script.as_posix()], capture_output=True,
                              text=True, encoding="utf-8", check=False)

    assert run().returncode == 0
    (tmp_path / "procedures/sections/new-source.md").write_text(
        "Do not accidentally deliver /high-wizard through a core source.\n", encoding="utf-8"
    )
    failed = run()
    assert failed.returncode == 1 and "new-source.md" in failed.stdout
