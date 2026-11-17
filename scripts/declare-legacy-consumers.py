"""Record actual legacy consumers of the canonical DB preamble, without converting them."""

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    path = ROOT / "procedures/setup-scripts/compile-procedures.py"
    spec = importlib.util.spec_from_file_location("consumer_inventory", path)
    compiler = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = compiler
    spec.loader.exec_module(compiler)
    document = (ROOT / "procedures/memory/storage-backends/db.md").read_text(encoding="utf-8")
    if not compiler.defines_section(document, "all-procedures"):
        raise ValueError("no common DB preamble to declare")
    for command in compiler.command_procedures(ROOT / "procedures"):
        if command.suffix != ".md":
            continue
        raw = command.read_text(encoding="utf-8")
        if not compiler.has_seam(raw):
            continue
        _, missing, used = compiler.inline_components(
            raw, ROOT / "procedures/components", backend="db"
        )
        if missing:
            raise ValueError(f"unresolved legacy consumer: {command.stem}: {missing}")
        if not compiler._backend_covers(document, command.stem, tuple(used)):
            continue
        target = ROOT / f"procedures/assemblies/{command.stem}.toml"
        node = (
            '[[sections]]\nid = "caller-context"\napplies_to = ["db"]\n'
            '[sections.backends]\n'
            'markdown = "procedures/sections/markdown/caller-context.md"\n'
            'db = "procedures/sections/db/caller-context.md"\n'
        )
        if target.exists():
            current = target.read_text(encoding="utf-8")
            if 'id = "caller-context"' in current:
                raise ValueError(f"consumer already declared: {target}")
            target.write_text(current + "\n" + node, encoding="utf-8", newline="\n")
        else:
            target.write_text(
                f'format_version = 1\nid = "{command.stem}"\nkind = "external"\n'
                f'title = {json.dumps(command.stem + " dependencies")}\n'
                'description = "Dependency declaration only; the complete command remains '
                'on the legacy renderer."\n\n' + node,
                encoding="utf-8", newline="\n",
            )
        print(command.stem)
