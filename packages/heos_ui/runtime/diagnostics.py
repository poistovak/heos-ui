from __future__ import annotations

from dataclasses import dataclass

from .metrics import RenderMetrics
from .profiler import RenderProfilerSnapshot
from .statistics import RenderStatistics


@dataclass(frozen=True, slots=True)
class RenderDiagnostics:
    """Complete render runtime diagnostics."""

    statistics: RenderStatistics
    metrics: RenderMetrics
    profiler: RenderProfilerSnapshot

    @property
    def rendered_frames(self) -> int:
        return self.metrics.frames

    @property
    def total_widgets(self) -> int:
        return self.metrics.total_widgets