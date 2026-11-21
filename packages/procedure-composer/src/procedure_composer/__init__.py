"""Pure, versioned procedure composition; source providers supply data, never code."""

from .composer import (
    BACKENDS,
    FORMAT_VERSION,
    Catalog,
    Composition,
    CompositionError,
    Document,
    DocumentEdit,
    FileSource,
    MemorySource,
    Reference,
    SourceProvider,
    Span,
    compose,
    dependents,
    validate_catalog,
)
from .document import expand_regions

__version__ = "0.2.0"
__all__ = [
    "BACKENDS",
    "FORMAT_VERSION",
    "Catalog",
    "Composition",
    "CompositionError",
    "Document",
    "DocumentEdit",
    "FileSource",
    "MemorySource",
    "Reference",
    "Span",
    "SourceProvider",
    "compose",
    "dependents",
    "expand_regions",
    "validate_catalog",
]
