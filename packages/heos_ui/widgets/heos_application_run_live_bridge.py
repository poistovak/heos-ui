from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_live_controller import (
    HEOSApplicationRunLiveController,
    HEOSApplicationRunLiveUpdate,
)
from .heos_application_run_report import HEOSApplicationRunReport
from .heos_application_runtime import HEOSApplicationRuntime
from .heos_application_runtime_loop import HEOSApplicationLoopResult


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunLiveBridgeResult:
    report: HEOSApplicationRunReport
    update: HEOSApplicationRunLiveUpdate

    @property
    def sequence(self) -> int:
        return self.update.sequence


@dataclass(slots=True)
class HEOSApplicationRunLiveBridge:
    controller: HEOSApplicationRunLiveController
    _latest: HEOSApplicationRunLiveBridgeResult | None = None

    @property
    def latest(self) -> HEOSApplicationRunLiveBridgeResult | None:
        return self._latest

    @property
    def has_data(self) -> bool:
        return self._latest is not None

    def publish(
        self,
        application: HEOSApplicationRuntime,
        result: HEOSApplicationLoopResult,
        *,
        requested: int,
    ) -> HEOSApplicationRunLiveBridgeResult:
        report = HEOSApplicationRunReport.capture(
            application,
            result,
            requested=requested,
        )
        update = self.controller.update(report)

        bridge_result = HEOSApplicationRunLiveBridgeResult(
            report=report,
            update=update,
        )
        self._latest = bridge_result

        return bridge_result

    def clear(self) -> None:
        self.controller.clear()
        self._latest = None
