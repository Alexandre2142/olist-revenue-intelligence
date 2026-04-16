"""General-purpose helpers."""

from __future__ import annotations

from pathlib import Path


def relative_to_root(path: Path, root: Path) -> str:
    """Return a display-friendly relative path when possible."""

    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)

