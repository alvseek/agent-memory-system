"""The composer reads data only and preserves the exact authored UTF-8 text."""

import hashlib
import os
import sys
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1] / "packages/procedure-composer/src"
sys.path.insert(0, str(PACKAGE))
from procedure_composer import (  # noqa: E402
    Catalog,
    CompositionError,
    FileSource,
    MemorySource,
    compose,
    dependents,
    validate_catalog,
)


def assembly(identity="flow", nodes=None, kind="procedure"):
    return (
        f'format_version = 1\nid = "{identity}"\ntitle = "Flow"\n'
        f'description = "Do the work."\nkind = "{kind}"\n'
        + (nodes or '[[sections]]\nid = "shared"\nsource = "procedures/sections/shared.md"\n')
    ).encode()


def files():
    return {
        "procedures/assemblies/flow.toml": assembly(),
        "procedures/sections/shared.md": "Exact é\n\r\n終\n".encode(),
    }


def test_exact_bytes_provenance_and_determinism():
    source = MemorySource(files())
    one = compose("flow", "db", source)
    assert one == compose("flow", "db", source)
    raw = files()["procedures/sections/shared.md"]
    assert one.text.encode() == raw
    assert one.sections[0].source_hash == hashlib.sha256(raw).hexdigest()
    assert one.sections[0].backend_applicability == ("markdown", "db")
    assert dependents("shared", source) == ("flow",)


def test_immutable_snapshot():
    data = files()
    source = MemorySource(data)
    data["procedures/sections/shared.md"] = b"changed"
    assert compose("flow", "db", source).text != "changed"


def test_nested_order_repeated_sources_and_backend_alternatives():
    data = files()
    data["procedures/assemblies/flow.toml"] = assembly(nodes="""
[[sections]]
id = "first"
component = "child"
[[sections]]
id = "variant"
[sections.backends]
markdown = "procedures/sections/md.md"
db = "procedures/sections/db.md"
[[sections]]
id = "last"
component = "child"
""")
    data["procedures/assemblies/child.toml"] = assembly("child", kind="component")
    data["procedures/sections/md.md"] = b"MD"
    data["procedures/sections/db.md"] = b"DB"
    catalog = validate_catalog(MemorySource(data))
    assert catalog.procedures == ("flow",)
    result = catalog.compose("flow", "db")
    assert result.text == "Exact é\n\r\n終\nDBExact é\n\r\n終\n"
    assert result.sections[1].backend_applicability == ("db",)
    assert catalog.dependents("shared") == ("flow",)


@pytest.mark.parametrize("path", [
    "../escape.md", "/absolute.md", "C:/escape.md", r"folder\escape.md",
    "procedures/sections/../escape.md", "procedures//sections/file.md",
    "procedures/sections/./file.md", "outside.md",
])
def test_unsafe_and_undeclared_targets(path):
    data = files()
    data["procedures/assemblies/flow.toml"] = assembly(nodes=(
        f'[[sections]]\nid = "bad"\nsource = "{path.replace(chr(92), chr(92) * 2)}"\n'
    ))
    with pytest.raises(CompositionError):
        validate_catalog(MemorySource(data))


@pytest.mark.parametrize("change", [
    lambda raw: raw.replace(b"format_version = 1", b"format_version = 99"),
    lambda raw: raw.replace(b'source = ', b'unknown = '),
    lambda raw: raw + b'component = "child"\n',
    lambda raw: raw + b'[[sections]]\nid = "shared"\nsource = "procedures/sections/shared.md"\n',
    lambda raw: raw.replace(b'id = "flow"', b'id = "BAD ID"'),
    lambda raw: raw.replace(b'source = "procedures/sections/shared.md"',
                           b'[sections.backends]\ndb = "procedures/sections/shared.md"'),
])
def test_invalid_data_never_falls_back(change):
    data = files()
    data["procedures/assemblies/flow.toml"] = change(data["procedures/assemblies/flow.toml"])
    with pytest.raises(CompositionError):
        validate_catalog(MemorySource(data))


def test_duplicate_assembly_id_and_conflicting_section_identity():
    data = files()
    data["procedures/assemblies/other.toml"] = assembly()
    with pytest.raises(CompositionError, match="duplicate assembly"):
        Catalog(MemorySource(data))
    data["procedures/assemblies/other.toml"] = assembly("other").replace(
        b"shared.md", b"other.md"
    )
    with pytest.raises(CompositionError, match="conflicting"):
        Catalog(MemorySource(data))


def test_one_source_cannot_hide_behind_two_different_section_identities():
    data = files()
    data["procedures/assemblies/other.toml"] = assembly("other").replace(
        b'id = "shared"', b'id = "different"'
    )
    with pytest.raises(CompositionError, match="multiple section identities"):
        Catalog(MemorySource(data))


def test_missing_source_component_and_cycles():
    data = files()
    del data["procedures/sections/shared.md"]
    with pytest.raises(CompositionError, match="missing source"):
        validate_catalog(MemorySource(data))
    data = files()
    data["procedures/assemblies/flow.toml"] = assembly(nodes=(
        '[[sections]]\nid = "ref"\ncomponent = "child"\n'
    ))
    with pytest.raises(CompositionError, match="not a component"):
        validate_catalog(MemorySource(data))
    data["procedures/assemblies/child.toml"] = assembly("child", kind="component", nodes=(
        '[[sections]]\nid = "cycle"\ncomponent = "child"\n'
    ))
    with pytest.raises(CompositionError, match="cycle"):
        validate_catalog(MemorySource(data))


def test_filesystem_snapshot_and_nested_repo_refusal(tmp_path):
    for path, raw in files().items():
        destination = tmp_path / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
    source = FileSource(tmp_path)
    assert compose("flow", "db", source).text == "Exact é\n\r\n終\n"
    (tmp_path / "procedures/sections/.git").write_text("gitdir: elsewhere")
    with pytest.raises(CompositionError, match="nested repository"):
        FileSource(tmp_path)


def test_invalid_utf8_unknown_backend_and_missing_procedure():
    data = files()
    data["procedures/sections/shared.md"] = b"\xff"
    with pytest.raises(CompositionError, match="UTF-8"):
        validate_catalog(MemorySource(data))
    source = MemorySource(files())
    with pytest.raises(CompositionError, match="unknown backend"):
        compose("flow", "unknown", source)
    with pytest.raises(CompositionError, match="unknown assembly"):
        compose("missing", "db", source)


def test_symlink_refused_even_when_it_points_inside_root(tmp_path):
    target = tmp_path / "real"
    target.mkdir()
    (tmp_path / "procedures").mkdir()
    try:
        os.symlink(target, tmp_path / "procedures/sections", target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"host does not permit symlink creation: {exc}")
    with pytest.raises(CompositionError, match="linked"):
        FileSource(tmp_path)
