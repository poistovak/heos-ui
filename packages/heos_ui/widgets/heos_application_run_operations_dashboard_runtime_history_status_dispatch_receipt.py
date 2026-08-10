from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

dispatch_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_dispatch"
)

RecoveryDispatch = (
    dispatch_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatch
)
RecoveryDispatchState = (
    dispatch_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatchState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceiptState(
    str,
    Enum,
):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceipt:
    sequence: int
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceiptState
    )
    diagnostic_code: str
    action: str
    accepted: bool
    confidence: float
    reason: str

    @classmethod
    def from_dispatch(
        cls,
        dispatch: RecoveryDispatch,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceipt:
        if dispatch.state is RecoveryDispatchState.DISPATCHED:
            return cls(
                sequence=dispatch.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceiptState.ACCEPTED
                ),
                diagnostic_code=dispatch.diagnostic_code,
                action=dispatch.action,
                accepted=True,
                confidence=dispatch.confidence,
                reason="Recovery dispatch was accepted.",
            )

        if dispatch.state is RecoveryDispatchState.MANUAL:
            return cls(
                sequence=dispatch.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceiptState.MANUAL
                ),
                diagnostic_code=dispatch.diagnostic_code,
                action=dispatch.action,
                accepted=False,
                confidence=dispatch.confidence,
                reason="Recovery dispatch requires manual handling.",
            )

        return cls(
            sequence=dispatch.sequence,
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceiptState.REJECTED
            ),
            diagnostic_code=dispatch.diagnostic_code,
            action=dispatch.action,
            accepted=False,
            confidence=dispatch.confidence,
            reason="Recovery dispatch was rejected.",
        )
