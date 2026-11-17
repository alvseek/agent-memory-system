"""Pure, versioned procedure composition; source providers supply data, never code."""

from .composer import (
    Catalog,
    Composition,
    CompositionError,
    FileSource,
    MemorySource,
    Section,
    SourceProvider,
    compose,
    dependents,
    validate_catalog,
)

__version__ = "0.1.0"
__all__ = [
    "Catalog", "Composition", "CompositionError", "FileSource", "MemorySource",
    "Section", "SourceProvider", "compose", "dependents", "validate_catalog",
]
