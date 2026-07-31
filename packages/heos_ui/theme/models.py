from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Theme:
    """Represents a UI theme."""

    name: str
    primary: str
    secondary: str
    success: str
    warning: str
    danger: str