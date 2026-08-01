from __future__ import annotations

from heos_ui.widgets.base import Widget

from .frame_batch import FrameBatch


class RenderPipeline:
    """Collects invalidations and renders stable widget frames."""

    def __init__(self) -> None:
        self._batch = FrameBatch()

    @property
    def pending_count(self) -> int:
        """Return widgets waiting for the next frame."""

        return self._batch.pending_count

    @property
    def frame_id(self) -> int:
        """Return the number of frames started by the pipeline."""

        return self._batch.frame_id

    def invalidate(self, widget: Widget) -> bool:
        """Invalidate and schedule a widget."""

        became_dirty = widget.invalidate()
        self._batch.enqueue(widget)
        return became_dirty

    def render_pending(self) -> int:
        """Render one stable frame of pending widgets."""

        widgets = self._batch.begin()
        rendered = 0

        try:
            for widget in widgets:
                if widget.render_if_dirty():
                    rendered += 1
        finally:
            self._batch.end()

        return rendered

    def clear(self) -> None:
        """Discard widgets waiting for a future frame."""

        self._batch.clear()
