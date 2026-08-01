from __future__ import annotations

from heos_ui.widgets.base import Widget

from .frame import FrameResult
from .scheduler import RenderScheduler


class FrameScheduler:
    """Coordinates widget invalidation and frame rendering."""

    def __init__(self) -> None:
        self._scheduler = RenderScheduler()
        self._frame_number = 0

    @property
    def frame_number(self) -> int:
        """Return the number of completed frames."""

        return self._frame_number

    @property
    def pending_count(self) -> int:
        """Return the number of widgets waiting for rendering."""

        return self._scheduler.pending_count

    def invalidate(self, widget: Widget) -> bool:
        """Invalidate and schedule a widget.

        Returns:
            True when the widget became dirty, otherwise False.
        """

        became_dirty = widget.invalidate()
        self._scheduler.invalidate(widget)
        return became_dirty

    def render_frame(self) -> FrameResult:
        """Render all currently scheduled widgets as one frame."""

        pending_widgets = self._scheduler.pending_count
        rendered_widgets = self._scheduler.flush()
        self._frame_number += 1

        return FrameResult(
            frame_number=self._frame_number,
            pending_widgets=pending_widgets,
            rendered_widgets=rendered_widgets,
        )
