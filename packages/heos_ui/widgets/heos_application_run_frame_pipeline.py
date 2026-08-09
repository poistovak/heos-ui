from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_canvas_renderer import (
    HEOSApplicationRunCanvasFrame,
    HEOSApplicationRunCanvasRenderer,
)
from .heos_application_run_status import HEOSApplicationRunStatusView
from .heos_application_run_status_renderer import (
    HEOSApplicationRunRenderScene,
    HEOSApplicationRunStatusRenderer,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunFrameResult:
    scene: HEOSApplicationRunRenderScene
    frame: HEOSApplicationRunCanvasFrame

    @property
    def command_count(self) -> int:
        return self.frame.command_count


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunFramePipeline:
    renderer: HEOSApplicationRunStatusRenderer
    canvas_renderer: HEOSApplicationRunCanvasRenderer

    @classmethod
    def create(cls) -> HEOSApplicationRunFramePipeline:
        return cls(
            renderer=HEOSApplicationRunStatusRenderer(),
            canvas_renderer=HEOSApplicationRunCanvasRenderer(),
        )

    def render(
        self,
        view: HEOSApplicationRunStatusView,
    ) -> HEOSApplicationRunFrameResult:
        scene = self.renderer.render(view)
        frame = self.canvas_renderer.render(scene)

        return HEOSApplicationRunFrameResult(
            scene=scene,
            frame=frame,
        )
