"""Compatibility adapters receive source context; their folder layout is not a lookup rule."""

import importlib.util
from pathlib import Path

import pytest
from procedure_composer import MemorySource

ROOT = Path(__file__).resolve().parents[1]


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_component_pointer_works_in_an_unrelated_directory_with_an_injected_provider(tmp_path):
    inline = module("injected_component", "procedures/components/inline.py")
    directory = tmp_path / "not-a-framework-layout"
    directory.mkdir()
    (directory / "sample.md").write_text("<!-- composed-component: sample -->", encoding="utf-8")
    source = MemorySource({
        "procedures/assemblies/sample.toml": (
            b'format_version=1\nid="sample"\nkind="component"\ntitle="Sample"\n'
            b'description="Test context injection."\n[[sections]]\nid="sample.body"\n'
            b'source="procedures/sections/body.md"\n'
        ),
        "procedures/sections/body.md": b"Injected content\n",
    })
    text, missing, used = inline.inline_components(
        "[Sample](components/sample.md)\n", directory, source_provider=source
    )
    assert "Injected content" in text and not missing and used == ["sample"]
    with pytest.raises(ValueError, match="injected source provider"):
        inline.inline_components("[Sample](components/sample.md)\n", directory)


def test_legacy_seam_factory_remains_live_without_deriving_a_parent_directory():
    seam = module("injected_seam", "procedures/memory/storage-backends/seam.py")
    document = "## sample\n\n<!-- composed-source: procedures/sections/body.md -->\n"
    with pytest.raises(ValueError, match="injected source provider"):
        seam.extract_section(document, "sample")
    files = {"procedures/sections/body.md": b"first"}
    seam.configure_source_provider(lambda: MemorySource(files))
    assert seam.extract_section(document, "sample") == "first"
    files["procedures/sections/body.md"] = b"changed"
    assert seam.extract_section(document, "sample") == "changed"
