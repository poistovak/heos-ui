from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

completion_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_completion"
)

ExecutionCompletion = (
    completion_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletion
)
ExecutionCompletionState = (
    completion_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletionState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionVerificationState(
    str,
    Enum,
):
    VERIFIED = "verified"
    FAILED = "failed"
    NOT_COMPLETED = "not_completed"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionVerification:
    sequence: int
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionVerificationState
    )
    diagnostic_code: str
    action: str
    verified: bool
    confidence: float
    reason: str

    @classmethod
    def verify(
        cls,
        completion: ExecutionCompletion,
        *,
        observed_success: bool,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionVerification:
        if completion.state is ExecutionCompletionState.MANUAL:
            return cls(
                sequence=completion.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionVerificationState.MANUAL
                ),
                diagnostic_code=completion.diagnostic_code,
                action=completion.action,
                verified=False,
                confidence=completion.confidence,
                reason="Recovery execution verification requires manual handling.",
            )

        if (
            completion.state is not ExecutionCompletionState.COMPLETED
            or not completion.completed
        ):
            return cls(
                sequence=completion.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionVerificationState.NOT_COMPLETED
                ),
                diagnostic_code=completion.diagnostic_code,
                action=completion.action,
                verified=False,
                confidence=completion.confidence,
                reason="Recovery execution was not completed.",
            )

        if not observed_success:
            return cls(
                sequence=completion.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionVerificationState.FAILED
                ),
                diagnostic_code=completion.diagnostic_code,
                action=completion.action,
                verified=False,
                confidence=completion.confidence,
                reason="Recovery execution did not produce the expected result.",
            )

        return cls(
            sequence=completion.sequence,
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionVerificationState.VERIFIED
            ),
            diagnostic_code=completion.diagnostic_code,
            action=completion.action,
            verified=True,
            confidence=completion.confidence,
            reason="Recovery execution produced the expected result.",
        )
