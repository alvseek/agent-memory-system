"""Replace migrated backend bodies with data includes of their canonical sources."""

import re
from pathlib import Path

from procedure_composer import Catalog, FileSource

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    baseline = ROOT / "tests/fixtures/composition-baseline/wrap-up.markdown.md"
    original = baseline.read_text(encoding="utf-8")
    gate = next(line for line in original.splitlines() if line.startswith("**Completion gate**"))
    persist = ROOT / "procedures/sections/markdown/wrap-up.persist-store.md"
    persist.write_bytes(persist.read_bytes() + gate.encode("utf-8") + b"\n\n")
    catalog = Catalog(FileSource(ROOT))
    names = set(catalog.entries) - {"no-subagent-load"}
    for backend in ("markdown", "db"):
        path = ROOT / f"procedures/memory/storage-backends/{backend}.md"
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        matches = list(re.finditer(r"(?m)^## ([a-z][a-z0-9-]*)\r?$", text))
        for index in range(len(matches) - 1, -1, -1):
            match = matches[index]
            name = match.group(1)
            if name not in names and not (backend == "db" and name == "all-procedures"):
                continue
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            if name == "all-procedures":
                sources = ["procedures/sections/db/caller-context.md"]
            else:
                sources = list(dict.fromkeys(
                    section.source for section in catalog.compose(name, backend).sections
                    if section.source.startswith(f"procedures/sections/{backend}/{name}.")
                ))
            replacement = match.group(0) + "\n\n"
            replacement += "".join(f"<!-- composed-source: {source} -->\n" for source in sources)
            replacement += "\n"
            text = text[:match.start()] + replacement + text[end:]
        path.write_bytes(text.encode("utf-8"))
