from __future__ import annotations

from heos_ui.widgets.base import Widget

from .clock import FrameClock
from .events import RenderEvent, RenderEvents
from .loop import RenderLoop
from .pipeline import RenderPipeline
from .profiler import RenderProfiler


class RenderRuntime:
    """High-level service coordinating the render runtime."""

    def __init__(
        self,
        pipeline: RenderPipeline | None = None,
        profiler: RenderProfiler | None = None,
        clock: FrameClock | None = None,
        events: RenderEvents | None = None,
    ) -> None:
        self._pipeline = pipeline or RenderPipeline()
        self._events = events or RenderEvents()
        self._loop = RenderLoop(
            pipeline=self._pipeline,
            profiler=profiler,
            clock=clock,
        )

    @property
    def frame(self) -> int:
        """Return the current frame number."""

        return self._loop.frame

    @property
    def pending_count(self) -> int:
        """Return the number of widgets waiting for rendering."""

        return self._pipeline.pending_count

    @property
    def profiler(self) -> RenderProfiler:
        """Return the runtime profiler."""

        return self._loop.profiler

    @property
    def events(self) -> RenderEvents:
        """Return the render event dispatcher."""

        return self._events

    def invalidate(self, widget: Widget) -> bool:
        """Invalidate and schedule a widget."""

        return self._pipeline.invalidate(widget)

    def tick(self) -> RenderEvent:
        """Execute one complete render frame."""

        rendered = self._loop.tick()
        event = RenderEvent(
            frame=self.frame,
            rendered=rendered,
        )
        self._events.emit(event)
        return event
