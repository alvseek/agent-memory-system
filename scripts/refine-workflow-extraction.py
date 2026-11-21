"""Finish the one-time source extraction using exact span transfers and explicit edits."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def transfer(source: str, marker: str, end: str | None, target: str) -> None:
    path = ROOT / source
    text = path.read_text(encoding="utf-8")
    start = text.index(marker)
    stop = text.index(end, start) if end else len(text)
    destination = ROOT / target
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(text[start:stop].encode("utf-8"))
    path.write_text(text[:start] + text[stop:], encoding="utf-8", newline="\n")


def replace(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise ValueError(f"expected exactly one edit match: {path}: {old!r}")
    target.write_text(text.replace(old, new), encoding="utf-8", newline="\n")


def variant_node(identity, markdown, db):
    return (f'[[sections]]\nid = "{identity}"\n[sections.backends]\n'
            f'markdown = "{markdown}"\ndb = "{db}"\n\n')


if __name__ == "__main__":
    # Git-only failure/report mechanics belong only to the git variant, not a DB
    # instruction followed by a no-op. Shared report content remains single-source.
    report = "procedures/sections/shared/wrap-up.text-006.md"
    transfer(report, "**On failure**", "\n---\n",
             "procedures/sections/markdown/wrap-up.failure-report.md")
    transfer(report, "Memory persisted — print the line", "📋 Open items",
             "procedures/sections/markdown/wrap-up.persistence-report.md")
    replace("procedures/sections/markdown/wrap-up.persistence-report.md",
            "Memory persisted — print the line matching this backend, not both:\n",
            "Memory persisted:\n")
    replace("procedures/sections/markdown/wrap-up.persistence-report.md",
            "- (store durable at write time) ✅ nothing to push — "
            "the write was already saved\n", "")
    transfer(report, "📋 Open items", None,
             "procedures/sections/shared/wrap-up.open-items-report.md")
    replace("procedures/sections/shared/wrap-up.open-items-report.md",
            "---\n\n---\n\n", "---\n\n")
    (ROOT / "procedures/sections/db/wrap-up.persistence-report.md").write_text(
        "Memory persisted:\n- ✅ nothing to push — the write was already saved\n\n",
        encoding="utf-8", newline="\n",
    )
    (ROOT / "procedures/sections/db/wrap-up.failure-report.md").write_bytes(b"")
    assembly = ROOT / "procedures/assemblies/wrap-up.toml"
    with assembly.open("a", encoding="utf-8", newline="\n") as output:
        output.write(variant_node(
            "wrap-up.persistence-report",
            "procedures/sections/markdown/wrap-up.persistence-report.md",
            "procedures/sections/db/wrap-up.persistence-report.md",
        ))
        output.write('[[sections]]\nid = "wrap-up.open-items-report"\n'
                     'source = "procedures/sections/shared/wrap-up.open-items-report.md"\n\n')
        output.write(variant_node(
            "wrap-up.failure-report",
            "procedures/sections/markdown/wrap-up.failure-report.md",
            "procedures/sections/db/wrap-up.failure-report.md",
        ))
    replace(report,
            "**Completion gate** (per NO TODOS LEFT BEHIND, UUID a1b2c3d4): "
            "the wrap-up is complete only when Step 2's outcome says this session's memory "
            "is persisted. A backend that is durable at write time passes trivially. "
            "A git-backed store passes only when nothing in scope is dirty and no branch "
            "carrying this agent's commits is ahead of its remote. In `agent` mode another "
            "agent's dirty files are expected, reported, and never a failure.",
            "**Completion gate** (UUID a1b2c3d4): report completion only when Step 2 "
            "confirms this session's memory is persisted. Apply the selected backend's "
            "persistence and failure rules below.")
    # An index is an outcome; only Markdown requires manually maintaining one.
    replace("procedures/sections/shared/update-knowledge.text-007.md",
            "### Step 4: Register in the Knowledge Index",
            "### Step 4: Confirm Knowledge Discoverability")
    replace("procedures/sections/shared/update-knowledge.text-007.md",
            "Add an entry to the knowledge directory for discoverability",
            "Ensure the entry is discoverable through the knowledge directory")
    replace("procedures/sections/shared/update-episodic.text-005.md",
            "for the sub-episode H3 header and index-entry placement",
            "for the sub-episode H3 header")
    # Load mechanics precede processing the loaded identity, including for a legacy
    # refresh-memory caller that reuses this component.
    path = ROOT / "procedures/assemblies/core-instruction-control-files.toml"
    content = path.read_text(encoding="utf-8")
    start = content.index('[[sections]]\nid = "core-instruction-control-files.load-agent-memory"')
    load_node = content[start:]
    content = content[:start]
    insertion = content.index("[[sections]]")
    path.write_text(content[:insertion] + load_node + content[insertion:],
                    encoding="utf-8", newline="\n")
