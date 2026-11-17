# Procedure composer

This pure Python 3.11+ package turns an ordered TOML assembly and UTF-8 section
files into procedure text and source provenance. It does not call a server,
GitHub, a shell, or code from the content being rendered.

Install this directory as a package. Consumers pin its immutable release/source
revision; an editing branch supplies data to the installed package, never code.

```python
from pathlib import Path
from procedure_composer import FileSource, compose, validate_catalog

source = FileSource(Path("<configured-content-root>"))
catalog = validate_catalog(source)
result = compose("<procedure-id>", "db", source)
```

`MemorySource` snapshots a path-to-bytes mapping for remote trees and unsaved
overlays. Remote adapters must reject Git symlinks and gitlinks before passing
regular-file bytes to it. `FileSource` snapshots regular files from the configured
assembly/section directories and refuses linked directories and nested repositories.

Each `procedures/assemblies/*.toml` declares `format_version = 1`, `id`, `title`,
`description`, optional paired `argument_name`/`argument_description`, optional
explicit `calls`, and ordered `[[sections]]`. A node has a stable `id` and exactly
one selector: `source`, `component`, or `[sections.backends]` with both `markdown`
and `db` paths. Component assemblies declare `kind = "component"`.
An explicit `applies_to = ["db"]` or `["markdown"]` limits a node to that backend;
omitting it means both. Backend alternatives must still name both variants, so a
missing variant is not silently treated as a deliberate omission.
Node `calls` can declare backend-specific procedure dependencies, for example
`calls = { markdown = ["<procedure-id>"], db = [] }`. Shared dependencies use the
assembly's top-level `calls`. Delivery validates them against its actual command
catalog; explanatory mentions are not inferred as calls.
An `external` assembly declares the canonical sections/components reused by a
legacy consumer. It contributes to reverse dependencies but is never served as a
standalone procedure; the legacy consumer still owns its complete flow.

Sources must be `.md` files beneath `procedures/sections/`. IDs are authored, not
derived from headings. Each manifest's filename stem matches its declared ID.
Repeated component appearances reuse their source identity;
conflicting definitions and duplicate nodes in one assembly are errors.
Sections concatenate without inferred separators: whitespace belongs to the
authored source. UTF-8 bytes, including line endings, are preserved.

`Composition` returns version, procedure metadata, exact text, declared call
dependencies and ordered `Section` values. Each section includes identity,
relative source path, SHA-256 and backend applicability. `dependents(source_id,
source_provider, source_path=...)` derives affected procedures for the selected
authored file rather than conflating distinct backend variants. `validate_catalog` checks every
assembly on both backends. Unsupported versions, missing sources, path escapes,
invalid selectors and cycles fail explicitly; consumers must not fall back to a
legacy rendering for a converted ID.
