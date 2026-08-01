from __future__ import annotations

from heos_ui.widgets.base import Widget


class RenderEngine:
    """Executes widget rendering."""

    def __init__(self) -> None:
        self._render_count = 0

    @property
    def render_count(self) -> int:
        """Return the total number of rendered widgets."""

        return self._render_count

    def render(self, widget: Widget) -> bool:
        """Render a single widget if required."""

        rendered = widget.render_if_dirty()

        if rendered:
            self._render_count += 1

        return rendered

    def render_all(
        self,
        widgets: tuple[Widget, ...],
    ) -> int:
        """Render all widgets in order."""

        rendered = 0

        for widget in widgets:
            if self.render(widget):
                rendered += 1

        return rendered

    def reset_statistics(self) -> None:
        """Reset render statistics."""

        self._render_count = 0