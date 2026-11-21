"""Single-file procedure documents: TOML metadata, inline prose, explicit references.

A document is one readable Markdown file. Its ``+++``-delimited TOML header holds the
procedure/component metadata that used to live in a separate ordered assembly. The body
is the instruction prose; paired ``@start``/``@end`` lines reference another document or
a named region of the selected storage-backend document. Directives are recognized only
outside fenced code, so examples stay literal.

Nothing in this module reads a file or writes a rendered span. It parses data and keeps
every byte that is not directive scaffolding, so callers can preserve UTF-8, Unicode and
LF/CRLF/CR exactly.
"""

from __future__ import annotations

import hashlib
import re
import tomllib
from dataclasses import dataclass
from pathlib import PurePosixPath

FORMAT_VERSION = 2
BACKENDS = ("markdown", "db")

KINDS = ("procedure", "component", "external")
REFERENCE_KINDS = ("component", "storage")
REGION_KIND = "region"

_ID = re.compile(r"[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*\Z")
_FENCE = re.compile(r" {0,3}(`{3,}|~{3,})([^\r\n]*)")
_DIRECTIVE = re.compile(r"@(start|end)(?:\s+(.*))?")
_KIND = re.compile(r"([a-z]+)(?:\s+(.*))?")
_ATTRIBUTE = re.compile(r'[ \t]+([a-z][a-z0-9_-]*)="([^"\\\r\n]*)"')

_ALLOWED_METADATA = {
    "format_version",
    "id",
    "kind",
    "title",
    "description",
    "argument_name",
    "argument_description",
    "calls",
}


class CompositionError(ValueError):
    """Invalid or unsupported authored data; callers must not silently fall back."""


def _identifier(value: object, *, field: str = "identity") -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise CompositionError(f"invalid {field}: {value!r}")
    return value


