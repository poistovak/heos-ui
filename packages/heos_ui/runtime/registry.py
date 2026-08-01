from __future__ import annotations

from heos_ui.widgets.base import Widget


class RenderRegistry:
    """Registry of renderable widgets."""

    def __init__(self) -> None:
        self._widgets: dict[str, Widget] = {}

    def register(self, widget: Widget) -> None:
        self._widgets[widget.id] = widget

    def unregister(self, widget_id: str) -> None:
        self._widgets.pop(widget_id, None)

    def get(self, widget_id: str) -> Widget | None:
        return self._widgets.get(widget_id)

    def clear(self) -> None:
        self._widgets.clear()

    @property
    def count(self) -> int:
        return len(self._widgets)

    def __iter__(self):
        return iter(self._widgets.values())