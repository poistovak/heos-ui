from __future__ import annotations

from .clock import FrameClock
from .pipeline import RenderPipeline
from .profiler import RenderProfiler


class RenderLoop:
    """Coordinates one complete render cycle."""

    def __init__(
        self,
        pipeline: RenderPipeline | None = None,
        profiler: RenderProfiler | None = None,
        clock: FrameClock | None = None,
    ) -> None:
        self._pipeline = pipeline or RenderPipeline()
        self._profiler = profiler or RenderProfiler()
        self._clock = clock or FrameClock()

    @property
    def frame(self) -> int:
        return self._clock.frame

    @property
    def profiler(self) -> RenderProfiler:
        return self._profiler

    def tick(self) -> int:
        self._clock.tick()

        self._profiler.begin_frame()

        try:
            rendered = self._pipeline.render_pending()
        finally:
            self._profiler.end_frame()

        return rendered