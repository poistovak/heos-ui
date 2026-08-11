from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

intake_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_intake"
)

ExecutionIntake = (
    intake_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntake
)
ExecutionIntakeState = (
    intake_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntakeState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequestState(
    str,
    Enum,
):
    READY = "ready"
    REJECTED = "rejected"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequest:
    sequence: int
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequestState
    )
    diagnostic_code: str
    action: str
    executable: bool
    confidence: float
    reason: str

    @classmethod
    def from_intake(
        cls,
        intake: ExecutionIntake,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequest:
        if intake.state is ExecutionIntakeState.ACCEPTED:
            return cls(
                sequence=intake.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequestState.READY
                ),
                diagnostic_code=intake.diagnostic_code,
                action=intake.action,
                executable=True,
                confidence=intake.confidence,
                reason="Recovery execution request is ready.",
            )

        if intake.state is ExecutionIntakeState.MANUAL:
            return cls(
                sequence=intake.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequestState.MANUAL
                ),
                diagnostic_code=intake.diagnostic_code,
                action=intake.action,
                executable=False,
                confidence=intake.confidence,
                reason="Recovery execution request requires manual handling.",
            )

        return cls(
            sequence=intake.sequence,
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequestState.REJECTED
            ),
            diagnostic_code=intake.diagnostic_code,
            action=intake.action,
            executable=False,
            confidence=intake.confidence,
            reason="Recovery execution request was rejected.",
        )
