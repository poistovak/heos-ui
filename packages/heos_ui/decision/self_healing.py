from __future__ import annotations

from dataclasses import dataclass

from heos_ui.energy import EnergySnapshot
from heos_ui.execution.pipeline import (
    PipelineResult,
    SafeExecutionPipeline,
)

from .conflict import DecisionAction
from .recovery import RecoveryPolicy, RecoveryState
from .recovery_scheduler import RecoveryScheduler


@dataclass(slots=True)
class SelfHealingCoordinator:
    pipeline: SafeExecutionPipeline
    recovery: RecoveryPolicy
    recovery_scheduler: RecoveryScheduler

    def execute(
        self,
        snapshot: EnergySnapshot,
        candidate: DecisionAction,
        *,
        success: bool = True,
        message: str = "",
    ) -> PipelineResult:
        result = self.pipeline.execute(
            snapshot,
            candidate,
            success=success,
            message=message,
        )

        target = candidate.action.target
        state = self.recovery.state(target)

        if (
            state is RecoveryState.BACKOFF
            and not self.recovery_scheduler.is_scheduled(target)
        ):
            self.recovery_scheduler.schedule_probe(target)

        return result

    def state(
        self,
        target: str,
    ) -> RecoveryState:
        return self.recovery.state(target)

    def is_recovery_scheduled(
        self,
        target: str,
    ) -> bool:
        return self.recovery_scheduler.is_scheduled(target)