from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_live_session import (
    HEOSApplicationRunLiveSession,
)
from .heos_application_run_session_canvas_renderer import (
    HEOSApplicationRunSessionCanvasFrame,
)
from .heos_application_run_session_health_pipeline import (
    HEOSApplicationRunSessionHealthPipeline,
    HEOSApplicationRunSessionHealthPipelineResult,
)
from .heos_application_run_session_health_widget import (
    HEOSApplicationRunSessionHealthView,
    HEOSApplicationRunSessionHealthWidget,
)
from .heos_application_run_session_live_renderer import (
    HEOSApplicationRunSessionLiveRenderer,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionOperationsUpdate:
    health: HEOSApplicationRunSessionHealthPipelineResult
    view: HEOSApplicationRunSessionHealthView
    frame: HEOSApplicationRunSessionCanvasFrame
    sequence: int


@dataclass(slots=True)
class HEOSApplicationRunSessionOperationsController:
    pipeline: HEOSApplicationRunSessionHealthPipeline
    widget: HEOSApplicationRunSessionHealthWidget
    renderer: HEOSApplicationRunSessionLiveRenderer
    _latest: HEOSApplicationRunSessionOperationsUpdate | None = None
    _sequence: int = 0

    @classmethod
    def create(cls) -> HEOSApplicationRunSessionOperationsController:
        return cls(
            pipeline=HEOSApplicationRunSessionHealthPipeline.create(),
            widget=HEOSApplicationRunSessionHealthWidget(),
            renderer=HEOSApplicationRunSessionLiveRenderer.create(),
        )

    @property
    def latest(self) -> HEOSApplicationRunSessionOperationsUpdate | None:
        return self._latest

    @property
    def sequence(self) -> int:
        return self._sequence

    @property
    def has_update(self) -> bool:
        return self._latest is not None

    def update(
        self,
        session: HEOSApplicationRunLiveSession,
    ) -> HEOSApplicationRunSessionOperationsUpdate:
        health = self.pipeline.evaluate(session)
        view = self.widget.update(health.presentation)
        frame = self.renderer.render(view)

        self._sequence += 1

        update = HEOSApplicationRunSessionOperationsUpdate(
            health=health,
            view=view,
            frame=frame,
            sequence=self._sequence,
        )
        self._latest = update

        return update

    def clear(self) -> None:
        self.widget.clear()
        self.renderer.clear()
        self._latest = None
