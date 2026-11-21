"""One-time extraction from the recorded legacy revision; refuses changed inputs.

Copies source substrings, records every copied span, and places mechanics at first
use. Editorial corrections are explicit subsequent edits, not generated paraphrases.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path


def load(root, name, relative):
    spec = importlib.util.spec_from_file_location(name, root / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def convert(root: Path) -> None:
    baseline = root / "tests/fixtures/composition-baseline"
    manifest = json.loads((baseline / "manifest.json").read_text(encoding="utf-8"))
    for relative, expected in manifest["input_sha256"].items():
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != expected:
            raise ValueError(f"source changed since baseline: {relative}")
    seam = load(root, "conversion_seam", "procedures/memory/storage-backends/seam.py")
    inline = load(root, "conversion_inline", "procedures/components/inline.py")
    backend_docs = {
        b: (root / f"procedures/memory/storage-backends/{b}.md").read_text(encoding="utf-8")
        for b in ("markdown", "db")
    }
    assembly_dir = root / "procedures/assemblies"
    if assembly_dir.exists():
        raise ValueError("refuse to overwrite an existing catalog")
    assembly_dir.mkdir()
    mapping = []

    def write_section(identity, text, origin, backend="shared"):
        path = f"procedures/sections/{backend}/{identity}.md"
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8"))
        mapping.append({"id": identity, "source": origin, "target": path,
                        "sha256": hashlib.sha256(text.encode()).hexdigest()})
        return path

    def node(identity, source=None, variants=None, component=None):
        lines = ["[[sections]]", f'id = "{identity}"']
        if source:
            lines.append(f'source = "{source}"')
        elif component:
            lines.append(f'component = "{component}"')
        else:
            lines.append("[sections.backends]")
            lines.extend(f'{b} = "{p}"' for b, p in variants.items())
        return "\n".join(lines) + "\n\n"

    # Generic DB caller context is authored once and shared across converted commands.
    context = {}
    for backend in ("markdown", "db"):
        text = (seam.extract_section(backend_docs[backend], "all-procedures") + "\n\n"
                if seam.defines_section(backend_docs[backend], "all-procedures") else "")
        context[backend] = write_section(
            "caller-context", text, f"storage-backends/{backend}.md#all-procedures", backend
        )
    preamble = node("caller-context", variants=context)
    components = manifest["graph"]["awaken-agent"]["components"]
    items = {name: root / row["source"] for name, row in manifest["graph"].items()}
    items.update({name: root / f"procedures/components/{name}.md" for name in components})
    calls = {
        "wrap-up": ["update-memory"],
        "update-memory": ["add-reasoning", "update-knowledge", "update-episodic",
                          "update-emotional"],
    }
    arguments = {"awaken-agent": "domain", "wrap-up": "mode", "update-memory": "mode",
                 "add-reasoning": "context", "update-knowledge": "context",
                 "update-episodic": "mode", "update-emotional": "moment_type"}
    for name, path in items.items():
        original = path.read_text(encoding="utf-8")
        text = inline.component_body(original) + "\n" if name in components else original
        # The storage section is dispatch scaffolding, never authored policy.
        if seam.has_seam(text):
            lines = text.splitlines(keepends=True)
            start = next(i for i, line in enumerate(lines)
                         if line.strip() == "## Storage Mechanics")
            end = next((i for i in range(start + 1, len(lines))
                        if lines[i].startswith("## ") or lines[i].strip() == "---"), len(lines))
            text = "".join(lines[:start] + lines[end:])
        text = seam._SEAM_XREF.sub("", text)
        # Authored edit units follow complete heading sections, never individual
        # paragraphs. Backend definitions follow the section that first uses them.
        paragraphs, buffer, fenced = [], [], False
        for line in text.splitlines(keepends=True):
            if not fenced and re.match(r"^#{1,4} ", line) and buffer:
                paragraphs.append("".join(buffer))
                buffer = []
            buffer.append(line)
            if line.lstrip().startswith("```"):
                fenced = not fenced
        if buffer:
            paragraphs.append("".join(buffer))
        ops = {}
        for backend, document in backend_docs.items():
            if seam.defines_section(document, name):
                body = seam.extract_section(document, name)
                found = list(re.finditer(r"(?m)^### § ([a-z][a-z0-9-]*)\s*$", body))
                for i, match in enumerate(found):
                    end = found[i + 1].start() if i + 1 < len(found) else len(body)
                    raw = body[match.start():end].rstrip("\n")
                    raw = re.sub(r"\n---\s*$", "", raw).rstrip("\n") + "\n\n"
                    ops.setdefault(match.group(1), {})[backend] = raw
        header = {
            "format_version": 1, "id": name,
            "title": original.splitlines()[0].removeprefix("# "),
            "description": next(p.strip() for p in original.split("\n\n")[1:]
                                if p.strip() and not p.startswith("#")),
        }
        if name in components:
            header["kind"] = "component"
        if name in arguments:
            header["argument_name"] = arguments[name]
            header["argument_description"] = "Input described in the procedure's Arguments section"
        if name in calls:
            header["calls"] = calls[name]
        rendered = ""
        for key, value in header.items():
            rendered += f"{key} = {json.dumps(value, ensure_ascii=False)}\n"
        rendered += "\n" + ("" if name in components else preamble)
        placed = set()
        for index, paragraph in enumerate(paragraphs, 1):
            identity = f"{name}.text-{index:03}"
            links = list(inline._COMPONENT_LINK.finditer(paragraph))
            if links:
                cleaned = inline._COMPONENT_LINK.sub(r"\1", paragraph)
                rendered += node(identity, source=write_section(
                    identity, cleaned, path.relative_to(root).as_posix()))
                for match in links:
                    component = match.group(2)
                    rendered += node(f"{name}.include-{component}", component=component)
            else:
                rendered += node(identity, source=write_section(
                    identity, paragraph, path.relative_to(root).as_posix()))
            for op in re.findall(r"§\s*([a-z][a-z0-9-]*)", paragraph):
                if op not in ops or op in placed:
                    continue
                if set(ops[op]) != {"markdown", "db"}:
                    raise ValueError(f"asymmetric operation: {name}/{op}")
                placed.add(op)
                identity = f"{name}.{op}"
                variants = {
                    backend: write_section(identity, raw, f"storage-backends/{backend}.md#{name}",
                                           backend)
                    for backend, raw in ops[op].items()
                }
                rendered += node(identity, variants=variants)
        # Awakening's load op is first used by its caller; keep the mechanics at the
        # start of the shared awakening component, which owns it in both backends.
        for op in sorted(set(ops) - placed):
            identity = f"{name}.{op}"
            variants = {backend: write_section(
                identity, raw, f"storage-backends/{backend}.md#{name}", backend
            ) for backend, raw in ops[op].items()}
            rendered += node(identity, variants=variants)
        (assembly_dir / f"{name}.toml").write_text(rendered, encoding="utf-8", newline="\n")
    (baseline / "extraction-map.json").write_text(
        json.dumps(mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    convert(Path(__file__).resolve().parents[1])
