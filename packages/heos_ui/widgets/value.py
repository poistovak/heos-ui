from __future__ import annotations

from dataclasses import dataclass

from .base import Widget


@dataclass(slots=True, kw_only=True)
class ValueWidget(Widget):
    """Widget displaying a value with an optional unit."""

    value: object
    unit: str = ""

    def render(self) -> str:
        """Return the formatted value."""

        if not self.unit:
            return str(self.value)

        return f"{self.value} {self.unit}"