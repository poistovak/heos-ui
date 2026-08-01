from __future__ import annotations

from heos_ui.widgets.base import Widget

from .render_queue import RenderQueue


class RenderPipeline:
    """Collects invalidations and renders queued widgets."""

    def __init__(self) -> None:
        self._queue = RenderQueue()

    @property
    def pending_count(self) -> int:
        """Return the number of widgets waiting for rendering."""

        return self._queue.pending_count

    def invalidate(self, widget: Widget) -> bool:
        """Invalidate and enqueue a widget."""

        became_dirty = widget.invalidate()
        self._queue.enqueue(widget)
        return became_dirty

    def render_pending(self) -> int:
        """Render all currently queued dirty widgets."""

        rendered = 0

        for widget in self._queue.dequeue_all():
            if widget.render_if_dirty():
                rendered += 1

        return rendered

    def clear(self) -> None:
        """Discard all pending widgets."""

        self._queue.clear()
