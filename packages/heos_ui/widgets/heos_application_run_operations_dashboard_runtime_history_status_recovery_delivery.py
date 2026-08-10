from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

receipt_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "dispatch_receipt"
)

DispatchReceipt = (
    receipt_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceipt
)
DispatchReceiptState = (
    receipt_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceiptState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDeliveryState(
    str,
    Enum,
):
    DELIVERED = "delivered"
    FAILED = "failed"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDelivery:
    sequence: int
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDeliveryState
    )
    diagnostic_code: str
    action: str
    delivered: bool
    confidence: float
    reason: str

    @classmethod
    def from_receipt(
        cls,
        receipt: DispatchReceipt,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDelivery:
        if receipt.state is DispatchReceiptState.ACCEPTED:
            return cls(
                sequence=receipt.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDeliveryState.DELIVERED
                ),
                diagnostic_code=receipt.diagnostic_code,
                action=receipt.action,
                delivered=True,
                confidence=receipt.confidence,
                reason="Recovery command was delivered.",
            )

        if receipt.state is DispatchReceiptState.MANUAL:
            return cls(
                sequence=receipt.sequence,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDeliveryState.MANUAL
                ),
                diagnostic_code=receipt.diagnostic_code,
                action=receipt.action,
                delivered=False,
                confidence=receipt.confidence,
                reason="Recovery delivery requires manual handling.",
            )

        return cls(
            sequence=receipt.sequence,
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDeliveryState.FAILED
            ),
            diagnostic_code=receipt.diagnostic_code,
            action=receipt.action,
            delivered=False,
            confidence=receipt.confidence,
            reason="Recovery command delivery failed.",
        )
