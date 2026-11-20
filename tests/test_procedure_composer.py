"""The composer reads single-file data only and preserves exact authored UTF-8 text."""

import hashlib
import importlib.util
import os
import sys
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1] / "packages/procedure-composer/src/procedure_composer"
_SPEC = importlib.util.spec_from_file_location(
    "procedure_composer_under_test",
    PACKAGE / "__init__.py",
    submodule_search_locations=[str(PACKAGE)],
)
pc = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = pc
_SPEC.loader.exec_module(pc)

Catalog = pc.Catalog
CompositionError = pc.CompositionError
FileSource = pc.FileSource
MemorySource = pc.MemorySource
compose = pc.compose
dependents = pc.dependents
validate_catalog = pc.validate_catalog


def document(identity="flow", kind="procedure", body="Do the work.\n", calls=""):
    call_line = f"{calls}\n" if calls else ""
    return (
        "+++\n"
        "format_version = 2\n"
        f'id = "{identity}"\n'
        f'kind = "{kind}"\n'
        'title = "Flow"\n'
        'description = "Do the work."\n'
        f"{call_line}"
        "+++\n"
        f"{body}"
    ).encode()


def backend(name, regions):
    text = f"# {name} backend\n\n"
    for identity, body in regions.items():
        text += f'@start region id="{identity}"\n{body}@end region\n\n'
    return text.encode()


def files():
    return {
        "procedures/flow.md": document(body="Exact é\n\r\n終\n"),
        "procedures/components/child.md": document("child", "component", "Child body\n"),
        "procedures/external/legacy.md": document("legacy", "external", "Legacy body\n"),
        "procedures/memory/storage-backends/db.md": backend("db", {"flow.persist": "DB body\n"}),
        "procedures/memory/storage-backends/markdown.md": backend(
            "markdown", {"flow.persist": "MD body\n"}
        ),
    }


def test_exact_bytes_provenance_and_determinism():
    data = files()
    source = MemorySource(data)
    one = compose("flow", "db", source)
    assert one == compose("flow", "db", source)
    raw = data["procedures/flow.md"]
    assert one.text == "Exact é\n\r\n終\n"
    assert one.text.encode() == raw.split(b"+++\n", 2)[2]
    assert one.spans[0].document_id == "flow"
    assert one.spans[0].path == "procedures/flow.md"
    assert one.spans[0].document_sha256 == hashlib.sha256(raw).hexdigest()
    assert one.spans[0].backend_applicability == ("markdown", "db")
    assert one.documents[0].raw == raw
    assert pc.__version__ == "0.2.0"


def test_immutable_snapshot():
    data = files()
    source = MemorySource(data)
    data["procedures/flow.md"] = b"changed"
    assert compose("flow", "db", source).text != "changed"


def test_component_storage_spans_and_full_documents():
    data = files()
    data["procedures/flow.md"] = document(
        body=(
            "Before\n"
            '@start component id="flow.rules" ref="procedures/components/child.md"\n'
            "@end component\n"
            '@start storage id="flow.persist" '
            'ref="procedures/memory/storage-backends/{backend}.md" '
            'target="flow.persist"\n'
            "@end storage\n"
            "After\n"
        )
    )
    db = compose("flow", "db", MemorySource(data))
    markdown = compose("flow", "markdown", MemorySource(data))
    assert db.text == "Before\nChild body\nDB body\nAfter\n"
    assert markdown.text == "Before\nChild body\nMD body\nAfter\n"
    assert [span.kind for span in db.spans] == ["text", "component", "storage", "text"]
    assert [span.id for span in db.spans] == [None, "flow.rules", "flow.persist", None]
    assert db.spans[2].target == "flow.persist"
    assert db.spans[2].backend_applicability == ("db",)
    assert db.spans[2].path == "procedures/memory/storage-backends/db.md"
    assert markdown.spans[2].path == "procedures/memory/storage-backends/markdown.md"
    assert [item.id for item in db.documents] == ["flow", "child", "db"]
    assert db.spans[2].document_id == "db"
    assert db.documents[1].kind == "component"
    assert db.documents[2].kind == "backend"
    assert "@start" not in db.text and "@end" not in db.text


