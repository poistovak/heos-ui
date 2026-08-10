import importlib

delivery_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_delivery"
)
receipt_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "dispatch_receipt"
)

Delivery = (
    delivery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDelivery
)
DeliveryState = (
    delivery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDeliveryState
)
Receipt = (
    receipt_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceipt
)
ReceiptState = (
    receipt_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceiptState
)


def receipt(
    *,
    sequence: int = 1,
    state: ReceiptState = ReceiptState.ACCEPTED,
    code: str = "RUN_SYNC_MISMATCH",
    action: str = "Retry synchronization.",
    accepted: bool = True,
    confidence: float = 0.75,
) -> Receipt:
    return Receipt(
        sequence=sequence,
        state=state,
        diagnostic_code=code,
        action=action,
        accepted=accepted,
        confidence=confidence,
        reason="receipt",
    )


def test_accepted_receipt_becomes_delivered() -> None:
    delivery = Delivery.from_receipt(
        receipt()
    )

    assert delivery.state is DeliveryState.DELIVERED


def test_delivered_state_sets_delivered_true() -> None:
    delivery = Delivery.from_receipt(
        receipt()
    )

    assert delivery.delivered


def test_delivered_state_has_reason() -> None:
    delivery = Delivery.from_receipt(
        receipt()
    )

    assert delivery.reason == "Recovery command was delivered."


def test_rejected_receipt_becomes_failed() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            state=ReceiptState.REJECTED,
            accepted=False,
        )
    )

    assert delivery.state is DeliveryState.FAILED


def test_failed_delivery_is_not_delivered() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            state=ReceiptState.REJECTED,
            accepted=False,
        )
    )

    assert not delivery.delivered


def test_failed_delivery_has_reason() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            state=ReceiptState.REJECTED,
            accepted=False,
        )
    )

    assert delivery.reason == "Recovery command delivery failed."


def test_manual_receipt_becomes_manual_delivery() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            state=ReceiptState.MANUAL,
            accepted=False,
        )
    )

    assert delivery.state is DeliveryState.MANUAL


def test_manual_delivery_is_not_delivered() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            state=ReceiptState.MANUAL,
            accepted=False,
        )
    )

    assert not delivery.delivered


def test_manual_delivery_has_reason() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            state=ReceiptState.MANUAL,
            accepted=False,
        )
    )

    assert delivery.reason == (
        "Recovery delivery requires manual handling."
    )


def test_delivery_preserves_sequence() -> None:
    delivery = Delivery.from_receipt(
        receipt(sequence=11)
    )

    assert delivery.sequence == 11


def test_delivery_preserves_diagnostic_code() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            code="RUN_STATUS_COUNT_MISMATCH",
        )
    )

    assert delivery.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_delivery_preserves_action() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            action="Retry status generation.",
        )
    )

    assert delivery.action == "Retry status generation."


def test_delivery_preserves_confidence() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            confidence=0.89,
        )
    )

    assert delivery.confidence == 0.89


def test_zero_confidence_is_preserved() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            confidence=0.0,
        )
    )

    assert delivery.confidence == 0.0


def test_delivered_snapshot_preserves_identity() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            sequence=7,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            confidence=0.62,
        )
    )

    assert delivery.sequence == 7
    assert delivery.diagnostic_code == "RUN_SYNC_MISMATCH"
    assert delivery.action == "Retry synchronization."
    assert delivery.confidence == 0.62


def test_failed_delivery_preserves_sequence() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            sequence=4,
            state=ReceiptState.REJECTED,
            accepted=False,
        )
    )

    assert delivery.sequence == 4


def test_manual_delivery_preserves_sequence() -> None:
    delivery = Delivery.from_receipt(
        receipt(
            sequence=5,
            state=ReceiptState.MANUAL,
            accepted=False,
        )
    )

    assert delivery.sequence == 5
