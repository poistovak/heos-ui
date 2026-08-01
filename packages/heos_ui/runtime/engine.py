from __future__ import annotations

from heos_ui.widgets.base import Widget

from .statistics import RenderStatistics


class RenderEngine:
    """Executes widget rendering and records statistics."""

    def __init__(self) -> None:
        self._attempted = 0
        self._rendered = 0
        self._skipped = 0
        self._batches = 0

    @property
    def render_count(self) -> int:
        """Return the total number of rendered widgets."""

        return self._rendered

    @property
    def statistics(self) -> RenderStatistics:
        """Return an immutable statistics snapshot."""

        return RenderStatistics(
            attempted=self._attempted,
            rendered=self._rendered,
            skipped=self._skipped,
            batches=self._batches,
        )

    def render(self, widget: Widget) -> bool:
        """Render a single widget if required."""

        self._attempted += 1
        rendered = widget.render_if_dirty()

        if rendered:
            self._rendered += 1
        else:
            self._skipped += 1

        return rendered

    def render_all(
        self,
        widgets: tuple[Widget, ...],
    ) -> int:
        """Render all widgets in order as one batch."""

        self._batches += 1
        rendered = 0

        for widget in widgets:
            if self.render(widget):
                rendered += 1

        return rendered

    def reset_statistics(self) -> None:
        """Reset all render statistics."""

        self._attempted = 0
        self._rendered = 0
        self._skipped = 0
        self._batches = 0
