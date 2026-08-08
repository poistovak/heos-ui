from __future__ import annotations

from dataclasses import dataclass

from .heos_application_loop_telemetry import HEOSApplicationLoopTelemetry
from .heos_application_runtime import (
    HEOSApplicationRuntime,
    HEOSApplicationState,
)
from .heos_application_runtime_loop import HEOSApplicationLoopResult


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunReport:
    state: HEOSApplicationState
    requested: int
    processed: int
    rendered: int
    skipped: int
    first_cycle: int | None
    last_cycle: int | None
    completed: bool
    stopped: bool

    @property
    def empty(self) -> bool:
        return self.processed == 0

    @property
    def interrupted(self) -> bool:
        return self.stopped and not self.completed

    @classmethod
    def capture(
        cls,
        application: HEOSApplicationRuntime,
        result: HEOSApplicationLoopResult,
        *,
        requested: int,
    ) -> HEOSApplicationRunReport:
        telemetry = HEOSApplicationLoopTelemetry.capture(
            result,
            requested=requested,
        )

        return cls(
            state=application.state,
            requested=telemetry.requested,
            processed=telemetry.processed,
            rendered=telemetry.rendered,
            skipped=telemetry.skipped,
            first_cycle=telemetry.first_cycle,
            last_cycle=telemetry.last_cycle,
            completed=telemetry.completed,
            stopped=telemetry.stopped,
        )
