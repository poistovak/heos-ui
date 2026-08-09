from __future__ import annotations

from dataclasses import dataclass

from . import (
    heos_application_run_operations_dashboard_runtime_history_canvas_renderer as canvas_renderer,
)
from . import (
    heos_application_run_operations_dashboard_runtime_history_health_renderer as health_renderer,
)
from . import (
    heos_application_run_operations_dashboard_runtime_history_health_widget as health_widget,
)

HealthView = (
    health_widget.HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView
)
RenderScene = (
    health_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderScene
)
CanvasFrame = (
    canvas_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasFrame
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryFrameResult:
    scene: RenderScene
    frame: CanvasFrame


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryFramePipeline:
    health_renderer: (
        health_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthRenderer
    )
    canvas_renderer: (
        canvas_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasRenderer
    )

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryFramePipeline:
        return cls(
            health_renderer=(
                health_renderer.
                HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthRenderer()
            ),
            canvas_renderer=(
                canvas_renderer.
                HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasRenderer()
            ),
        )

    def render(
        self,
        view: HealthView,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryFrameResult:
        scene = self.health_renderer.render(view)
        frame = self.canvas_renderer.render(scene)

        return HEOSApplicationRunOperationsDashboardRuntimeHistoryFrameResult(
            scene=scene,
            frame=frame,
        )
