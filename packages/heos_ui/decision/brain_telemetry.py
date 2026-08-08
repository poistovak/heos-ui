from __future__ import annotations

from dataclasses import dataclass

from heos_ui.telemetry import TelemetryService

from .brain import BrainCycleReport


@dataclass(slots=True)
class BrainCycleTelemetry:
    telemetry: TelemetryService

    def record(
        self,
        report: BrainCycleReport,
    ) -> None:
        runtime = report.cycle.report

        self.telemetry.record(
            "brain.cycle.sequence",
            float(report.sequence),
        )
        self.telemetry.record(
            "brain.cycle.accepted",
            float(runtime.accepted),
        )
        self.telemetry.record(
            "brain.cycle.blocked",
            float(runtime.blocked),
        )
        self.telemetry.record(
            "brain.cycle.executed",
            float(runtime.executed),
        )
        self.telemetry.record(
            "brain.health.healthy_targets",
            float(report.healthy_targets),
        )
        self.telemetry.record(
            "brain.health.unhealthy_targets",
            float(report.unhealthy_targets),
        )
        self.telemetry.record(
            "brain.cycle.successful",
            1.0 if report.successful else 0.0,
        )