"""An assembly is ordered data. All editable text comes from declared section files."""

from __future__ import annotations

import hashlib
import re
import stat
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Mapping, Protocol

FORMAT_VERSION = 1
BACKENDS = ("markdown", "db")
_ID = re.compile(r"[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*\Z")
_ASSEMBLIES = "procedures/assemblies"
_SECTIONS = "procedures/sections/"


class CompositionError(ValueError):
    """Invalid or unsupported authored data; callers must not silently fall back."""


def _linked(path: Path) -> bool:
    """Windows junctions are reparse points even on Python before is_junction."""
    return path.is_symlink() or bool(
        getattr(path.lstat(), "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    )


def _path(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise CompositionError(f"unsafe source path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in ("", ".", "..") for p in value.split("/")):
        raise CompositionError(f"unsafe source path: {value!r}")
    return value


class SourceProvider(Protocol):
    """A single immutable revision. Providers reject unsafe/non-regular Git entries."""

    def read(self, path: str) -> bytes: ...

    def paths(self, directory: str) -> tuple[str, ...]: ...


class MemorySource:
    """Immutable bytes, suitable for a revision-pinned remote tree or draft overlay."""

    def __init__(self, files: Mapping[str, bytes]) -> None:
        self._files = {_path(p): bytes(data) for p, data in files.items()}

    def read(self, path: str) -> bytes:
        try:
            return self._files[_path(path)]
        except KeyError as exc:
            raise CompositionError(f"missing source: {path}") from exc

    def paths(self, directory: str) -> tuple[str, ...]:
        prefix = _path(directory) + "/"
        return tuple(sorted(p for p in self._files if p.startswith(prefix)))


class FileSource(MemorySource):
    """Snapshot regular files beneath a caller-supplied root; never traverse links.

    Only assembly and section directories are captured. A nested repository, symlink
    or Windows junction is refused instead of following data outside the source root.
    """

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
        for relative in (_ASSEMBLIES, _SECTIONS.rstrip("/")):
            target = root
            for part in PurePosixPath(relative).parts:
                target = target / part
                if target.exists() and _linked(target):
                    raise CompositionError(f"linked source directory: {target}")
                if target.exists() and (target / ".git").exists():
                    raise CompositionError(f"nested repository: {target}")
            if target.exists():
                walk(target)
        super().__init__(files)


@dataclass(frozen=True)
class Section:
    id: str
    source: str
    source_hash: str
    backend_applicability: tuple[str, ...]
    text: str


@dataclass(frozen=True)
class Composition:
    format_version: int
    procedure_id: str
    title: str
    description: str
    argument_name: str | None
    argument_description: str | None
    text: str
    sections: tuple[Section, ...]
    calls: tuple[str, ...]


def _identifier(value: object) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise CompositionError(f"invalid authored identity: {value!r}")
    return value


class Catalog:
    def __init__(self, source_provider: SourceProvider) -> None:
        self.source = source_provider
        self.entries: dict[str, dict] = {}
        self.manifest_paths: dict[str, str] = {}
        self._identities: dict[str, tuple] = {}
        self._source_owners: dict[str, str] = {}
        for path in source_provider.paths(_ASSEMBLIES):
            _path(path)
            if not path.endswith(".toml"):
                continue
            try:
                data = tomllib.loads(source_provider.read(path).decode("utf-8"))
            except (UnicodeError, tomllib.TOMLDecodeError) as exc:
                raise CompositionError(f"invalid assembly: {path}: {exc}") from exc
            allowed = {"format_version", "id", "title", "description", "argument_name",
                       "argument_description", "sections", "kind", "calls"}
            if set(data) - allowed:
                raise CompositionError(f"unknown assembly fields: {path}")
            if type(data.get("format_version")) is not int or data["format_version"] != 1:
                raise CompositionError(f"unsupported format version: {path}")
            identity = _identifier(data.get("id"))
            if identity in self.entries:
                raise CompositionError(f"duplicate assembly ID: {identity}")
            if PurePosixPath(path).stem != identity:
                raise CompositionError(f"assembly filename must identify {identity}: {path}")
            if data.get("kind", "procedure") not in ("procedure", "component", "external"):
                raise CompositionError(f"unknown assembly kind: {path}")
            for field in ("title", "description"):
                if not isinstance(data.get(field), str) or not data[field]:
                    raise CompositionError(f"missing {field}: {path}")
            if ("argument_name" in data) != ("argument_description" in data):
                raise CompositionError(f"incomplete argument metadata: {path}")
            for field in ("argument_name", "argument_description"):
                if field in data and not isinstance(data[field], str):
                    raise CompositionError(f"invalid argument metadata: {path}")
            calls = data.get("calls", [])
            if not isinstance(calls, list):
                raise CompositionError(f"invalid calls: {path}")
            for call in calls:
                _identifier(call)
            if not isinstance(data.get("sections"), list) or not data["sections"]:
                raise CompositionError(f"missing ordered sections: {path}")
            local_ids = set()
            for node in data["sections"]:
                self._check_node(node, local_ids)
            self.entries[identity] = data
            self.manifest_paths[identity] = path

    def _check_node(self, node: dict, local_ids: set) -> None:
        if not isinstance(node, dict) or set(node) - {
            "id", "source", "backends", "component", "applies_to",
            "calls",
        }:
            raise CompositionError("unknown section selector")
        applies = node.get("applies_to", list(BACKENDS))
        if (not isinstance(applies, list) or not applies
                or any(not isinstance(item, str) for item in applies)
                or len(set(applies)) != len(applies) or set(applies) - set(BACKENDS)):
            raise CompositionError("invalid explicit backend applicability")
        calls = node.get("calls", {})
        if not isinstance(calls, dict) or set(calls) - set(BACKENDS):
            raise CompositionError("invalid backend call dependencies")
        for targets in calls.values():
            if not isinstance(targets, list):
                raise CompositionError("call dependencies must be lists")
            for target in targets:
                _identifier(target)
        identity = _identifier(node.get("id"))
        if identity in local_ids:
            raise CompositionError(f"duplicate section ID: {identity}")
        local_ids.add(identity)
        selectors = set(node) & {"source", "backends", "component"}
        if len(selectors) != 1:
            raise CompositionError(f"section must select exactly one source: {identity}")
        if "component" in node:
            _identifier(node["component"])
            signature = ("component", node["component"])
        else:
            variants = node.get("backends")
            if variants is not None:
                if not isinstance(variants, dict) or set(variants) != set(BACKENDS):
                    raise CompositionError(f"backend alternatives must cover {BACKENDS}")
            else:
                variants = {b: node["source"] for b in BACKENDS}
            for path in variants.values():
                _path(path)
                if not path.startswith(_SECTIONS) or not path.endswith(".md"):
                    raise CompositionError(f"undeclared section directory/type: {path}")
                owner = self._source_owners.setdefault(path, identity)
                if owner != identity:
                    raise CompositionError(f"source has multiple section identities: {path}")
            signature = tuple(sorted(variants.items()))
        previous = self._identities.setdefault(identity, signature)
        if previous != signature:
            raise CompositionError(f"section ID has conflicting sources: {identity}")

    @property
    def procedures(self) -> tuple[str, ...]:
        return tuple(sorted(k for k, v in self.entries.items()
                            if v.get("kind", "procedure") == "procedure"))

    def compose(self, procedure_id: str, backend: str) -> Composition:
        if backend not in BACKENDS:
            raise CompositionError(f"unknown backend: {backend}")
        if procedure_id not in self.entries:
            raise CompositionError(f"unknown assembly: {procedure_id}")
        sections: list[Section] = []
        calls: list[str] = []

        def expand(identity: str, stack: tuple[str, ...]) -> None:
            if identity in stack:
                raise CompositionError(f"component cycle: {' -> '.join((*stack, identity))}")
            if identity not in self.entries:
                raise CompositionError(f"missing component: {identity}")
            entry = self.entries[identity]
            calls.extend(entry.get("calls", []))
            for node in entry["sections"]:
                applies = node.get("applies_to", BACKENDS)
                if backend not in applies:
                    continue
                calls.extend(node.get("calls", {}).get(backend, []))
                if "component" in node:
                    target = node["component"]
                    if self.entries.get(target, {}).get("kind") != "component":
                        raise CompositionError(f"not a component: {target}")
                    expand(target, (*stack, identity))
                    continue
                variants = node.get("backends", {b: node.get("source") for b in BACKENDS})
                path = variants[backend]
                raw = self.source.read(path)
                try:
                    text = raw.decode("utf-8")
                except UnicodeError as exc:
                    raise CompositionError(f"section is not UTF-8: {path}") from exc
                sections.append(Section(
                    node["id"], path, hashlib.sha256(raw).hexdigest(),
                    tuple(b for b in BACKENDS if variants[b] == path and b in applies), text,
                ))

        expand(procedure_id, ())
        data = self.entries[procedure_id]
        return Composition(
            FORMAT_VERSION, procedure_id, data["title"], data["description"],
            data.get("argument_name"), data.get("argument_description"),
            "".join(s.text for s in sections), tuple(sections),
            tuple(dict.fromkeys(calls)),
        )

    def dependents(self, source_id: str, *, source_path: str | None = None) -> tuple[str, ...]:
        consumers = sorted(name for name, entry in self.entries.items()
                           if entry.get("kind", "procedure") in ("procedure", "external"))
        return tuple(name for name in consumers if any(
            section.id == source_id and (source_path is None or section.source == source_path)
            for backend in BACKENDS for section in self.compose(name, backend).sections
        ))

    def validate(self) -> None:
        for identity in self.entries:
            for backend in BACKENDS:
                self.compose(identity, backend)


def compose(procedure_id: str, backend: str, source_provider: SourceProvider) -> Composition:
    return Catalog(source_provider).compose(procedure_id, backend)


def validate_catalog(source_provider: SourceProvider) -> Catalog:
    catalog = Catalog(source_provider)
    catalog.validate()
    return catalog


def dependents(
    source_id: str, source_provider: SourceProvider, *, source_path: str | None = None,
) -> tuple[str, ...]:
    return Catalog(source_provider).dependents(source_id, source_path=source_path)
