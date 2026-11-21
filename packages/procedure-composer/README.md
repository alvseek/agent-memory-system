# Procedure composer

This pure Python 3.11+ package turns one readable Markdown document per procedure or
component into procedure text and source provenance. It does not call a server, GitHub,
a shell, or code from the content being rendered.

Install this directory as a package. Consumers pin its immutable release/source
revision; an editing branch supplies data to the installed package, never code.

```python
from pathlib import Path
from procedure_composer import FileSource, compose, validate_catalog

source = FileSource(Path("<configured-content-root>"))
catalog = validate_catalog(source)
result = compose("<procedure-id>", "db", source)
```

`MemorySource` snapshots a path-to-bytes mapping for remote trees and unsaved overlays.
Remote adapters must reject Git symlinks and gitlinks before passing regular-file bytes
to it. `FileSource` snapshots regular files beneath the content root's `procedures/`
tree and refuses linked directories and nested repositories.

## One document, one readable source

A procedure or component is one Markdown file with a `+++`-delimited TOML header. The
header is metadata, not delivered instructions. The body is the generic prose; paired
`@start`/`@end` lines mark where canonical content expands.

```markdown
+++
format_version = 2
id = "wrap-up"
kind = "procedure"
title = "Wrap Up Session"
description = "End-of-session memory orchestrator."
calls = { markdown = ["update-memory", "push-memory"], db = ["update-memory"] }
+++
## Procedure

Update the session's memory.

@start component id="wrap-up.rules" ref="procedures/components/no-subagent-load.md"
@end component

Persist it using the active storage backend.

@start storage id="wrap-up.persist-store" ref="procedures/memory/storage-backends/{backend}.md" target="wrap-up.persist-store"
@end storage

Report the remaining work.
```

A component reference expands the referenced component document's complete body. A
storage reference expands one named region of the selected backend document:

```markdown
@start region id="wrap-up.persist-store"
The actual instructions for this backend live here.
@end region
```

Reference interiors are empty. Cached composed text in a source file is rejected; the
canonical text has exactly one home. Reference identities are unique within a document,
and region identities are unique within a backend document.

A reference may be gated to one backend with `applies_to="db"` or
`applies_to="markdown"`; omitting it means both. A region may declare
`ending="none"` when its authored body deliberately has no final newline — the structural
line break before `@end region` is then not content. `ending` is the only region attribute
besides `id`.

Directive lines are removed with their line terminator; every other byte is preserved.
Blank lines around a reference are authored content, not composer trimming. UTF-8,
Unicode and LF/CRLF/CR are preserved exactly.

A directive inside fenced code is literal, so examples never expand and a printed template
keeps its text. An unterminated fence is an error rather than a silent truncation of the
document's references.

## Metadata

Allowed header fields are `format_version` (must be `2`), `id`, `kind`, `title`,
`description`, optional paired `argument_name`/`argument_description`, and `calls`.

`kind` is `procedure`, `component`, or `external`. An external document declares
dependencies of a legacy consumer; it contributes to reverse dependencies but is never
served as a procedure.

`calls` is either a shared list or an explicit table naming both backends:

```toml
calls = ["update-memory"]
calls = { markdown = ["update-memory", "push-memory"], db = ["update-memory"] }
```

The backend table is deliberately exhaustive: a missing variant is an error, not a
silent omission. Component calls join the procedure's calls in expansion order without
duplicates.

## Discovery and confinement

The catalog scans direct `.md` files in:

- `procedures/` and `procedures/memory/` for `procedure` documents;
- `procedures/components/` for `component` documents;
- `procedures/external/` for `external` documents.

A file without a `+++` header is left alone as a legacy command. A file with a header
must declare the kind its directory holds, and its filename stem must match its `id`.

A component reference must resolve to a discovered component document under
`procedures/components/`. A storage reference must use `{backend}` exactly once and
resolve to `procedures/memory/storage-backends/{db,markdown}.md`. Paths are
repository-root-relative, confined, and never absolute.

## Composition and provenance

`Composition` returns:

- `format_version`, procedure metadata, exact `text`, declared `calls`;
- `spans`: ordered provenance for each rendered piece, with the owning document's
  identity, path and full-file SHA-256, backend applicability, and the optional
  reference/region identity;
- `documents`: the complete bytes and hash of every owning document that contributed.

A span's text is rendered output, never an edit target. An editor opens and saves the
complete document named by `DocumentEdit`; the full-file hash is the revision guard.
`dependents(document_path, source)` derives every procedure and external consumer of a
whole file, including transitive component reads and both backend documents, so a
backend-file edit discloses its full impact rather than only the clicked region.

Every document and both backends are validated. Missing components or regions, cycles,
unsafe paths, duplicate identities, unsupported metadata and the superseded
`format_version 1` fragmented assemblies fail explicitly. There is no fallback reader
for the old format and no legacy rendering for a converted ID.

Legacy heading-based backend sections and unconverted procedures may coexist with named
regions; the legacy adapters keep their own extraction behavior and use
`expand_regions(text)` to replace region blocks with their bodies. New directive lines
are never delivered as instruction text by this composer.
