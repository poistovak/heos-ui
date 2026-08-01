from __future__ import annotations

from heos_ui.widgets.base import Widget

from .frame import FrameResult
from .pipeline import RenderPipeline


class FrameScheduler:
    """Coordinates invalidation and frame rendering."""

    def __init__(self, pipeline: RenderPipeline | None = None) -> None:
        self._pipeline = pipeline or RenderPipeline()
        self._frame_number = 0

    @property
    def frame_number(self) -> int:
        """Return the number of completed frames."""

        return self._frame_number

    @property
    def pending_count(self) -> int:
        """Return the number of widgets awaiting rendering."""

        return self._pipeline.pending_count

    def invalidate(self, widget: Widget) -> bool:
        """Invalidate and schedule a widget."""

        return self._pipeline.invalidate(widget)

    def render_frame(self) -> FrameResult:
        """Render all pending widgets as one frame."""

        pending_widgets = self._pipeline.pending_count
        rendered_widgets = self._pipeline.render_pending()
        self._frame_number += 1

        return FrameResult(
            frame_number=self._frame_number,
            pending_widgets=pending_widgets,
            rendered_widgets=rendered_widgets,
        )
