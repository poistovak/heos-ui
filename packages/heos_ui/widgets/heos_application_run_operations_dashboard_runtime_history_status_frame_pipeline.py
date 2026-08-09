from __future__ import annotations

import importlib
from dataclasses import dataclass

canvas_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_canvas_renderer"
)
renderer_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_renderer"
)
widget_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_widget"
)

CanvasFrame = (
    canvas_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasFrame
)
CanvasRenderer = (
    canvas_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasRenderer
)
Renderer = (
    renderer_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderer
)
RenderScene = (
    renderer_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderScene
)
StatusView = (
    widget_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusFrameResult:
    scene: RenderScene
    frame: CanvasFrame


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusFramePipeline:
    renderer: Renderer
    canvas_renderer: CanvasRenderer

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusFramePipeline:
        return cls(
            renderer=Renderer(),
            canvas_renderer=CanvasRenderer(),
        )

    def render(
        self,
        view: StatusView,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusFrameResult:
        scene = self.renderer.render(view)
        frame = self.canvas_renderer.render(scene)

        return (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusFrameResult(
                scene=scene,
                frame=frame,
            )
        )
