from __future__ import annotations

from heos_ui.widgets.base import Widget


class RenderQueue:
    """FIFO queue of unique widgets awaiting rendering."""

    def __init__(self) -> None:
        self._widgets: dict[int, Widget] = {}

    @property
    def pending_count(self) -> int:
        return len(self._widgets)

    @property
    def is_empty(self) -> bool:
        return not self._widgets

    def enqueue(self, widget: Widget) -> None:
        self._widgets.setdefault(id(widget), widget)

    def dequeue_all(self) -> tuple[Widget, ...]:
        widgets = tuple(self._widgets.values())
        self._widgets.clear()
        return widgets

    def clear(self) -> None:
        self._widgets.clear()
