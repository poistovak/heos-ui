from __future__ import annotations

from dataclasses import dataclass

from . import (
    heos_application_run_operations_dashboard_runtime_history_frame_pipeline as frame_pipeline,
)
from . import (
    heos_application_run_operations_dashboard_runtime_history_health_widget as health_widget,
)

FramePipeline = (
    frame_pipeline.HEOSApplicationRunOperationsDashboardRuntimeHistoryFramePipeline
)
FrameResult = (
    frame_pipeline.HEOSApplicationRunOperationsDashboardRuntimeHistoryFrameResult
)
HealthView = (
    health_widget.HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryLiveRenderer:
    pipeline: FramePipeline
    _latest_result: FrameResult | None = None
    _render_count: int = 0

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryLiveRenderer:
        return cls(
            pipeline=FramePipeline.create(),
        )

    @property
    def latest_result(
        self,
    ) -> FrameResult | None:
        return self._latest_result

    @property
    def latest_frame(self):
        if self._latest_result is None:
            return None

        return self._latest_result.frame

    @property
    def render_count(self) -> int:
        return self._render_count

    @property
    def has_frame(self) -> bool:
        return self.latest_frame is not None

    def render(
        self,
        view: HealthView,
    ) -> FrameResult:
        result = self.pipeline.render(view)

        self._latest_result = result
        self._render_count += 1

        return result

    def clear(self) -> None:
        self._latest_result = None