def test_nested_and_repeated_references_keep_order():
    data = files()
    data["procedures/components/grand.md"] = document("grand", "component", "Grand body\n")
    data["procedures/components/child.md"] = document(
        "child",
        "component",
        (
            "Child before\n"
            '@start component id="child.grand" ref="procedures/components/grand.md"\n'
            "@end component\n"
            "Child after\n"
        ),
    )
    data["procedures/flow.md"] = document(
        body=(
            '@start component id="flow.one" ref="procedures/components/child.md"\n'
            "@end component\n"
            '@start component id="flow.two" ref="procedures/components/child.md"\n'
            "@end component\n"
        )
    )
    result = compose("flow", "db", MemorySource(data))
    assert result.text == (
        "Child before\nGrand body\nChild after\nChild before\nGrand body\nChild after\n"
    )
    assert [span.id for span in result.spans] == [
        "flow.one",
        "child.grand",
        "flow.one",
        "flow.two",
        "child.grand",
        "flow.two",
    ]


def test_literal_fenced_examples_are_not_directives():
    data = files()
    data["procedures/flow.md"] = document(
        body=(
            "```markdown\n"
            '@start component id="sample" ref="procedures/components/missing.md"\n'
            "@end component\n"
            "```\n"
            "~~~\n"
            '@start component id="tilde" ref="procedures/components/missing.md"\n'
            "~~~\n"
            "````\n"
            '@start component id="long" ref="procedures/components/missing.md"\n'
            "````\n"
            '@start component id="flow.rules" ref="procedures/components/child.md"\n'
            "@end component\n"
        )
    )
    result = compose("flow", "db", MemorySource(data))
    assert '@start component id="sample"' in result.text
    assert '@start component id="tilde"' in result.text
    assert '@start component id="long"' in result.text
    assert "Child body" in result.text
    assert "missing component" not in result.text

    data["procedures/memory/storage-backends/db.md"] = (
        b'# DB\n\n```\n@start region id="example"\nnot a region\n@end region\n```\n'
        b'@start region id="flow.persist"\nDB body\n@end region\n'
    )
    backend = Catalog(MemorySource(data)).backend_document(
        "procedures/memory/storage-backends/db.md"
    )
    assert backend.region("flow.persist") == "DB body\n"
    assert dict(backend.regions).get("example") is None


@pytest.mark.parametrize(
    "body",
    [
        # duplicate reference identity
        (
            '@start component id="x" ref="procedures/components/child.md"\n@end component\n'
            '@start component id="x" ref="procedures/components/child.md"\n@end component\n'
        ),
        # unmatched end
        "@end component\n",
        # nested start
        (
            '@start component id="a" ref="procedures/components/child.md"\n'
            '@start component id="b" ref="procedures/components/child.md"\n'
        ),
        # mismatched end
        ('@start component id="a" ref="procedures/components/child.md"\n@end storage\n'),
        # cached body is not allowed
        (
            '@start component id="a" ref="procedures/components/child.md"\n'
            "cached text\n@end component\n"
        ),
        (
            '@start storage id="a" ref="procedures/memory/storage-backends/{backend}.md" '
            'target="flow.persist"\nCached\n@end storage\n'
        ),
        # unknown / missing / malformed attributes
        (
            '@start component id="a" extra="x" ref="procedures/components/child.md"\n'
            "@end component\n"
        ),
        ('@start component id="a"\n@end component\n'),
        ("@start component id=\"a\" ref='x'\n@end component\n"),
        # directive without a kind
        "@start\n",
        # a region is not a document reference
        '@start region id="a"\ntext\n@end region\n',
        # unterminated fence
        '```markdown\n@start component id="a"\n',
        # unclosed reference
        '@start component id="a" ref="procedures/components/child.md"\n',
    ],
)
def test_malformed_document_directives_fail(body):
    data = files()
    data["procedures/flow.md"] = document(body=body)
    with pytest.raises(CompositionError):
        validate_catalog(MemorySource(data))


@pytest.mark.parametrize(
    "text",
    [
        '@start region id="x"\na\n@end region\n@start region id="x"\nb\n@end region\n',
        '@start region id="x"\na\n@end region\n@end region\n',
        '@start region id="x"\n@start region id="y"\nb\n@end region\n',
        '@start component id="x" ref="procedures/components/child.md"\n@end component\n',
        '@start region id="x" ref="other.md"\n@end region\n',
        '@start region id="x"\n',
    ],
)
def test_malformed_backend_regions_fail(text):
    data = files()
    data["procedures/memory/storage-backends/db.md"] = text.encode()
    with pytest.raises(CompositionError):
        validate_catalog(MemorySource(data))


