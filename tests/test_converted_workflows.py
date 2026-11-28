"""Instruction accounting against captured bytes, plus ordering and delivery guards."""

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest
from procedure_composer import Catalog, FileSource, MemorySource

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "tests/fixtures/composition-baseline"


def catalog():
    return Catalog(FileSource(ROOT))


def test_recorded_conversion_preserved_legacy_instructions_or_named_edits():
    # This audits the conversion, not every future wording change made in the
    # editor. Current operational invariants are tested independently below.
    identities = json.loads((BASELINE / "manifest.json").read_text(encoding="utf-8"))["graph"]
    for name in identities:
        for backend in ("markdown", "db"):
            before = (BASELINE / f"{name}.{backend}.md").read_text(encoding="utf-8")
            after = (BASELINE / "converted" / f"{name}.{backend}.md").read_text(encoding="utf-8")
            allowed = set()
            if name == "update-episodic":
                allowed.update(
                    line
                    for line in before.splitlines()
                    if line.startswith("Obtain the current date+time")
                )
                assert "for the sub-episode H3 header (**§ stamp-date**)" in after
            if name == "update-knowledge":
                allowed.update(
                    line
                    for line in before.splitlines()
                    if line.startswith("Add an entry to the knowledge directory")
                )
                assert "Ensure the entry is discoverable" in after
            if name == "wrap-up":
                allowed.add("Memory persisted — print the line matching this backend, not both:")
                allowed.add(
                    "- (store durable at write time) ✅ nothing to push — "
                    "the write was already saved"
                )
                if backend == "db":
                    # Only Git persistence instructions disappear on the DB backend.
                    failure = before.split("**On failure**", 1)[1].split("\n---\n", 1)[0]
                    allowed.update(("**On failure**" + failure).splitlines())
                    allowed.update(
                        line
                        for line in before.splitlines()
                        if line.startswith(("**Completion gate**", "- (git-backed"))
                    )
                    assert "report completion only when Step 2" in after
                    assert "WRAP-UP INCOMPLETE" not in after
                expected = "nothing to push" if backend == "db" else "pushed / no changes"
                assert expected in after
            missing = [
                line
                for line in before.splitlines()
                if line.strip()
                and not line.startswith("#")
                and line.strip() not in ("---", "```", "```markdown")
                and line not in allowed
                and line.strip() not in after
            ]
            assert not missing, (name, backend, missing)


def test_current_workflows_keep_their_operational_contracts():
    critical = {
        "awaken-agent": ["own context", "load-user-profile", "load-latest-episode"],
        "wrap-up": [
            "call `/update-memory` without arguments",
            "one final report",
            "tech debts",
            "next steps",
        ],
        "update-memory": ["cutoff", "all 5 must pass", "tech debts", "next steps"],
        "update-episodic": [
            "carry-forward",
            "newest-first",
            "finished",
            "tech debts",
            "next steps",
        ],
        "update-reasoning": [
            "final conclusion",
            "preserve the existing uuid",
            "reasoning-pattern-template",
        ],
        "update-knowledge": [
            "knowledge-file-template", "without approval, including shared entries",
            "change a shared decision or the supporting evidence conflicts",
            "defer just that edit instead of waiting", "partial write",
        ],
        "update-emotional": ["newest", "emotional-moment-template"],
    }
    current = catalog()
    for identity, tokens in critical.items():
        for backend in ("markdown", "db"):
            text = current.compose(identity, backend).text.replace("**", "").lower()
            assert all(token in text for token in tokens), (identity, backend)

    db = current.compose("wrap-up", "db").text
    markdown = current.compose("wrap-up", "markdown").text
    assert current.compose("wrap-up", "db").argument_name is None
    assert "$ARGUMENTS" not in db and "$ARGUMENTS" in markdown
    for git_only in ("/push-memory", "[agent|all]", "push error"):
        assert git_only in markdown and git_only not in db
    assert "what remains unsaved" in db

    # Helheim shows one card per span, including whitespace-only spans.
    for backend in ("db", "markdown"):
        shared, finish = current.compose("wrap-up", backend).spans
        assert shared.path == "procedures/wrap-up.md" and shared.text.strip()
        assert finish.path.endswith(f"/{backend}.md") and finish.target == "wrap-up.finish"
        assert finish.text.strip()


def test_backend_mechanics_are_beside_steps_and_resources_remain_references():
    composed = catalog()
    assert "add-reasoning" not in composed.procedures
    for backend in ("db", "markdown"):
        caller = composed.compose("update-memory", backend)
        assert "update-reasoning" in caller.calls and "add-reasoning" not in caller.calls
        assert "added / refined / skipped" in caller.text
        assert "update-knowledge" in caller.calls and "added / updated / skipped" in caller.text
    text = composed.compose("update-reasoning", "db").text.replace("\r\n", "\n")
    assert text.index("### § read-reasoning-store\n") < text.index("## 2. Save")
    assert text.index("### § save\n") > text.index("## 2. Save")
    assert "template_version" in text and "reasoning-pattern-template" in text
    awakening = composed.compose("awaken-agent", "db").text
    assert awakening.index("### § load-agent-memory") < awakening.index("### Step 2:")
    for name in composed.procedures:
        db = composed.compose(name, "db").text
        assert "## Storage Mechanics" not in db
        assert "components/" not in db
        assert "cp [AGENT-MEMORY-PATH]" not in db
        assert "MOVE-TO-TODAY" not in db
        assert "## Templates (inlined)" not in db
    assert composed.compose("wrap-up", "markdown").calls == ("update-memory", "push-memory")
    assert composed.compose("wrap-up", "db").calls == ("update-memory",)