def _path(value: object, *, field: str = "source path") -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise CompositionError(f"unsafe {field}: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in value.split("/")):
        raise CompositionError(f"unsafe {field}: {value!r}")
    return value


@dataclass(frozen=True)
class Metadata:
    format_version: int
    id: str
    kind: str
    title: str
    description: str
    argument_name: str | None
    argument_description: str | None
    calls: tuple[str, ...]
    backend_calls: tuple[tuple[str, tuple[str, ...]], ...]

    def calls_for(self, backend: str) -> tuple[str, ...]:
        if self.backend_calls:
            return dict(self.backend_calls)[backend]
        return self.calls


@dataclass(frozen=True)
class Prose:
    text: str


@dataclass(frozen=True)
class Reference:
    kind: str
    id: str
    ref: str
    target: str | None = None
    applies_to: tuple[str, ...] = BACKENDS


Node = Prose | Reference


@dataclass(frozen=True)
class Document:
    path: str
    raw: bytes
    sha256: str
    metadata: Metadata
    body: str
    nodes: tuple[Node, ...]

    @property
    def references(self) -> tuple[Reference, ...]:
        return tuple(node for node in self.nodes if isinstance(node, Reference))


@dataclass(frozen=True)
class BackendDocument:
    """A storage-backend Markdown document and its named regions, in authored order."""

    path: str
    raw: bytes
    sha256: str
    regions: tuple[tuple[str, str], ...]

    def region(self, identity: str) -> str:
        try:
            return dict(self.regions)[identity]
        except KeyError as exc:
            raise CompositionError(f"missing region {identity!r} in {self.path}") from exc


def _metadata(data: dict, path: str) -> Metadata:
    unknown = set(data) - _ALLOWED_METADATA
    if unknown:
        raise CompositionError(f"unknown document fields in {path}: {sorted(unknown)}")
    if type(data.get("format_version")) is not int:
        raise CompositionError(f"invalid format version in {path}")
    if data["format_version"] != FORMAT_VERSION:
        raise CompositionError(
            f"unsupported format version {data['format_version']} in {path}; "
            f"single-file documents require {FORMAT_VERSION}"
        )
    identity = _identifier(data.get("id"), field="document identity")
    kind = data.get("kind", "procedure")
    if kind not in KINDS:
        raise CompositionError(f"unknown document kind in {path}: {kind!r}")
    for field in ("title", "description"):
        if not isinstance(data.get(field), str) or not data[field]:
            raise CompositionError(f"missing {field} in {path}")
    if ("argument_name" in data) != ("argument_description" in data):
        raise CompositionError(f"incomplete argument metadata in {path}")
    for field in ("argument_name", "argument_description"):
        if field in data and not isinstance(data[field], str):
            raise CompositionError(f"invalid argument metadata in {path}")

    shared: tuple[str, ...] = ()
    backend_calls: tuple[tuple[str, tuple[str, ...]], ...] = ()
    if "calls" in data:
        raw = data["calls"]
        if isinstance(raw, list):
            shared = tuple(_identifier(call, field="call") for call in raw)
        elif isinstance(raw, dict):
            if set(raw) != set(BACKENDS):
                raise CompositionError(f"backend-scoped calls in {path} must name both {BACKENDS}")
            if any(not isinstance(raw[backend], list) for backend in BACKENDS):
                raise CompositionError(f"backend-scoped calls in {path} must be lists")
            backend_calls = tuple(
                (backend, tuple(_identifier(call, field="call") for call in raw[backend]))
                for backend in BACKENDS
            )
        else:
            raise CompositionError(f"invalid calls in {path}")
    return Metadata(
        FORMAT_VERSION,
        identity,
        kind,
        data["title"],
        data["description"],
        data.get("argument_name"),
        data.get("argument_description"),
        shared,
        backend_calls,
    )


def _attributes(text: str, path: str, line: int) -> dict[str, str]:
    if text and not text[0].isspace():
        text = " " + text
    attributes: dict[str, str] = {}
    position = 0
    while position < len(text):
        match = _ATTRIBUTE.match(text, position)
        if not match:
            if text[position:].strip():
                raise CompositionError(f"{path}:{line}: malformed directive attributes")
            break
        key, value = match.groups()
        if key in attributes:
            raise CompositionError(f"{path}:{line}: duplicate directive attribute {key!r}")
        attributes[key] = value
        position = match.end()
    return attributes


def _directive(content: str):
    """Match a directive line."""
    return _DIRECTIVE.fullmatch(content.strip())


def _event(part, path: str, line_number: int):
    action = part.group(1)
    rest = (part.group(2) or "").strip()
    named = _KIND.fullmatch(rest)
    if not named:
        raise CompositionError(f"{path}:{line_number}: directive must name its kind")
    kind = named.group(1)
    attributes = _attributes(named.group(2) or "", path, line_number)
    if action == "end" and attributes:
        raise CompositionError(f"{path}:{line_number}: @end {kind} takes no attributes")
    return ("directive", action, kind, attributes, line_number)


def _events(text: str, path: str):
    """Yield directive events and raw lines.

    A directive inside fenced code stays literal, so a printed example never expands and
    is never mistaken for a reference. An unterminated fence is an error.
    """
    fence: tuple[str, int] | None = None
    for line_number, line in enumerate(text.splitlines(keepends=True), 1):
        content = line.rstrip("\r\n")
        if fence is not None:
            yield ("raw", line)
            closing = re.fullmatch(
                r" {0,3}(" + re.escape(fence[0]) + r"{" + str(fence[1]) + r",})[ \t]*",
                content,
            )
            if closing:
                fence = None
            continue
        opening = _FENCE.fullmatch(content)
        if opening:
            marker = opening.group(1)
            fence = (marker[0], len(marker))
            yield ("raw", line)
            continue
        directive = _directive(content)
        if not directive:
            yield ("raw", line)
            continue
        yield _event(directive, path, line_number)
    if fence is not None:
        raise CompositionError(f"{path}: unterminated fenced code block")


def _applicability(value: str, path: str, line: int) -> tuple[str, ...]:
    parts = [part.strip() for part in value.split(",")]
    if not parts or any(not part for part in parts):
        raise CompositionError(f"{path}:{line}: invalid backend applicability {value!r}")
    if len(set(parts)) != len(parts) or set(parts) - set(BACKENDS):
        raise CompositionError(f"{path}:{line}: invalid backend applicability {value!r}")
    return tuple(backend for backend in BACKENDS if backend in parts)


def _reference(kind: str, attributes: dict[str, str], path: str, line: int) -> Reference:
    expected = {
        "component": {"id", "ref"},
        "storage": {"id", "ref", "target"},
    }[kind]
    required = expected
    allowed = expected | {"applies_to"}
    if set(attributes) - allowed or not required <= set(attributes):
        raise CompositionError(f"{path}:{line}: {kind} directive requires {sorted(required)}")
    identity = _identifier(attributes["id"], field="reference identity")
    ref = _path(attributes["ref"], field="reference path")
    if kind == "component" and ("{" in ref or "}" in ref):
        raise CompositionError(f"{path}:{line}: component reference may not use braces")
    target = (
        _identifier(attributes["target"], field="region identity") if kind == "storage" else None
    )
    applies_to = (
        _applicability(attributes["applies_to"], path, line)
        if "applies_to" in attributes
        else BACKENDS
    )
    return Reference(kind, identity, ref, target, applies_to)


def _parse_document_body(text: str, path: str) -> tuple[Node, ...]:
    nodes: list[Node] = []
    prose: list[str] = []
    open_kind: str | None = None
    open_attributes: dict[str, str] = {}
    open_line = 0
    interior: list[str] = []
    identities: set[str] = set()

    def flush() -> None:
        if prose:
            nodes.append(Prose("".join(prose)))
            prose.clear()

    def finish(reference: Reference) -> None:
        if reference.id in identities:
            raise CompositionError(
                f"{path}:{open_line}: duplicate reference identity {reference.id!r}"
            )
        identities.add(reference.id)
        nodes.append(reference)

    for event in _events(text, path):
        if event[0] == "raw":
            (line,) = event[1:]
            if open_kind is None:
                prose.append(line)
            else:
                interior.append(line)
            continue
        _, action, kind, attributes, line = event
        if action == "start":
            if open_kind is not None:
                raise CompositionError(f"{path}:{line}: nested directives are not supported")
            if kind not in REFERENCE_KINDS:
                raise CompositionError(
                    f"{path}:{line}: {kind!r} directives belong in a storage-backend document"
                )
            reference = _reference(kind, attributes, path, line)
            flush()
            open_kind, open_attributes, open_line = kind, attributes, line
            interior = []
            continue
        if open_kind is None:
            raise CompositionError(f"{path}:{line}: unmatched @end {kind}")
        if kind != open_kind:
            raise CompositionError(f"{path}:{line}: @end {kind} does not close @start {open_kind}")
        reference = _reference(open_kind, open_attributes, path, open_line)
        if "".join(interior).strip():
            raise CompositionError(
                f"{path}:{open_line}: reference {reference.id!r} must be empty; "
                "composed content is never cached in the source"
            )
        flush()
        finish(reference)
        open_kind, open_attributes = None, {}
        interior = []
    if open_kind is not None:
        raise CompositionError(f"{path}:{open_line}: unclosed @start {open_kind}")
    flush()
    return tuple(nodes)


def parse_document(path: str, raw: bytes) -> Document:
    """Parse one version-2 Markdown document, preserving its body bytes exactly."""
    path = _path(path)
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise CompositionError(f"document is not UTF-8: {path}") from exc
    if text.startswith("\ufeff"):
        raise CompositionError(f"document must not start with a byte-order mark: {path}")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "+++":
        raise CompositionError(f"missing +++ metadata header: {path}")
    closing = next(
        (index for index in range(1, len(lines)) if lines[index].rstrip("\r\n") == "+++"),
        None,
    )
    if closing is None:
        raise CompositionError(f"unterminated metadata header: {path}")
    header = "".join(lines[1:closing])
    try:
        data = tomllib.loads(header.replace("\r\n", "\n").replace("\r", "\n"))
    except tomllib.TOMLDecodeError as exc:
        raise CompositionError(f"invalid metadata in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise CompositionError(f"invalid metadata in {path}")
    metadata = _metadata(data, path)
    body = "".join(lines[closing + 1 :])
    return Document(
        path,
        raw,
        hashlib.sha256(raw).hexdigest(),
        metadata,
        body,
        _parse_document_body(body, path),
    )


def _trim_one_ending(text: str) -> str:
    if text.endswith("\r\n"):
        return text[:-2]
    if text.endswith(("\n", "\r")):
        return text[:-1]
    return text


def _region_attributes(attributes: dict[str, str], path: str, line: int) -> tuple[str, str | None]:
    if set(attributes) not in ({"id"}, {"id", "ending"}):
        raise CompositionError(f"{path}:{line}: region directive requires ['id']")
    identity = _identifier(attributes["id"], field="region identity")
    ending = attributes.get("ending")
    if ending is not None and ending != "none":
        raise CompositionError(f"{path}:{line}: region ending must be 'none'")
    return identity, ending


def parse_backend_document(path: str, raw: bytes) -> BackendDocument:
    """Extract named regions from a storage-backend document.

    Only ``region`` directives are legal here. Legacy heading-based backend sections and
    prose are untouched; this parser adds regions beside them rather than replacing them.
    """
    path = _path(path)
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise CompositionError(f"backend document is not UTF-8: {path}") from exc
    lines = text.splitlines(keepends=True)
    if lines and lines[0].startswith("+++"):
        raise CompositionError(f"backend document must not carry document metadata: {path}")
    regions: list[tuple[str, str]] = []
    identities: set[str] = set()
    open_id: str | None = None
    open_ending: str | None = None
    open_line = 0
    interior: list[str] = []

    for event in _events(text, path):
        if event[0] == "raw":
            (line,) = event[1:]
            if open_id is not None:
                interior.append(line)
            continue
        _, action, kind, attributes, line = event
        if kind != REGION_KIND:
            raise CompositionError(
                f"{path}:{line}: only region directives are allowed in a backend document"
            )
        if action == "start":
            if open_id is not None:
                raise CompositionError(f"{path}:{line}: nested regions are not supported")
            identity, ending = _region_attributes(attributes, path, line)
            if identity in identities:
                raise CompositionError(f"{path}:{line}: duplicate region identity {identity!r}")
            identities.add(identity)
            open_id, open_ending, open_line = identity, ending, line
            interior = []
            continue
        if open_id is None:
            raise CompositionError(f"{path}:{line}: unmatched @end region")
        body = "".join(interior)
        if open_ending == "none":
            body = _trim_one_ending(body)
        regions.append((open_id, body))
        open_id, open_ending, interior = None, None, []
    if open_id is not None:
        raise CompositionError(f"{path}:{open_line}: unclosed @start region {open_id}")
    return BackendDocument(path, raw, hashlib.sha256(raw).hexdigest(), tuple(regions))


def expand_regions(text: str, path: str = "<inline>") -> str:
    """Expand region blocks in a section body, dropping only directive scaffolding.

    Used by the legacy seam adapter so a heading-based backend section that now contains
    named regions delivers the same prose it did before, never the directive lines.
    """
    output: list[str] = []
    open_id: str | None = None
    open_ending: str | None = None
    open_line = 0
    interior: list[str] = []

    for event in _events(text, path):
        if event[0] == "raw":
            (line,) = event[1:]
            if open_id is None:
                output.append(line)
            else:
                interior.append(line)
            continue
        _, action, kind, attributes, line = event
        if kind != REGION_KIND:
            raise CompositionError(f"{path}:{line}: only region directives are supported here")
        if action == "start":
            if open_id is not None:
                raise CompositionError(f"{path}:{line}: nested regions are not supported")
            identity, ending = _region_attributes(attributes, path, line)
            open_id, open_ending, open_line = identity, ending, line
            interior = []
            continue
        if open_id is None:
            raise CompositionError(f"{path}:{line}: unmatched @end region")
        body = "".join(interior)
        if open_ending == "none":
            body = _trim_one_ending(body)
        output.append(body.rstrip("\n"))
        output.append("\n")
        open_id, open_ending, interior = None, None, []
    if open_id is not None:
        raise CompositionError(f"{path}:{open_line}: unclosed @start region {open_id}")
    return "".join(output)


def backend_path(reference: str, backend: str) -> str:
    """Resolve the single ``{backend}`` substitution and enforce the backend location."""
    if backend not in BACKENDS:
        raise CompositionError(f"unknown backend: {backend}")
    if "{" in reference and reference.count("{backend}") == 0:
        raise CompositionError(f"unsupported reference substitution: {reference!r}")
    if reference.count("{backend}") != 1:
        raise CompositionError(
            f"storage reference must use {{backend}} exactly once: {reference!r}"
        )
    resolved = reference.replace("{backend}", backend)
    if "{" in resolved or "}" in resolved:
        raise CompositionError(f"unsupported reference substitution: {reference!r}")
    resolved = _path(resolved)
    expected = f"procedures/memory/storage-backends/{backend}.md"
    if resolved != expected:
        raise CompositionError(f"storage reference must resolve to {expected!r}, not {resolved!r}")
    return resolved