def test_backend_document_must_not_carry_document_metadata():
    data = files()
    data["procedures/memory/storage-backends/db.md"] = document(
        body='@start region id="flow.persist"\nDB\n@end region\n'
    )
    with pytest.raises(CompositionError, match="must not carry document metadata"):
        validate_catalog(MemorySource(data))


def test_missing_component_target_and_variant():
    data = files()
    data["procedures/flow.md"] = document(
        body=(
            '@start component id="flow.rules" ref="procedures/components/missing.md"\n'
            "@end component\n"
        )
    )
    with pytest.raises(CompositionError, match="missing component"):
        validate_catalog(MemorySource(data))

    data = files()
    data["procedures/flow.md"] = document(
        body=('@start component id="flow.rules" ref="procedures/flow.md"\n@end component\n')
    )
    with pytest.raises(CompositionError, match="not a component"):
        validate_catalog(MemorySource(data))

    data = files()
    data["procedures/memory/storage-backends/db.md"] = backend("db", {})
    data["procedures/flow.md"] = document(
        body=(
            '@start storage id="flow.persist" '
            'ref="procedures/memory/storage-backends/{backend}.md" target="flow.persist"\n'
            "@end storage\n"
        )
    )
    markdown = compose("flow", "markdown", MemorySource(data))
    assert markdown.text == "MD body\n"
    with pytest.raises(CompositionError, match="missing region"):
        compose("flow", "db", MemorySource(data))


@pytest.mark.parametrize(
    "ref",
    [
        "procedures/memory/storage-backends/{backend}/../db.md",
        "procedures/memory/storage-backends/{other}.md",
        "procedures/memory/storage-backends/{backend}.md.extra",
        "procedures/elsewhere/{backend}.md",
        "procedures/memory/storage-backends/db.md",
    ],
)
def test_storage_reference_must_resolve_to_the_consolidated_backend(ref):
    data = files()
    data["procedures/flow.md"] = document(
        body=(f'@start storage id="flow.persist" ref="{ref}" target="flow.persist"\n@end storage\n')
    )
    with pytest.raises(CompositionError):
        validate_catalog(MemorySource(data))


@pytest.mark.parametrize(
    "ref",
    [
        "../escape.md",
        "/absolute.md",
        "C:/escape.md",
        r"procedures\components\child.md",
        "procedures//components/child.md",
        "procedures/components/./child.md",
        "outside.md",
        "procedures/components/{backend}.md",
    ],
)
def test_unsafe_component_references(ref):
    data = files()
    data["procedures/flow.md"] = document(
        body=(f'@start component id="flow.rules" ref="{ref}"\n@end component\n')
    )
    with pytest.raises(CompositionError):
        validate_catalog(MemorySource(data))


def test_component_cycles_are_refused():
    data = files()
    data["procedures/components/child.md"] = document(
        "child",
        "component",
        ('@start component id="child.self" ref="procedures/components/child.md"\n@end component\n'),
    )
    data["procedures/flow.md"] = document(
        body=(
            '@start component id="flow.rules" ref="procedures/components/child.md"\n'
            "@end component\n"
        )
    )
    with pytest.raises(CompositionError, match="cycle"):
        validate_catalog(MemorySource(data))


def test_unsupported_and_fragmented_formats_fail_clearly():
    data = files()
    data["procedures/flow.md"] = document().replace(b"format_version = 2", b"format_version = 1")
    with pytest.raises(CompositionError, match="unsupported format version"):
        Catalog(MemorySource(data))

    data = files()
    data["procedures/flow.md"] = document().replace(b"format_version = 2", b'format_version = "2"')
    with pytest.raises(CompositionError):
        Catalog(MemorySource(data))

    data = files()
    data["procedures/assemblies/flow.toml"] = (
        b'format_version = 1\nid = "flow"\ntitle = "Flow"\ndescription = "Old"\n'
    )
    with pytest.raises(CompositionError, match="fragmented assembly"):
        Catalog(MemorySource(data))


