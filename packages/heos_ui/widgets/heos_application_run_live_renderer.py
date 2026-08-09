from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_canvas_renderer import (
    HEOSApplicationRunCanvasFrame,
)
from .heos_application_run_frame_pipeline import (
    HEOSApplicationRunFramePipeline,
    HEOSApplicationRunFrameResult,
)
from .heos_application_run_status import HEOSApplicationRunStatusView


@dataclass(slots=True)
class HEOSApplicationRunLiveRenderer:
    pipeline: HEOSApplicationRunFramePipeline
    _latest: HEOSApplicationRunFrameResult | None = None
    _render_count: int = 0

    @classmethod
    def create(cls) -> HEOSApplicationRunLiveRenderer:
        return cls(
            pipeline=HEOSApplicationRunFramePipeline.create(),
        )

    @property
    def latest(self) -> HEOSApplicationRunFrameResult | None:
        return self._latest

    @property
    def latest_frame(self) -> HEOSApplicationRunCanvasFrame | None:
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
        view: HEOSApplicationRunStatusView,
    ) -> HEOSApplicationRunCanvasFrame:
        result = self.pipeline.render(view)

        self._latest = result
        self._render_count += 1

        return result.frame

    def clear(self) -> None:
        self._latest = None
