from __future__ import annotations

from dataclasses import dataclass

from .base import Widget


@dataclass(slots=True, kw_only=True)
class ProgressWidget(Widget):
    """Widget displaying progress from zero to one hundred percent."""

    value: float

    def __post_init__(self) -> None:
        if not 0 <= self.value <= 100:
            raise ValueError("Progress value must be between 0 and 100.")

    def render(self) -> str:
        """Return the formatted progress value."""

        return f"{self.title}: {self.value:g}%"