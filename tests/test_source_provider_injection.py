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


def test_v2_component_uses_an_injected_provider(tmp_path):
    inline = module("injected_component", "procedures/components/inline.py")
    directory = tmp_path / "not-a-framework-layout"
    directory.mkdir()
    component = (
        "+++\nformat_version = 2\nid = \"sample\"\nkind = \"component\"\n"
        "title = \"Sample\"\ndescription = \"Test context injection.\"\n+++\n"
        "Injected content\n"
    )
    (directory / "sample.md").write_text(component, encoding="utf-8")
    source = MemorySource({"procedures/components/sample.md": component.encode()})
    text, missing, used = inline.inline_components(
        "[Sample](components/sample.md)\n", directory, source_provider=source
    )
    assert "Injected content" in text and not missing and used == ["sample"]
    with pytest.raises(ValueError, match="injected source provider"):
        inline.inline_components("[Sample](components/sample.md)\n", directory)


def test_superseded_component_pointer_is_refused(tmp_path):
    inline = module("pointer_component", "procedures/components/inline.py")
    directory = tmp_path / "components"
    directory.mkdir()
    (directory / "sample.md").write_text(
        "<!-- composed-component: sample -->", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="superseded composed-component pointer"):
        inline.inline_components("[Sample](components/sample.md)\n", directory)


def test_legacy_seam_expands_regions_and_refuses_superseded_includes():
    seam = module("injected_seam", "procedures/memory/storage-backends/seam.py")
    document = '## sample\n\n@start region id="body"\nfirst\n@end region\n'
    assert seam.extract_section(document, "sample") == "first"
    document = (
        '## sample\n\n@start region id="a"\nfirst\n@end region\n'
        '@start region id="b"\nsecond\n@end region\n'
    )
    assert seam.extract_section(document, "sample") == "first\nsecond"
    with pytest.raises(ValueError, match="superseded composed-source"):
        seam.extract_section(
            "## sample\n\n<!-- composed-source: procedures/sections/body.md -->\n",
            "sample",
        )
