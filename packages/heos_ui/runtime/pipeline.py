from __future__ import annotations

from heos_ui.widgets.base import Widget

from .engine import RenderEngine
from .frame_batch import FrameBatch


class RenderPipeline:
    """Collects invalidations and renders stable widget frames."""

    def __init__(self, engine: RenderEngine | None = None) -> None:
        self._batch = FrameBatch()
        self._engine = engine or RenderEngine()

    @property
    def pending_count(self) -> int:
        """Return widgets waiting for the next frame."""

        return self._batch.pending_count

    @property
    def frame_id(self) -> int:
        """Return the number of frames started by the pipeline."""

        return self._batch.frame_id

    @property
    def render_count(self) -> int:
        """Return the total number of rendered widgets."""

        return self._engine.render_count

    def invalidate(self, widget: Widget) -> bool:
        """Invalidate and schedule a widget."""

        became_dirty = widget.invalidate()
        self._batch.enqueue(widget)
        return became_dirty

    def render_pending(self) -> int:
        """Render one stable frame of pending widgets."""

        widgets = self._batch.begin()

        try:
            return self._engine.render_all(widgets)
        finally:
            self._batch.end()

    def clear(self) -> None:
        """Discard widgets waiting for a future frame."""

        self._batch.clear()