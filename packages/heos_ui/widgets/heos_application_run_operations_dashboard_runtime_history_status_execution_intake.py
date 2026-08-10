from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

delivery_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_delivery"
)

RecoveryDelivery = (
    delivery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDelivery
)
RecoveryDeliveryState = (
    delivery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDeliveryState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntakeState(
    str,
    Enum,
):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntake:
    sequence: int
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntakeState
    )
    diagnostic_code: str
    action: str
    accepted: bool
    confidence: float
    reason: str

    @classmethod
    def from_delivery(
        cls,
        delivery: RecoveryDelivery,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntake:
        if delivery.state is RecoveryDeliveryState.DELIVERED:
            return cls(
                sequence=delivery.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntakeState.ACCEPTED
                ),
                diagnostic_code=delivery.diagnostic_code,
                action=delivery.action,
                accepted=True,
                confidence=delivery.confidence,
                reason="Recovery delivery was accepted for execution.",
            )

        if delivery.state is RecoveryDeliveryState.MANUAL:
            return cls(
                sequence=delivery.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntakeState.MANUAL
                ),
                diagnostic_code=delivery.diagnostic_code,
                action=delivery.action,
                accepted=False,
                confidence=delivery.confidence,
                reason="Recovery execution intake requires manual handling.",
            )

        return cls(
            sequence=delivery.sequence,
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntakeState.REJECTED
            ),
            diagnostic_code=delivery.diagnostic_code,
            action=delivery.action,
            accepted=False,
            confidence=delivery.confidence,
            reason="Recovery delivery was rejected by execution intake.",
        )
