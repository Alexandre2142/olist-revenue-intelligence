"""API utility helpers."""

from __future__ import annotations


def normalize_state_code(value: str) -> str:
    """Normalize Brazilian state codes for API payloads."""

    return value.strip().upper()

