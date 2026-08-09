from __future__ import annotations

import importlib
from dataclasses import dataclass

pipeline_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_frame_pipeline"
)
widget_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_widget"
)

FramePipeline = (
    pipeline_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusFramePipeline
)
FrameResult = (
    pipeline_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusFrameResult
)
StatusView = (
    widget_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusLiveRenderer:
    pipeline: FramePipeline
    _latest_result: FrameResult | None = None
    _render_count: int = 0

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusLiveRenderer:
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
        view: StatusView,
    ) -> FrameResult:
        result = self.pipeline.render(view)

        self._latest_result = result
        self._render_count += 1

        return result

    def clear(self) -> None:
        self._latest_result = None
