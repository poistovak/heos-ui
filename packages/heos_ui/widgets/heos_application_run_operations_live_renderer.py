from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_canvas_renderer import (
    HEOSApplicationRunOperationsCanvasFrame,
)
from .heos_application_run_operations_frame_pipeline import (
    HEOSApplicationRunOperationsFramePipeline,
    HEOSApplicationRunOperationsFrameResult,
)
from .heos_application_run_operations_health_widget import (
    HEOSApplicationRunOperationsHealthView,
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsLiveRenderer:
    pipeline: HEOSApplicationRunOperationsFramePipeline
    _latest: HEOSApplicationRunOperationsFrameResult | None = None
    _render_count: int = 0

    @classmethod
    def create(cls) -> HEOSApplicationRunOperationsLiveRenderer:
        return cls(
            pipeline=HEOSApplicationRunOperationsFramePipeline.create(),
        )

    @property
    def latest(self) -> HEOSApplicationRunOperationsFrameResult | None:
        return self._latest

    @property
    def latest_frame(
        self,
    ) -> HEOSApplicationRunOperationsCanvasFrame | None:
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
        view: HEOSApplicationRunOperationsHealthView,
    ) -> HEOSApplicationRunOperationsCanvasFrame:
        result = self.pipeline.render(view)

        self._latest = result
        self._render_count += 1

        return result.frame

    def clear(self) -> None:
        self._latest = None
