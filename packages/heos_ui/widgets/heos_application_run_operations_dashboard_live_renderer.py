from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_dashboard_canvas_renderer import (
    HEOSApplicationRunOperationsDashboardCanvasFrame,
)
from .heos_application_run_operations_dashboard_frame_pipeline import (
    HEOSApplicationRunOperationsDashboardFramePipeline,
    HEOSApplicationRunOperationsDashboardFrameResult,
)
from .heos_application_run_operations_dashboard_health_widget import (
    HEOSApplicationRunOperationsDashboardHealthView,
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardLiveRenderer:
    pipeline: HEOSApplicationRunOperationsDashboardFramePipeline
    _latest: HEOSApplicationRunOperationsDashboardFrameResult | None = None
    _render_count: int = 0

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardLiveRenderer:
        return cls(
            pipeline=(
                HEOSApplicationRunOperationsDashboardFramePipeline.create()
            )
        )

    @property
    def latest(
        self,
    ) -> HEOSApplicationRunOperationsDashboardFrameResult | None:
        return self._latest

    @property
    def latest_frame(
        self,
    ) -> HEOSApplicationRunOperationsDashboardCanvasFrame | None:
        if self._latest is None:
            return None

        return self._latest.frame

    @property
    def render_count(self) -> int:
        return self._render_count

    @property
    def has_frame(self) -> bool:
        return self._latest is not None

    def render(
        self,
        view: HEOSApplicationRunOperationsDashboardHealthView,
    ) -> HEOSApplicationRunOperationsDashboardCanvasFrame:
        result = self.pipeline.render(view)

        self._latest = result
        self._render_count += 1

        return result.frame

    def clear(self) -> None:
        self._latest = None