def test_metadata_and_discovery_rules():
    data = files()
    data["procedures/flow.md"] = document().replace(
        b"+++\nformat_version", b"+++\nunknown_field = 1\nformat_version"
    )
    with pytest.raises(CompositionError, match="unknown document fields"):
        Catalog(MemorySource(data))

    data = files()
    data["procedures/flow.md"] = document(identity="different")
    with pytest.raises(CompositionError, match="filename must identify"):
        Catalog(MemorySource(data))

    data = files()
    data["procedures/components/flow.md"] = document("flow", "component")
    with pytest.raises(CompositionError, match="duplicate document identity"):
        Catalog(MemorySource(data))

    data = files()
    data["procedures/components/wrong.md"] = document("wrong", "procedure")
    with pytest.raises(CompositionError, match="this directory holds"):
        Catalog(MemorySource(data))

    data = files()
    data["procedures/readme.md"] = b"# Legacy command, not a document\n"
    assert Catalog(MemorySource(data)).procedures == ("flow",)

    data = files()
    data["procedures/flow.md"] = b"\xef\xbb\xbf" + document()
    with pytest.raises(CompositionError, match="byte-order mark"):
        Catalog(MemorySource(data))


def test_unterminated_header_is_not_treated_as_legacy():
    data = files()
    data["procedures/flow.md"] = b'+++\nformat_version = 2\nid = "flow"\n'
    with pytest.raises(CompositionError, match="unterminated metadata header"):
        Catalog(MemorySource(data))


def test_shared_and_backend_scoped_calls():
    data = files()
    data["procedures/flow.md"] = document(calls='calls = ["update-memory"]')
    assert compose("flow", "db", MemorySource(data)).calls == ("update-memory",)
    assert compose("flow", "markdown", MemorySource(data)).calls == ("update-memory",)

    data["procedures/flow.md"] = document(
        calls=('calls = { markdown = ["update-memory", "push-memory"], db = ["update-memory"] }')
    )
    assert compose("flow", "db", MemorySource(data)).calls == ("update-memory",)
    assert compose("flow", "markdown", MemorySource(data)).calls == (
        "update-memory",
        "push-memory",
    )


def test_component_calls_join_in_expansion_order_without_duplicates():
    data = files()
    data["procedures/components/child.md"] = document(
        "child", "component", "Child\n", calls='calls = ["child-dep", "flow-dep"]'
    )
    data["procedures/flow.md"] = document(
        calls='calls = ["flow-dep"]',
        body=(
            '@start component id="flow.rules" ref="procedures/components/child.md"\n'
            "@end component\n"
        ),
    )
    assert compose("flow", "db", MemorySource(data)).calls == ("flow-dep", "child-dep")


def test_empty_region_and_empty_component_are_tracked():
    data = files()
    data["procedures/memory/storage-backends/db.md"] = backend("db", {"flow.empty": ""})
    data["procedures/components/child.md"] = document("child", "component", "")
    data["procedures/flow.md"] = document(
        body=(
            '@start component id="flow.rules" ref="procedures/components/child.md"\n'
            "@end component\n"
            '@start storage id="flow.empty" '
            'ref="procedures/memory/storage-backends/{backend}.md" target="flow.empty"\n'
            "@end storage\n"
        )
    )
    result = compose("flow", "db", MemorySource(data))
    assert result.text == ""
    assert [span.kind for span in result.spans] == ["component", "storage"]
    assert [span.text for span in result.spans] == ["", ""]


def test_document_level_dependents_include_transitive_component_and_backend_impact():
    data = files()
    data["procedures/components/grand.md"] = document("grand", "component", "Grand\n")
    data["procedures/components/child.md"] = document(
        "child",
        "component",
        (
            '@start component id="child.grand" ref="procedures/components/grand.md"\n'
            "@end component\n"
        ),
    )
    reference = (
        '@start component id="flow.rules" ref="procedures/components/child.md"\n@end component\n'
    )
    data["procedures/flow.md"] = document(body=reference)
    data["procedures/other.md"] = document("other", body=reference)
    data["procedures/external/legacy.md"] = document("legacy", "external", reference)

    source = MemorySource(data)
    assert dependents("procedures/components/grand.md", source) == (
        "flow",
        "legacy",
        "other",
    )
    assert dependents("procedures/components/child.md", source) == (
        "flow",
        "legacy",
        "other",
    )
    assert dependents("procedures/flow.md", source) == ("flow",)
    assert dependents("procedures/components/unused.md", source) == ()

    data["procedures/flow.md"] = document(
        body=(
            '@start storage id="flow.persist" '
            'ref="procedures/memory/storage-backends/{backend}.md" target="flow.persist"\n'
            "@end storage\n"
        )
    )
    data["procedures/other.md"] = document("other", body="No storage here.\n")
    source = MemorySource(data)
    db_path = "procedures/memory/storage-backends/db.md"
    markdown_path = "procedures/memory/storage-backends/markdown.md"
    assert dependents(db_path, source) == ("flow",)
    assert dependents(markdown_path, source) == ("flow",)


