"""Baseline fixture bytes must reconcile to their recorded pre-conversion revision."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/composition-baseline"


def test_baseline_bytes_and_committed_sources():
    manifest = json.loads((FIXTURES / "manifest.json").read_text(encoding="utf-8"))
    assert set(manifest["graph"]) == set(manifest["roots"] + manifest["required_calls"])
    for path, digest in manifest["input_sha256"].items():
        raw = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{manifest['commit']}:{path}"]
        )
        assert hashlib.sha256(raw).hexdigest() == digest, path
    for filename, digest in manifest["output_sha256"].items():
        assert hashlib.sha256((FIXTURES / filename).read_bytes()).hexdigest() == digest
    converted = json.loads((FIXTURES / "converted/manifest.json").read_text(encoding="utf-8"))
    for filename, digest in converted["sha256"].items():
        raw = (FIXTURES / "converted" / filename).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest
