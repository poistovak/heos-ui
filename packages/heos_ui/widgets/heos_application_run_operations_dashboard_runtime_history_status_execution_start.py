from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

request_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_request"
)

ExecutionRequest = (
    request_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequest
)
ExecutionRequestState = (
    request_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequestState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStartState(
    str,
    Enum,
):
    STARTED = "started"
    BLOCKED = "blocked"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStart:
    sequence: int
    state: HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStartState
    diagnostic_code: str
    action: str
    started: bool
    confidence: float
    reason: str

    @classmethod
    def from_request(
        cls,
        request: ExecutionRequest,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStart:
        if request.state is ExecutionRequestState.READY and request.executable:
            return cls(
                sequence=request.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStartState.STARTED
                ),
                diagnostic_code=request.diagnostic_code,
                action=request.action,
                started=True,
                confidence=request.confidence,
                reason="Recovery execution was started.",
            )

        if request.state is ExecutionRequestState.MANUAL:
            return cls(
                sequence=request.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStartState.MANUAL
                ),
                diagnostic_code=request.diagnostic_code,
                action=request.action,
                started=False,
                confidence=request.confidence,
                reason="Recovery execution start requires manual handling.",
            )

        return cls(
            sequence=request.sequence,
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStartState.BLOCKED
            ),
            diagnostic_code=request.diagnostic_code,
            action=request.action,
            started=False,
            confidence=request.confidence,
            reason="Recovery execution start was blocked.",
        )
