from __future__ import annotations

from dataclasses import dataclass

from heos_ui.decision.recovery import RecoveryPolicy, RecoveryState
from heos_ui.decision.recovery_scheduler import RecoveryScheduler
from heos_ui.telemetry import TelemetryService


@dataclass(slots=True)
class HealthStateTelemetry:
    telemetry: TelemetryService
    recovery: RecoveryPolicy
    recovery_scheduler: RecoveryScheduler

    def update(
        self,
        target: str,
    ) -> RecoveryState:
        state = self.recovery.state(target)

        self.telemetry.record(
            f"health.{target}.healthy",
            1.0 if state is RecoveryState.HEALTHY else 0.0,
        )
        self.telemetry.record(
            f"health.{target}.backoff",
            1.0 if state is RecoveryState.BACKOFF else 0.0,
        )
        self.telemetry.record(
            f"health.{target}.probe",
            1.0 if state is RecoveryState.PROBE else 0.0,
        )
        self.telemetry.record(
            f"health.{target}.recovery_scheduled",
            (
                1.0
                if self.recovery_scheduler.is_scheduled(target)
                else 0.0
            ),
        )

        return state