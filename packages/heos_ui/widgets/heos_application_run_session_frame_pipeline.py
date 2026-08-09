from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_session_canvas_renderer import (
    HEOSApplicationRunSessionCanvasFrame,
    HEOSApplicationRunSessionCanvasRenderer,
)
from .heos_application_run_session_health_renderer import (
    HEOSApplicationRunSessionHealthRenderer,
    HEOSApplicationRunSessionRenderScene,
)
from .heos_application_run_session_health_widget import (
    HEOSApplicationRunSessionHealthView,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionFrameResult:
    scene: HEOSApplicationRunSessionRenderScene
    frame: HEOSApplicationRunSessionCanvasFrame

    @property
    def command_count(self) -> int:
        return self.frame.command_count


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionFramePipeline:
    renderer: HEOSApplicationRunSessionHealthRenderer
    canvas_renderer: HEOSApplicationRunSessionCanvasRenderer

    @classmethod
    def create(cls) -> HEOSApplicationRunSessionFramePipeline:
        return cls(
            renderer=HEOSApplicationRunSessionHealthRenderer(),
            canvas_renderer=HEOSApplicationRunSessionCanvasRenderer(),
        )

    def render(
        self,
        view: HEOSApplicationRunSessionHealthView,
    ) -> HEOSApplicationRunSessionFrameResult:
        scene = self.renderer.render(view)
        frame = self.canvas_renderer.render(scene)

        return HEOSApplicationRunSessionFrameResult(
            scene=scene,
            frame=frame,
        )