def test_newline_unicode_and_blank_lines_are_preserved():
    data = files()
    data["procedures/flow.md"] = (
        b'+++\r\nformat_version = 2\r\nid = "flow"\r\nkind = "procedure"\r\n'
        b'title = "Flow"\r\ndescription = "Do it."\r\n+++\r\n'
        b"Before\r\n\r\n"
        b'@start component id="flow.rules" ref="procedures/components/child.md"\r\n'
        b"@end component\r\n\r\nAfter\r\n"
    )
    data["procedures/components/child.md"] = document("child", "component", "Child é\n").replace(
        b"\n", b"\r\n"
    )
    result = compose("flow", "db", MemorySource(data))
    assert result.text == "Before\r\n\r\nChild é\r\n\r\nAfter\r\n"

    data["procedures/flow.md"] = document(body="A\u2028B\nC\rD\r")
    assert compose("flow", "db", MemorySource(data)).text == "A\u2028B\nC\rD\r"

    data["procedures/flow.md"] = document(body="Line 1\n\nLine 2\n")
    assert compose("flow", "db", MemorySource(data)).text == "Line 1\n\nLine 2\n"


def test_cr_only_document_preserves_source_and_prose():
    data = files()
    path = "procedures/flow.md"
    data[path] = document(body="First\nSecond\n").replace(b"\n", b"\r")
    result = compose("flow", "db", MemorySource(data))
    assert result.text == "First\rSecond\r"
    assert result.documents[0].raw == data[path]


@pytest.mark.parametrize(
    "calls",
    [
        'calls = { markdown = "update-memory", db = [] }',
        "calls = { markdown = [], db = 7 }",
    ],
)
def test_backend_calls_require_arrays(calls):
    data = files()
    data["procedures/flow.md"] = document(calls=calls)
    with pytest.raises(CompositionError, match="backend-scoped calls.*must be lists"):
        Catalog(MemorySource(data))


def test_closing_directive_refuses_attributes():
    data = files()
    data["procedures/flow.md"] = document(
        body=(
            '@start component id="flow.rules" ref="procedures/components/child.md"\n'
            '@end component id="different"\n'
        )
    )
    with pytest.raises(CompositionError, match="@end component takes no attributes"):
        Catalog(MemorySource(data))


def test_filesystem_snapshot_and_nested_repo_refusal(tmp_path):
    for path, raw in files().items():
        destination = tmp_path / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
    (tmp_path / "procedures/sections").mkdir()
    (tmp_path / "procedures/sections/legacy.md").write_bytes(b"legacy\n")
    source = FileSource(tmp_path)
    assert compose("flow", "db", source).text == "Exact é\n\r\n終\n"
    assert source.read("procedures/sections/legacy.md") == b"legacy\n"
    (tmp_path / "procedures/components/.git").write_text("gitdir: elsewhere")
    with pytest.raises(CompositionError, match="nested repository"):
        FileSource(tmp_path)


def test_symlink_refused_even_when_it_points_inside_root(tmp_path):
    target = tmp_path / "real"
    target.mkdir()
    (tmp_path / "procedures").mkdir()
    try:
        os.symlink(target, tmp_path / "procedures/components", target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"host does not permit symlink creation: {exc}")
    with pytest.raises(CompositionError, match="linked"):
        FileSource(tmp_path)


def test_invalid_utf8_unknown_backend_and_missing_document():
    data = files()
    data["procedures/flow.md"] = b"+++\nformat_version = 2\n\xff"
    with pytest.raises(CompositionError, match="UTF-8"):
        Catalog(MemorySource(data))
    data = files()
    data["procedures/memory/storage-backends/db.md"] = b"\xff"
    with pytest.raises(CompositionError, match="UTF-8"):
        Catalog(MemorySource(data))
    source = MemorySource(files())
    with pytest.raises(CompositionError, match="unknown backend"):
        compose("flow", "unknown", source)
    with pytest.raises(CompositionError, match="unknown document"):
        compose("missing", "db", source)


def test_validate_catalog_both_backends():
    catalog = validate_catalog(MemorySource(files()))
    assert catalog.procedures == ("flow",)
    assert catalog.documents["flow"].metadata.title == "Flow"
    assert (
        catalog.backend_document("procedures/memory/storage-backends/db.md").region("flow.persist")
        == "DB body\n"
    )