@pytest.mark.parametrize("backend", ["db", "markdown"])
def test_awaken_uses_profile_from_backend_without_placeholder_section(backend):
    text = catalog().compose("awaken-agent", backend).text
    assert "# USER PROFILE" not in text
    assert "[User Profile](#user-profile)" not in text
    assert "§ load-user-profile" in text
    assert "§ persist-user-profile" in text
    assert "First run — no profile at all" in text
    assert ("shared.user_profile" if backend == "db" else "global instructions file") in text


def test_current_composition_matches_reviewed_delivery():
    # Keep the migration evidence immutable. These separate fingerprints cover the
    # current delivered text after subsequent intentional authoring changes.
    expected = json.loads((ROOT / "tests/fixtures/procedure-delivery.json").read_text("utf-8"))
    composed = catalog()
    actual = {
        name: {
            backend: hashlib.sha256(composed.compose(name, backend).text.encode()).hexdigest()
            for backend in ("db", "markdown")
        }
        for name in composed.procedures
    }
    assert actual == expected


def test_no_fragmented_inventory_or_directive_leakage_remains():
    assert not (ROOT / "procedures/assemblies").exists()
    assert not (ROOT / "procedures/sections").exists()
    for directory in (
        "procedures",
        "procedures/memory",
        "procedures/components",
        "procedures/external",
        "procedures/memory/storage-backends",
    ):
        for path in (ROOT / directory).glob("*.md"):
            text = path.read_text(encoding="utf-8")
            if not text.startswith("+++"):
                continue
            for marker in (
                "<!-- composed-procedure:",
                "<!-- composed-component:",
                "<!-- composed-source:",
            ):
                assert marker not in text, path
    composed = catalog()
    for identity in composed.documents:
        for backend in ("markdown", "db"):
            text = composed.compose(identity, backend).text
            assert "@start " not in text and "@end " not in text, (identity, backend)
            assert "<!-- composed-" not in text, (identity, backend)


def test_extraction_lineage_has_no_unrecorded_source_origins():
    manifest = json.loads((BASELINE / "manifest.json").read_text(encoding="utf-8"))
    extracted = json.loads((BASELINE / "extraction-map.json").read_text(encoding="utf-8"))
    assert extracted
    for entry in extracted:
        origin = entry["source"]
        assert origin.startswith("storage-backends/") or origin in manifest["input_sha256"]
    # The manifest identifies the original conversion; track later renames here.
    renamed = {"add-reasoning": "update-reasoning"}
    current = catalog().procedures
    for name in manifest["graph"]:
        assert renamed.get(name, name) in current


def test_missing_converted_source_refuses_instead_of_legacy_pointer_fallback():
    source = FileSource(ROOT)
    data = {p: source.read(p) for p in source.paths("procedures")}
    data.pop("procedures/memory/storage-backends/db.md")
    with pytest.raises(ValueError, match="missing source"):
        Catalog(MemorySource(data)).compose("wrap-up", "db")


def test_reverse_dependencies_include_the_actual_legacy_refresh_consumer():
    composed = catalog()
    assert "refresh-memory" not in composed.procedures
    assert composed.documents["refresh-memory"].metadata.kind == "external"
    assert composed.dependents("procedures/components/core-instruction-control-files.md") == (
        "awaken-agent",
        "refresh-memory",
    )
    assert composed.dependents("procedures/components/no-subagent-load.md") == (
        "awaken-agent",
        "refresh-memory",
    )
    legacy = (ROOT / "procedures/refresh-memory.md").read_text(encoding="utf-8")
    for component in ("core-instruction-control-files", "no-subagent-load"):
        assert f"components/{component}.md" in legacy


def test_backend_specific_impact_matches_actual_legacy_delivery():
    composed = catalog()
    externals = {
        identity
        for identity, document in composed.documents.items()
        if document.metadata.kind == "external"
    }
    db_path = "procedures/memory/storage-backends/db.md"
    markdown_path = "procedures/memory/storage-backends/markdown.md"
    # update-memory delegates storage to the procedures it calls.
    consumers = (set(composed.procedures) | externals) - {"update-memory"}
    assert set(composed.dependents(db_path)) == consumers
    # Tenant sharing has no Markdown section. Each other external consumes its own
    # backend section or, for refresh-memory, the shared awakening component.
    assert set(composed.dependents(markdown_path)) == consumers - {"tenant-sharing"}


@pytest.mark.parametrize("host", ["claude-code", "opencode"])
def test_real_installer_emits_canonical_converted_instructions(tmp_path, host):
    spec = importlib.util.spec_from_file_location(
        f"conversion_installer_{host}",
        ROOT / f"procedures/setup-scripts/setup-all-{host}.py",
    )
    installer = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = installer
    spec.loader.exec_module(installer)
    target = tmp_path / host
    installer.install(target, ROOT, tmp_path / "compiled")
    for name in catalog().procedures:
        path = target / (f"agent-memory-{name}/SKILL.md" if host == "opencode" else f"{name}.md")
        text = path.read_text(encoding="utf-8")
        assert text.endswith(catalog().compose(name, "markdown").text)
        assert "<!-- composed-procedure:" not in text
