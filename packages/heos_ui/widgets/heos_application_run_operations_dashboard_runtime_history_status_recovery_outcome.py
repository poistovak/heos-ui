from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

executor_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_executor"
)

RecoveryExecution = (
    executor_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecution
)
RecoveryExecutionState = (
    executor_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecutionState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcomeState(
    str,
    Enum,
):
    NOT_NEEDED = "not_needed"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcome:
    sequence: int
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcomeState
    )
    diagnostic_code: str
    successful: bool
    message: str

    @classmethod
    def from_execution(
        cls,
        execution: RecoveryExecution,
        *,
        succeeded: bool | None = None,
    ) -> (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcome
    ):
        if execution.state is RecoveryExecutionState.SKIPPED:
            return cls(
                sequence=execution.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcomeState.NOT_NEEDED
                ),
                diagnostic_code=execution.diagnostic_code,
                successful=True,
                message="Recovery was not required.",
            )

        if execution.state is RecoveryExecutionState.BLOCKED:
            return cls(
                sequence=execution.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcomeState.BLOCKED
                ),
                diagnostic_code=execution.diagnostic_code,
                successful=False,
                message="Recovery execution was blocked.",
            )

        if succeeded is None:
            raise ValueError(
                "Executed recovery requires an explicit outcome."
            )

        if succeeded:
            return cls(
                sequence=execution.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcomeState.SUCCEEDED
                ),
                diagnostic_code=execution.diagnostic_code,
                successful=True,
                message="Recovery execution succeeded.",
            )

        return cls(
            sequence=execution.sequence,
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcomeState.FAILED
            ),
            diagnostic_code=execution.diagnostic_code,
            successful=False,
            message="Recovery execution failed.",
        )
