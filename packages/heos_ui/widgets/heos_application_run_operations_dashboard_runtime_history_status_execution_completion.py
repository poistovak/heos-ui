from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

start_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_start"
)

ExecutionStart = (
    start_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStart
)
ExecutionStartState = (
    start_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStartState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletionState(
    str,
    Enum,
):
    COMPLETED = "completed"
    NOT_STARTED = "not_started"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletion:
    sequence: int
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletionState
    )
    diagnostic_code: str
    action: str
    completed: bool
    confidence: float
    reason: str

    @classmethod
    def from_start(
        cls,
        start: ExecutionStart,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletion:
        if start.state is ExecutionStartState.STARTED and start.started:
            return cls(
                sequence=start.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletionState.COMPLETED
                ),
                diagnostic_code=start.diagnostic_code,
                action=start.action,
                completed=True,
                confidence=start.confidence,
                reason="Recovery execution completed.",
            )

        if start.state is ExecutionStartState.MANUAL:
            return cls(
                sequence=start.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletionState.MANUAL
                ),
                diagnostic_code=start.diagnostic_code,
                action=start.action,
                completed=False,
                confidence=start.confidence,
                reason="Recovery execution completion requires manual handling.",
            )

        return cls(
            sequence=start.sequence,
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletionState.NOT_STARTED
            ),
            diagnostic_code=start.diagnostic_code,
            action=start.action,
            completed=False,
            confidence=start.confidence,
            reason="Recovery execution was not started.",
        )
