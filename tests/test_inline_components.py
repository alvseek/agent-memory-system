"""inline.py — component inlining, the stage before seam composition.

Lives beside the seam's test, inside control-files. The module sits next to the
components it serves (``procedures/components/inline.py``) so both this tool and
Munnin's ContentLoader import the same implementation; it is loaded by file path.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

CF = Path(__file__).resolve().parents[1]  # control-files/
_MODULE = CF / "procedures" / "components" / "inline.py"
COMPONENTS = CF / "procedures" / "components"

_spec = importlib.util.spec_from_file_location("cf_inline", _MODULE)
inline = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(inline)


def _write(d: Path, name: str, body: str, header: bool = True) -> None:
    head = f"# {name} (component)\n\nA component.\n\n---\n\n" if header else ""
    (d / f"{name}.md").write_text(head + body, encoding="utf-8")


# --- body extraction ---


def test_body_is_what_follows_the_rule() -> None:
    doc = "# Title (component)\n\nHeader prose.\n\n---\n\nTHE BODY\n"
    assert inline.component_body(doc) == "THE BODY"


def test_body_without_rule_drops_only_the_h1() -> None:
    assert inline.component_body("# Title\n\nTHE BODY\n") == "THE BODY"
    assert inline.component_body("THE BODY\n") == "THE BODY"


# --- inlining ---


def test_link_becomes_label_and_body_follows(tmp_path: Path) -> None:
    _write(tmp_path, "warn", "Do not delegate.")
    text, missing, used = inline.inline_components(
        "Step 1\n\n[**Careful**](components/warn.md)\n\nStep 2\n", tmp_path
    )
    assert missing == []
    assert used == ["warn"]
    assert "components/warn.md" not in text  # no reference to a file the agent can't reach
    assert "**Careful**" in text  # caller's own wording survives the de-link
    assert "Do not delegate." in text
    assert text.index("**Careful**") < text.index("Do not delegate.")
    assert "Step 1" in text and "Step 2" in text


def test_any_path_prefix_resolves(tmp_path: Path) -> None:
    _write(tmp_path, "warn", "BODY")
    for ref in (
        "[x](components/warn.md)",
        "[x](../components/warn.md)",
        "[x]([AGENT-MEMORY-PATH]/control-files/procedures/components/warn.md)",
    ):
        text, missing, _ = inline.inline_components(ref + "\n", tmp_path)
        assert missing == [] and "BODY" in text, ref


def test_non_component_links_are_left_alone(tmp_path: Path) -> None:
    _write(tmp_path, "warn", "BODY")
    text, _, _ = inline.inline_components(
        "See [the map](docs/orientation-map.md) and [x](components/warn.md)\n", tmp_path
    )
    assert "[the map](docs/orientation-map.md)" in text  # unrelated link untouched
    assert "BODY" in text


def test_nested_components_are_inlined(tmp_path: Path) -> None:
    _write(tmp_path, "inner", "INNER BODY")
    _write(tmp_path, "outer", "OUTER BODY\n\n[y](components/inner.md)")
    text, missing, used = inline.inline_components("[x](components/outer.md)\n", tmp_path)
    assert missing == []
    assert set(used) == {"inner", "outer"}
    assert "OUTER BODY" in text and "INNER BODY" in text
    assert "components/inner.md" not in text


def test_missing_component_is_reported_and_left_visible(tmp_path: Path) -> None:
    text, missing, used = inline.inline_components("[x](components/ghost.md)\n", tmp_path)
    assert missing == ["ghost"]
    assert used == []
    assert "components/ghost.md" in text  # unresolved reference stays visible, never silent


def test_circular_reference_is_reported_not_hung(tmp_path: Path) -> None:
    _write(tmp_path, "a", "A BODY\n\n[b](components/b.md)")
    _write(tmp_path, "b", "B BODY\n\n[a](components/a.md)")
    text, missing, _ = inline.inline_components("[a](components/a.md)\n", tmp_path)
    assert any("circular" in m for m in missing)
    assert "A BODY" in text


def test_text_without_components_is_untouched(tmp_path: Path) -> None:
    src = "# Procedure\n\nNothing shared here.\n"
    text, missing, used = inline.inline_components(src, tmp_path)
    assert (text, missing, used) == (src, [], [])


# --- the real tree ---


def test_shipped_components_all_have_a_body() -> None:
    shipped = [p for p in COMPONENTS.glob("*.md") if p.stem != "README"]
    assert shipped, "no components found — the contract folder should not be empty"
    for path in shipped:
        assert inline.component_body(path.read_text(encoding="utf-8")).strip()
