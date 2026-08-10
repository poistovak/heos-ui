from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

outcome_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_outcome"
)

RecoveryOutcome = (
    outcome_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcome
)
RecoveryOutcomeState = (
    outcome_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcomeState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackState(
    str,
    Enum,
):
    NONE = "none"
    POSITIVE = "positive"
    NEGATIVE = "negative"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedback:
    sequence: int
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackState
    )
    diagnostic_code: str
    learned: bool
    retry_recommended: bool
    message: str

    @classmethod
    def from_outcome(
        cls,
        outcome: RecoveryOutcome,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedback:
        if outcome.state is RecoveryOutcomeState.NOT_NEEDED:
            return cls(
                sequence=outcome.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackState.NONE
                ),
                diagnostic_code=outcome.diagnostic_code,
                learned=False,
                retry_recommended=False,
                message="No recovery feedback is required.",
            )

        if outcome.state is RecoveryOutcomeState.SUCCEEDED:
            return cls(
                sequence=outcome.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackState.POSITIVE
                ),
                diagnostic_code=outcome.diagnostic_code,
                learned=True,
                retry_recommended=False,
                message="Recovery succeeded and produced positive feedback.",
            )

        if outcome.state is RecoveryOutcomeState.FAILED:
            return cls(
                sequence=outcome.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackState.NEGATIVE
                ),
                diagnostic_code=outcome.diagnostic_code,
                learned=True,
                retry_recommended=True,
                message="Recovery failed and requires further evaluation.",
            )

        return cls(
            sequence=outcome.sequence,
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackState.MANUAL
            ),
            diagnostic_code=outcome.diagnostic_code,
            learned=True,
            retry_recommended=False,
            message="Recovery was blocked and requires manual intervention.",
        )
