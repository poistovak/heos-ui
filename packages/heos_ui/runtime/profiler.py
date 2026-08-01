from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter


@dataclass(frozen=True, slots=True)
class RenderProfilerSnapshot:
    """Immutable render profiler snapshot."""

    frame_count: int
    total_frame_time: float
    average_frame_time: float
    last_frame_time: float


class RenderProfiler:
    """Measures render performance."""

    def __init__(self) -> None:
        self._frame_count = 0
        self._total_time = 0.0
        self._last_time = 0.0
        self._started = 0.0

    @property
    def snapshot(self) -> RenderProfilerSnapshot:
        average = (
            self._total_time / self._frame_count
            if self._frame_count
            else 0.0
        )

        return RenderProfilerSnapshot(
            frame_count=self._frame_count,
            total_frame_time=self._total_time,
            average_frame_time=average,
            last_frame_time=self._last_time,
        )

    def begin_frame(self) -> None:
        self._started = perf_counter()

    def end_frame(self) -> float:
        elapsed = perf_counter() - self._started

        self._last_time = elapsed
        self._total_time += elapsed
        self._frame_count += 1

        return elapsed

    def reset(self) -> None:
        self._frame_count = 0
        self._total_time = 0.0
        self._last_time = 0.0
        self._started = 0.0