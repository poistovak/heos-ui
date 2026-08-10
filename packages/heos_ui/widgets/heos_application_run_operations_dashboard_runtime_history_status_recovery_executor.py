from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

decision_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_decision"
)

RecoveryDecision = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecision
)
RecoveryDecisionState = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecisionState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecutionState(
    str,
    Enum,
):
    SKIPPED = "skipped"
    EXECUTED = "executed"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecution:
    sequence: int
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecutionState
    )
    diagnostic_code: str
    action: str
    executed: bool


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecutor:
    _execution_count: int = 0
    _latest: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecution
        | None
    ) = None

    @property
    def execution_count(self) -> int:
        return self._execution_count

    @property
    def latest(
        self,
    ) -> (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecution
        | None
    ):
        return self._latest

    @property
    def has_executions(self) -> bool:
        return self._latest is not None

    def execute(
        self,
        decision: RecoveryDecision,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecution:
        self._execution_count += 1

        if decision.state is RecoveryDecisionState.SKIP:
            state = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecutionState.SKIPPED
            )
            executed = False
        elif decision.state is RecoveryDecisionState.HOLD:
            state = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecutionState.BLOCKED
            )
            executed = False
        else:
            state = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecutionState.EXECUTED
            )
            executed = True

        execution = (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecution(
                sequence=self._execution_count,
                state=state,
                diagnostic_code=decision.diagnostic_code,
                action=decision.action,
                executed=executed,
            )
        )

        self._latest = execution
        return execution

    def reset(self) -> None:
        self._execution_count = 0
        self._latest = None
