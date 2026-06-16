"""Reusable components for the blockchain pipeline demo."""

from importlib import import_module
from typing import Any

__all__ = [
    "TRANSACTION_SCHEMA",
    "build_source_transactions",
    "validate_source_transactions",
]

_LAZY_EXPORTS = {
    "TRANSACTION_SCHEMA": ("blockchain_pipeline.schemas", "TRANSACTION_SCHEMA"),
    "build_source_transactions": (
        "blockchain_pipeline.source_data",
        "build_source_transactions",
    ),
    "validate_source_transactions": (
        "blockchain_pipeline.source_data",
        "validate_source_transactions",
    ),
}


def __getattr__(name: str) -> Any:
    """Load PySpark-dependent exports only when they are requested."""
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attribute_name = _LAZY_EXPORTS[name]
    return getattr(import_module(module_name), attribute_name)
