from __future__ import annotations

from dataclasses import dataclass, field

from heos_ui.widgets import Widget


@dataclass(slots=True)
class Layout:
    """Base class for HEOS UI layouts."""

    children: list[Widget] = field(default_factory=list)

    def add(self, widget: Widget) -> None:
        self.children.append(widget)

    def __iter__(self):
        return iter(self.children)

    def __len__(self) -> int:
        return len(self.children)