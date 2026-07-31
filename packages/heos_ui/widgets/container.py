from __future__ import annotations

from dataclasses import dataclass, field

from .base import Widget


@dataclass(slots=True)
class WidgetContainer:
    """Container for HEOS UI widgets."""

    widgets: list[Widget] = field(default_factory=list)

    def add(self, widget: Widget) -> None:
        self.widgets.append(widget)

    def __iter__(self):
        return iter(self.widgets)

    def __len__(self) -> int:
        return len(self.widgets)