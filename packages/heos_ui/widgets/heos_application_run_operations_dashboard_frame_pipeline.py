from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_dashboard_canvas_renderer import (
    HEOSApplicationRunOperationsDashboardCanvasFrame,
    HEOSApplicationRunOperationsDashboardCanvasRenderer,
)
from .heos_application_run_operations_dashboard_health_renderer import (
    HEOSApplicationRunOperationsDashboardHealthRenderer,
    HEOSApplicationRunOperationsDashboardRenderScene,
)
from .heos_application_run_operations_dashboard_health_widget import (
    HEOSApplicationRunOperationsDashboardHealthView,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardFrameResult:
    scene: HEOSApplicationRunOperationsDashboardRenderScene
    frame: HEOSApplicationRunOperationsDashboardCanvasFrame

    @property
    def command_count(self) -> int:
        return self.frame.command_count


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardFramePipeline:
    renderer: HEOSApplicationRunOperationsDashboardHealthRenderer
    canvas_renderer: HEOSApplicationRunOperationsDashboardCanvasRenderer

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardFramePipeline:
        return cls(
            renderer=HEOSApplicationRunOperationsDashboardHealthRenderer(),
            canvas_renderer=(
                HEOSApplicationRunOperationsDashboardCanvasRenderer()
            ),
        )

    def render(
        self,
        view: HEOSApplicationRunOperationsDashboardHealthView,
    ) -> HEOSApplicationRunOperationsDashboardFrameResult:
        scene = self.renderer.render(view)
        frame = self.canvas_renderer.render(scene)

        return HEOSApplicationRunOperationsDashboardFrameResult(
            scene=scene,
            frame=frame,
        )