def test_backend_gated_references_and_document_impact():
    data = files()
    data["procedures/flow.md"] = document(
        body=(
            '@start storage id="flow.db-only" '
            'ref="procedures/memory/storage-backends/{backend}.md" '
            'target="flow.persist" applies_to="db"\n'
            "@end storage\n"
            '@start component id="flow.markdown-only" '
            'ref="procedures/components/child.md" applies_to="markdown"\n'
            "@end component\n"
        )
    )
    db = compose("flow", "db", MemorySource(data))
    markdown = compose("flow", "markdown", MemorySource(data))
    assert db.text == "DB body\n"
    assert markdown.text == "Child body\n"
    assert [span.kind for span in db.spans] == ["storage"]
    assert db.spans[0].backend_applicability == ("db",)
    assert markdown.spans[0].backend_applicability == ("markdown",)
    assert dependents("procedures/memory/storage-backends/db.md", MemorySource(data)) == ("flow",)
    assert dependents("procedures/memory/storage-backends/markdown.md", MemorySource(data)) == ()
    assert dependents("procedures/components/child.md", MemorySource(data)) == ("flow",)

    data["procedures/flow.md"] = document(
        body=(
            '@start component id="flow.db-only" '
            'ref="procedures/components/child.md" applies_to="db"\n'
            "@end component\n"
        )
    )
    assert compose("flow", "db", MemorySource(data)).text == "Child body\n"
    assert compose("flow", "markdown", MemorySource(data)).text == ""
    assert dependents("procedures/components/child.md", MemorySource(data)) == ("flow",)


@pytest.mark.parametrize("value", ["all", "db,db", "", "db,"])
def test_invalid_backend_applicability_fails(value):
    data = files()
    data["procedures/flow.md"] = document(
        body=(
            f'@start component id="flow.rules" '
            f'ref="procedures/components/child.md" applies_to="{value}"\n'
            "@end component\n"
        )
    )
    with pytest.raises(CompositionError):
        validate_catalog(MemorySource(data))


def test_region_ending_none_preserves_an_authored_missing_newline():
    data = files()
    data["procedures/memory/storage-backends/db.md"] = (
        b'@start region id="flow.persist" ending="none"\nDB body\n@end region\n'
    )
    catalog = Catalog(MemorySource(data))
    assert (
        catalog.backend_document("procedures/memory/storage-backends/db.md").region("flow.persist")
        == "DB body"
    )
    data["procedures/flow.md"] = document(
        body=(
            '@start storage id="flow.persist" '
            'ref="procedures/memory/storage-backends/{backend}.md" target="flow.persist"\n'
            "@end storage\n"
        )
    )
    assert compose("flow", "db", MemorySource(data)).text == "DB body"

    data["procedures/memory/storage-backends/db.md"] = (
        b'@start region id="flow.persist" ending="other"\nDB body\n@end region\n'
    )
    with pytest.raises(CompositionError):
        Catalog(MemorySource(data))


def test_forced_reference_inside_fenced_code():
    data = files()
    data["procedures/flow.md"] = document(
        body=(
            "```\n"
            "before\n"
            '@@start storage id="flow.persist" '
            'ref="procedures/memory/storage-backends/{backend}.md" target="flow.persist"\n'
            "@@end storage\n"
            "after\n"
            "```\n"
        )
    )
    result = compose("flow", "db", MemorySource(data))
    assert result.text == "```\nbefore\nDB body\nafter\n```\n"
    assert [span.kind for span in result.spans] == ["text", "storage", "text"]


def test_malformed_document_directives_fail_inside_and_outside_fences():
    data = files()
    data["procedures/flow.md"] = document(
        body='```\n@@start component id="x"\n@end component\n```\n'
    )
    with pytest.raises(CompositionError):
        validate_catalog(MemorySource(data))


def test_expand_regions_drops_only_directive_scaffolding():
    assert (
        pc.expand_regions('Before\n@start region id="a"\nA\n@end region\nAfter\n')
        == "Before\nA\nAfter\n"
    )
    assert pc.expand_regions('@start region id="a" ending="none"\nA\n@end region\n') == "A\n"
    with pytest.raises(CompositionError):
        pc.expand_regions('@start component id="a" ref="x.md"\n@end component\n')
    with pytest.raises(CompositionError):
        pc.expand_regions('@start region id="a"\nA\n')
