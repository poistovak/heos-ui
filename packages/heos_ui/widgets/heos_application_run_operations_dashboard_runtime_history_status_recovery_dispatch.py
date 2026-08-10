from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

command_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_command"
)

RecoveryCommand = (
    command_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommand
)
RecoveryCommandState = (
    command_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommandState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatchState(
    str,
    Enum,
):
    DISPATCHED = "dispatched"
    REJECTED = "rejected"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatch:
    sequence: int
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatchState
    )
    diagnostic_code: str
    action: str
    dispatched: bool
    confidence: float
    reason: str


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatcher:
    _dispatch_count: int = 0
    _latest: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatch
        | None
    ) = None

    @property
    def dispatch_count(self) -> int:
        return self._dispatch_count

    @property
    def latest(
        self,
    ) -> (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatch
        | None
    ):
        return self._latest

    @property
    def has_dispatches(self) -> bool:
        return self._latest is not None

    def dispatch(
        self,
        command: RecoveryCommand,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatch:
        self._dispatch_count += 1

        if command.state is RecoveryCommandState.MANUAL:
            state = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatchState.MANUAL
            )
            dispatched = False
            reason = "Recovery command requires manual dispatch."
        elif (
            command.state is RecoveryCommandState.BLOCKED
            or not command.executable
        ):
            state = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatchState.REJECTED
            )
            dispatched = False
            reason = "Recovery command was rejected by dispatcher."
        else:
            state = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatchState.DISPATCHED
            )
            dispatched = True
            reason = "Recovery command was dispatched."

        result = (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatch(
                sequence=self._dispatch_count,
                state=state,
                diagnostic_code=command.diagnostic_code,
                action=command.action,
                dispatched=dispatched,
                confidence=command.confidence,
                reason=reason,
            )
        )

        self._latest = result
        return result

    def reset(self) -> None:
        self._dispatch_count = 0
        self._latest = None
