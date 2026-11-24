"""Capture immutable after-conversion evidence, not a ban on future prose edits."""

import argparse
import hashlib
import json
from pathlib import Path

from procedure_composer import Catalog, FileSource

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    destination = root / "tests/fixtures/composition-baseline/converted"
    destination.mkdir(exist_ok=False)
    catalog = Catalog(FileSource(root))
    hashes = {}
    for identity in catalog.procedures:
        for backend in ("markdown", "db"):
            raw = catalog.compose(identity, backend).text.encode("utf-8")
            name = f"{identity}.{backend}.md"
            (destination / name).write_bytes(raw)
            hashes[name] = hashlib.sha256(raw).hexdigest()
    (destination / "manifest.json").write_text(
        json.dumps({"purpose": "Historical generated conversion evidence; never an authored source",
                    "sha256": hashes}, indent=2) + "\n", encoding="utf-8", newline="\n",
    )
    print(f"Captured {len(hashes)} historical outputs")
