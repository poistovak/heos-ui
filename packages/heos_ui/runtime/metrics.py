from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RenderMetrics:
    """Aggregated render metrics."""

    frames: int
    rendered_widgets: int
    skipped_widgets: int

    @property
    def total_widgets(self) -> int:
        return self.rendered_widgets + self.skipped_widgets

    @property
    def render_ratio(self) -> float:
        if self.total_widgets == 0:
            return 0.0

        return self.rendered_widgets / self.total_widgets