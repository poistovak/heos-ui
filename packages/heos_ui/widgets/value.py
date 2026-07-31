from __future__ import annotations

from dataclasses import dataclass

from .base import Widget


@dataclass(slots=True)
class ValueWidget(Widget):
    """Displays a value with its unit."""

    value: float
    unit: str

    def render(self) -> str:
        return f"{self.value} {self.unit}"