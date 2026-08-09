from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_session_canvas_renderer import (
    HEOSApplicationRunSessionCanvasFrame,
)
from .heos_application_run_session_frame_pipeline import (
    HEOSApplicationRunSessionFramePipeline,
    HEOSApplicationRunSessionFrameResult,
)
from .heos_application_run_session_health_widget import (
    HEOSApplicationRunSessionHealthView,
)


@dataclass(slots=True)
class HEOSApplicationRunSessionLiveRenderer:
    pipeline: HEOSApplicationRunSessionFramePipeline
    _latest: HEOSApplicationRunSessionFrameResult | None = None
    _render_count: int = 0

    @classmethod
    def create(cls) -> HEOSApplicationRunSessionLiveRenderer:
        return cls(
            pipeline=HEOSApplicationRunSessionFramePipeline.create(),
        )

    @property
    def latest(self) -> HEOSApplicationRunSessionFrameResult | None:
        return self._latest

    @property
    def latest_frame(self) -> HEOSApplicationRunSessionCanvasFrame | None:
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
        view: HEOSApplicationRunSessionHealthView,
    ) -> HEOSApplicationRunSessionCanvasFrame:
        result = self.pipeline.render(view)

        self._latest = result
        self._render_count += 1

        return result.frame

    def clear(self) -> None:
        self._latest = None
