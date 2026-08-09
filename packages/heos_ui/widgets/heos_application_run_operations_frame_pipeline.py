from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_canvas_renderer import (
    HEOSApplicationRunOperationsCanvasFrame,
    HEOSApplicationRunOperationsCanvasRenderer,
)
from .heos_application_run_operations_health_renderer import (
    HEOSApplicationRunOperationsHealthRenderer,
    HEOSApplicationRunOperationsRenderScene,
)
from .heos_application_run_operations_health_widget import (
    HEOSApplicationRunOperationsHealthView,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsFrameResult:
    scene: HEOSApplicationRunOperationsRenderScene
    frame: HEOSApplicationRunOperationsCanvasFrame

    @property
    def command_count(self) -> int:
        return self.frame.command_count


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsFramePipeline:
    renderer: HEOSApplicationRunOperationsHealthRenderer
    canvas_renderer: HEOSApplicationRunOperationsCanvasRenderer

    @classmethod
    def create(cls) -> HEOSApplicationRunOperationsFramePipeline:
        return cls(
            renderer=HEOSApplicationRunOperationsHealthRenderer(),
            canvas_renderer=HEOSApplicationRunOperationsCanvasRenderer(),
        )

    def render(
        self,
        view: HEOSApplicationRunOperationsHealthView,
    ) -> HEOSApplicationRunOperationsFrameResult:
        scene = self.renderer.render(view)
        frame = self.canvas_renderer.render(scene)

        return HEOSApplicationRunOperationsFrameResult(
            scene=scene,
            frame=frame,
        )
