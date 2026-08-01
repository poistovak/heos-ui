from __future__ import annotations

from heos_ui.widgets.base import Widget


class RenderScheduler:
    """Schedules dirty widgets for rendering."""

    def __init__(self) -> None:
        self._dirty_widgets: dict[int, Widget] = {}

    @property
    def pending_count(self) -> int:
        return len(self._dirty_widgets)

    def invalidate(self, widget: Widget) -> None:
        self._dirty_widgets[id(widget)] = widget

    def flush(self) -> int:
        rendered = 0
        pending = tuple(self._dirty_widgets.values())
        self._dirty_widgets.clear()

        for widget in pending:
            if widget.render_if_dirty():
                rendered += 1

        return rendered