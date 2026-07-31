from __future__ import annotations

from dataclasses import dataclass

from .base import Widget


@dataclass(slots=True)
class LabelWidget(Widget):
    """Simple text label."""

    text: str

    def render(self) -> str:
        return self.text