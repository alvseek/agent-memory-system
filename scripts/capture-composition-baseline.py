"""Capture immutable workflow inputs and legacy outputs before source conversion."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOTS = ("awaken-agent", "wrap-up")
REQUIRED = ("update-memory", "add-reasoning", "update-knowledge",
            "update-episodic", "update-emotional")


def capture(root: Path, destination: Path) -> dict:
    script = root / "procedures/setup-scripts/compile-procedures.py"
    spec = importlib.util.spec_from_file_location("baseline_compiler", script)
    compiler = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = compiler
    spec.loader.exec_module(compiler)
    catalog = {p.stem: p for p in compiler.command_procedures(root / "procedures")}
    graph, inputs, visited = {}, {}, set()

    def visit(name: str) -> None:
        if name in visited:
            return
        visited.add(name)
        path = catalog[name]
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        inlined, missing, used = compiler.inline_components(text, root / "procedures/components")
        if missing:
            raise ValueError(f"{name}: unresolved components: {missing}")
        # This is a candidate call inventory, not an assertion that every mention executes.
        mentions = sorted(set(re.findall(r"/([a-z][a-z0-9-]+)", inlined)) & catalog.keys())
        resources = sorted(set(re.findall(
            r"([a-z][a-z0-9-]*(?:template))", inlined
        )))
        graph[name] = {"source": path.relative_to(root).as_posix(),
                       "components": sorted(set(used)), "command_mentions": mentions,
                       "resource_mentions": resources}
        inputs[path.relative_to(root).as_posix()] = hashlib.sha256(raw).hexdigest()
        for component in used:
            source = root / "procedures/components" / f"{component}.md"
            inputs[source.relative_to(root).as_posix()] = hashlib.sha256(
                source.read_bytes()
            ).hexdigest()

    for name in (*ROOTS, *REQUIRED):
        visit(name)
    for backend in compiler.BACKENDS:
        source = root / f"procedures/memory/storage-backends/{backend}.md"
        inputs[source.relative_to(root).as_posix()] = hashlib.sha256(
            source.read_bytes()
        ).hexdigest()
    destination.mkdir(parents=True, exist_ok=False)
    outputs = {}
    with tempfile.TemporaryDirectory() as temporary:
        for backend in compiler.BACKENDS:
            reports, skipped = compiler.compile_all(root, Path(temporary) / backend, backend)
            for report in reports:
                if report.name not in graph:
                    continue
                if report.unresolved_ops or report.missing_components:
                    raise ValueError(f"incomplete baseline: {report}")
                raw = report.out_path.read_bytes()
                filename = f"{report.name}.{backend}.md"
                (destination / filename).write_bytes(raw)
                outputs[filename] = hashlib.sha256(raw).hexdigest()
            if set(graph) & set(skipped):
                raise ValueError(f"skipped required commands: {skipped}")
    manifest = {
        "commit": subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip(),
        "roots": ROOTS, "required_calls": REQUIRED,
        "graph": graph, "input_sha256": inputs, "output_sha256": outputs,
        "note": "Generated historical evidence, not an authored procedure source. "
                "Command mentions include explanatory/conditional references; "
                "inspect before conversion.",
    }
    (destination / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    manifest = capture(args.root.resolve(), args.out.resolve())
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
