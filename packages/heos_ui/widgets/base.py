from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Widget:
    """Base class for all HEOS UI widgets."""

    id: str
    title: str

    def render(self) -> str:
        """Return a text representation of the widget."""
        return self.title