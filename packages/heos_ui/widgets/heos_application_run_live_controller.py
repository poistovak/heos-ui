from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_canvas_renderer import (
    HEOSApplicationRunCanvasFrame,
)
from .heos_application_run_live_renderer import (
    HEOSApplicationRunLiveRenderer,
)
from .heos_application_run_report import HEOSApplicationRunReport
from .heos_application_run_status import HEOSApplicationRunStatusView
from .heos_application_run_status_controller import (
    HEOSApplicationRunStatusController,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunLiveUpdate:
    view: HEOSApplicationRunStatusView
    frame: HEOSApplicationRunCanvasFrame
    sequence: int


@dataclass(slots=True)
class HEOSApplicationRunLiveController:
    controller: HEOSApplicationRunStatusController
    renderer: HEOSApplicationRunLiveRenderer
    _latest: HEOSApplicationRunLiveUpdate | None = None
    _update_count: int = 0

    @property
    def latest(self) -> HEOSApplicationRunLiveUpdate | None:
        return self._latest

    @property
    def latest_frame(self) -> HEOSApplicationRunCanvasFrame | None:
        if self._latest is None:
            return None

        return self._latest.frame

    @property
    def update_count(self) -> int:
        return self._update_count

    @property
    def has_data(self) -> bool:
        return self._latest is not None

    def update(
        self,
        report: HEOSApplicationRunReport,
    ) -> HEOSApplicationRunLiveUpdate:
        view = self.controller.update(report)
        frame = self.renderer.render(view)

        self._update_count += 1

        update = HEOSApplicationRunLiveUpdate(
            view=view,
            frame=frame,
            sequence=self._update_count,
        )

        self._latest = update
        return update

    def clear(self) -> None:
        self.controller.clear()
        self.renderer.clear()
        self._latest = None
