from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from heos_ui.events.bus import EventBus
from heos_ui.runtime.scheduler_core import Scheduler
from heos_ui.telemetry import TelemetryService

from .engine import DiagnosticResult, DiagnosticsEngine


@dataclass(frozen=True, slots=True)
class HealthSnapshot:
    healthy: bool
    check_count: int
    failed_count: int


@dataclass(slots=True)
class HealthMonitor:
    diagnostics: DiagnosticsEngine
    telemetry: TelemetryService
    event_bus: EventBus

    _checks: list[Callable[[], DiagnosticResult]] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def register(
        self,
        check: Callable[[], DiagnosticResult],
    ) -> None:
        self._checks.append(check)

    def run(self) -> HealthSnapshot:
        self.diagnostics.clear()

        for check in self._checks:
            self.diagnostics.record(check())

        results = self.diagnostics.report()
        failed_count = sum(
            not result.healthy
            for result in results
        )

        snapshot = HealthSnapshot(
            healthy=self.diagnostics.healthy(),
            check_count=len(results),
            failed_count=failed_count,
        )

        self.telemetry.record(
            "health.healthy",
            1.0 if snapshot.healthy else 0.0,
        )
        self.telemetry.record(
            "health.check_count",
            float(snapshot.check_count),
        )
        self.telemetry.record(
            "health.failed_count",
            float(snapshot.failed_count),
        )

        self.event_bus.publish(
            "health.completed",
            snapshot,
        )

        return snapshot

    def schedule(
        self,
        scheduler: Scheduler,
        interval: float,
    ) -> None:
        if interval <= 0.0:
            raise ValueError(
                "Health-check interval must be positive."
            )

        scheduler.every(
            interval,
            self.run,
        )

    @property
    def check_count(self) -> int:
        return len(self._checks)