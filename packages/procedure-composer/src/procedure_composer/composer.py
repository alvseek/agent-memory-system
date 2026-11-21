"""Compose single-file procedure documents for one storage backend.

An authored document owns its generic prose. Paired references insert a canonical
component or one named region of the selected backend document at the point of use. The
composer returns both the rendered text and the full owning documents that produced it,
so an editor can always open and save the complete source rather than a rendered span.

The format is data only. Nothing here evaluates an expression, imports authored code, or
falls back to the superseded fragmented assembly format.
"""

from __future__ import annotations

import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Protocol

from .document import (
    BACKENDS,
    FORMAT_VERSION,
    BackendDocument,
    CompositionError,
    Document,
    Prose,
    Reference,
    _path,
    backend_path,
    parse_backend_document,
    parse_document,
)

_ASSEMBLIES = "procedures/assemblies"
_PROCEDURE_DIRS = ("procedures", "procedures/memory")
_COMPONENT_DIR = "procedures/components"
_EXTERNAL_DIR = "procedures/external"
_BACKEND_DIR = "procedures/memory/storage-backends"
_BACKEND_DOCUMENTS = tuple(f"{_BACKEND_DIR}/{backend}.md" for backend in BACKENDS)


def _linked(path: Path) -> bool:
    """Windows junctions are reparse points even on Python before is_junction."""
    return path.is_symlink() or bool(
        getattr(path.lstat(), "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    )


class SourceProvider(Protocol):
    """A single immutable revision. Providers reject unsafe/non-regular Git entries."""

    def read(self, path: str) -> bytes: ...

    def paths(self, directory: str) -> tuple[str, ...]: ...


class MemorySource:
    """Immutable bytes, suitable for a revision-pinned remote tree or draft overlay."""

    def __init__(self, files: Mapping[str, bytes]) -> None:
        self._files = {_path(path): bytes(data) for path, data in files.items()}

    def read(self, path: str) -> bytes:
        try:
            return self._files[_path(path)]
        except KeyError as exc:
            raise CompositionError(f"missing source: {path}") from exc

    def paths(self, directory: str) -> tuple[str, ...]:
        prefix = _path(directory) + "/"
        return tuple(sorted(path for path in self._files if path.startswith(prefix)))


class FileSource(MemorySource):
    """Snapshot regular files beneath the ``procedures/`` tree; never traverse links.

    The procedures tree is the authoring and delivery surface: procedure, component,
    external and backend documents all live inside it. A nested repository, symlink or
    Windows junction is refused instead of following data outside the content root.
    """

    _TREE = "procedures"

    def __init__(self, root: Path) -> None:
        root = Path(root)
        if _linked(root):
            raise CompositionError("source root must not be a symlink")
        root = root.resolve(strict=True)
        files: dict[str, bytes] = {}

        def walk(directory: Path) -> None:
            if _linked(directory):
                raise CompositionError(f"linked source directory: {directory}")
            if (directory / ".git").exists():
                raise CompositionError(f"nested repository: {directory}")
            for path in sorted(directory.iterdir()):
                if _linked(path):
                    raise CompositionError(f"linked source: {path}")
                if path.is_dir():
                    walk(path)
                elif path.is_file():
                    files[path.relative_to(root).as_posix()] = path.read_bytes()
                else:
                    raise CompositionError(f"non-regular source: {path}")

        # Check every ancestor too: otherwise a linked procedures/ bypasses walk.
        target = root
        for part in Path(self._TREE).parts:
            target = target / part
            if target.exists() and _linked(target):
                raise CompositionError(f"linked source directory: {target}")
            if target.exists() and (target / ".git").exists():
                raise CompositionError(f"nested repository: {target}")
        if target.exists():
            walk(target)
        super().__init__(files)


@dataclass(frozen=True)
class Span:
    """One ordered piece of rendered text and the full document that owns it."""

    kind: str
    document_id: str
    path: str
    document_sha256: str
    text: str
    id: str | None = None
    target: str | None = None
    backend_applicability: tuple[str, ...] = BACKENDS


@dataclass(frozen=True)
class DocumentEdit:
    """The complete owning document bytes, never a rendered span."""

    id: str
    kind: str
    path: str
    sha256: str
    raw: bytes


@dataclass(frozen=True)
class Composition:
    format_version: int
    procedure_id: str
    title: str
    description: str
    argument_name: str | None
    argument_description: str | None
    text: str
    spans: tuple[Span, ...]
    calls: tuple[str, ...]
    documents: tuple[DocumentEdit, ...]


def _direct(source_provider: SourceProvider, directory: str) -> tuple[str, ...]:
    prefix = directory + "/"
    selected = []
    for path in source_provider.paths(directory):
        if not path.startswith(prefix):
            continue
        if "/" not in path[len(prefix) :]:
            selected.append(path)
    return tuple(sorted(selected))


class Catalog:
    """Every supported version-2 document in one immutable source revision."""

    def __init__(self, source_provider: SourceProvider) -> None:
        self.source = source_provider
        self.documents: dict[str, Document] = {}
        self._by_path: dict[str, Document] = {}
        self._backend_cache: dict[str, BackendDocument] = {}
        self._refuse_fragmented_catalog()
        self._discover()
        self._check_backend_documents()

    def _refuse_fragmented_catalog(self) -> None:
        legacy = [path for path in self.source.paths(_ASSEMBLIES) if path.endswith(".toml")]
        if legacy:
            raise CompositionError(
                "unsupported format_version 1 fragmented assembly catalog; "
                "single-file format_version 2 documents replace it"
            )

    def _discover(self) -> None:
        groups = (
            *((directory, "procedure") for directory in _PROCEDURE_DIRS),
            (_COMPONENT_DIR, "component"),
            (_EXTERNAL_DIR, "external"),
        )
        for directory, expected_kind in groups:
            for path in _direct(self.source, directory):
                if not path.endswith(".md"):
                    continue
                raw = self.source.read(path)
                if raw.startswith(b"\xef\xbb\xbf+++"):
                    raise CompositionError(
                        f"document must not start with a byte-order mark: {path}"
                    )
                if not raw.startswith(b"+++"):
                    continue
                document = parse_document(path, raw)
                if document.metadata.kind != expected_kind:
                    raise CompositionError(
                        f"{path} declares kind {document.metadata.kind!r}; "
                        f"this directory holds {expected_kind!r} documents"
                    )
                if Path(path).stem != document.metadata.id:
                    raise CompositionError(
                        f"document filename must identify {document.metadata.id}: {path}"
                    )
                if document.metadata.id in self.documents:
                    raise CompositionError(f"duplicate document identity: {document.metadata.id}")
                self.documents[document.metadata.id] = document
                self._by_path[path] = document

    def _check_backend_documents(self) -> None:
        for path in _BACKEND_DOCUMENTS:
            if path in self.source.paths(_BACKEND_DIR):
                self.backend_document(path)

    @property
    def procedures(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                identity
                for identity, document in self.documents.items()
                if document.metadata.kind == "procedure"
            )
        )

    def backend_document(self, path: str) -> BackendDocument:
        cached = self._backend_cache.get(path)
        if cached is not None:
            return cached
        raw = self.source.read(path)
        document = parse_backend_document(path, raw)
        self._backend_cache[path] = document
        return document

    def _component(self, reference: Reference) -> Document:
        document = self._by_path.get(reference.ref)
        if document is None:
            raise CompositionError(f"missing component: {reference.ref}")
        if document.metadata.kind != "component":
            raise CompositionError(f"not a component: {document.metadata.id}")
        return document

    def compose(self, document_id: str, backend: str) -> Composition:
        if backend not in BACKENDS:
            raise CompositionError(f"unknown backend: {backend}")
        document = self.documents.get(document_id)
        if document is None:
            raise CompositionError(f"unknown document: {document_id}")
        renderer = _Renderer(self, backend)
        renderer.render(document, (document_id,), None)
        metadata = document.metadata
        return Composition(
            FORMAT_VERSION,
            metadata.id,
            metadata.title,
            metadata.description,
            metadata.argument_name,
            metadata.argument_description,
            renderer.text(),
            tuple(renderer.spans),
            tuple(dict.fromkeys(renderer.calls)),
            tuple(renderer.documents),
        )

    def dependents(self, source_path: str) -> tuple[str, ...]:
        """Procedures and external consumers whose compositions read this whole file."""
        source_path = _path(source_path)
        affected = []
        for identity in sorted(self.documents):
            document = self.documents[identity]
            if document.metadata.kind not in ("procedure", "external"):
                continue
            reachable = {document.path}
            self._reachable(document, reachable, {identity}, set(BACKENDS), {})
            if source_path in reachable:
                affected.append(identity)
        return tuple(affected)

    def _reachable(
        self,
        document: Document,
        found: set[str],
        stack: set[str],
        backends: set[str],
        seen: dict[str, set[str]],
    ) -> None:
        previous = seen.get(document.metadata.id, set())
        fresh = backends - previous
        if not fresh:
            return
        seen[document.metadata.id] = previous | fresh
        for node in document.nodes:
            if not isinstance(node, Reference):
                continue
            effective = fresh & set(node.applies_to)
            if not effective:
                continue
            if node.kind == "component":
                found.add(node.ref)
                target = self._by_path.get(node.ref)
                if target is not None and target.metadata.id not in stack:
                    self._reachable(
                        target,
                        found,
                        stack | {target.metadata.id},
                        effective,
                        seen,
                    )
                continue
            for backend in effective:
                found.add(backend_path(node.ref, backend))

    def validate(self) -> None:
        for identity in self.documents:
            for backend in BACKENDS:
                self.compose(identity, backend)
        for path in _BACKEND_DOCUMENTS:
            if path in self.source.paths(_BACKEND_DIR):
                self.backend_document(path)


class _Renderer:
    def __init__(self, catalog: Catalog, backend: str) -> None:
        self.catalog = catalog
        self.backend = backend
        self._parts: list[str] = []
        self.spans: list[Span] = []
        self.calls: list[str] = []
        self.documents: list[DocumentEdit] = []
        self._seen_documents: set[str] = set()

    def text(self) -> str:
        return "".join(self._parts)

    def _enter(self, document: Document) -> None:
        if document.path not in self._seen_documents:
            self._seen_documents.add(document.path)
            self.documents.append(
                DocumentEdit(
                    document.metadata.id,
                    document.metadata.kind,
                    document.path,
                    document.sha256,
                    document.raw,
                )
            )
        self.calls.extend(document.metadata.calls_for(self.backend))

    def _enter_backend(self, path: str, raw: bytes, sha256: str) -> None:
        if path in self._seen_documents:
            return
        self._seen_documents.add(path)
        self.documents.append(DocumentEdit(Path(path).stem, "backend", path, sha256, raw))

    def render(
        self,
        document: Document,
        stack: tuple[str, ...],
        reference_id: str | None,
        applies_to: tuple[str, ...] = BACKENDS,
    ) -> None:
        self._enter(document)
        for node in document.nodes:
            if isinstance(node, Prose):
                self._prose(node.text, document, reference_id, applies_to)
            elif node.kind == "component":
                self._component(node, stack, applies_to)
            else:
                self._storage(node)

    def _prose(
        self,
        text: str,
        document: Document,
        reference_id: str | None,
        applies_to: tuple[str, ...],
    ) -> None:
        if not text:
            return
        self._parts.append(text)
        self.spans.append(
            Span(
                "component" if document.metadata.kind == "component" else "text",
                document.metadata.id,
                document.path,
                document.sha256,
                text,
                id=reference_id if document.metadata.kind == "component" else None,
                backend_applicability=applies_to,
            )
        )

    def _component(
        self,
        reference: Reference,
        stack: tuple[str, ...],
        applies_to: tuple[str, ...],
    ) -> None:
        effective = tuple(backend for backend in applies_to if backend in reference.applies_to)
        if self.backend not in effective:
            return
        document = self.catalog._component(reference)
        if document.metadata.id in stack:
            chain = " -> ".join((*stack, document.metadata.id))
            raise CompositionError(f"component cycle: {chain}")
        before = len(self.spans)
        self.render(
            document,
            (*stack, document.metadata.id),
            reference.id,
            effective,
        )
        if len(self.spans) == before:
            self.spans.append(
                Span(
                    "component",
                    document.metadata.id,
                    document.path,
                    document.sha256,
                    "",
                    id=reference.id,
                    backend_applicability=effective,
                )
            )

    def _storage(self, reference: Reference) -> None:
        if self.backend not in reference.applies_to:
            return
        path = backend_path(reference.ref, self.backend)
        backend = self.catalog.backend_document(path)
        region = backend.region(reference.target)
        self._enter_backend(backend.path, backend.raw, backend.sha256)
        self._parts.append(region)
        self.spans.append(
            Span(
                "storage",
                Path(path).stem,
                backend.path,
                backend.sha256,
                region,
                id=reference.id,
                target=reference.target,
                backend_applicability=(self.backend,),
            )
        )


def compose(procedure_id: str, backend: str, source_provider: SourceProvider) -> Composition:
    return Catalog(source_provider).compose(procedure_id, backend)


def validate_catalog(source_provider: SourceProvider) -> Catalog:
    catalog = Catalog(source_provider)
    catalog.validate()
    return catalog


def dependents(source_path: str, source_provider: SourceProvider) -> tuple[str, ...]:
    return Catalog(source_provider).dependents(source_path)
