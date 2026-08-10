import importlib

dispatch_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_dispatch"
)
receipt_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "dispatch_receipt"
)

Dispatch = (
    dispatch_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatch
)
DispatchState = (
    dispatch_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatchState
)
Receipt = (
    receipt_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceipt
)
ReceiptState = (
    receipt_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDispatchReceiptState
)


def dispatch(
    *,
    sequence: int = 1,
    state: DispatchState = DispatchState.DISPATCHED,
    code: str = "RUN_SYNC_MISMATCH",
    action: str = "Retry synchronization.",
    dispatched: bool = True,
    confidence: float = 0.75,
) -> Dispatch:
    return Dispatch(
        sequence=sequence,
        state=state,
        diagnostic_code=code,
        action=action,
        dispatched=dispatched,
        confidence=confidence,
        reason="dispatch",
    )


def test_dispatched_becomes_accepted() -> None:
    receipt = Receipt.from_dispatch(
        dispatch()
    )

    assert receipt.state is ReceiptState.ACCEPTED


def test_accepted_receipt_is_accepted() -> None:
    receipt = Receipt.from_dispatch(
        dispatch()
    )

    assert receipt.accepted


def test_accepted_receipt_has_reason() -> None:
    receipt = Receipt.from_dispatch(
        dispatch()
    )

    assert receipt.reason == "Recovery dispatch was accepted."


def test_rejected_dispatch_becomes_rejected() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            state=DispatchState.REJECTED,
            dispatched=False,
        )
    )

    assert receipt.state is ReceiptState.REJECTED


def test_rejected_receipt_is_not_accepted() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            state=DispatchState.REJECTED,
            dispatched=False,
        )
    )

    assert not receipt.accepted


def test_rejected_receipt_has_reason() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            state=DispatchState.REJECTED,
            dispatched=False,
        )
    )

    assert receipt.reason == "Recovery dispatch was rejected."


def test_manual_dispatch_becomes_manual() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            state=DispatchState.MANUAL,
            dispatched=False,
        )
    )

    assert receipt.state is ReceiptState.MANUAL


def test_manual_receipt_is_not_accepted() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            state=DispatchState.MANUAL,
            dispatched=False,
        )
    )

    assert not receipt.accepted


def test_manual_receipt_has_reason() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            state=DispatchState.MANUAL,
            dispatched=False,
        )
    )

    assert receipt.reason == (
        "Recovery dispatch requires manual handling."
    )


def test_receipt_preserves_sequence() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(sequence=7)
    )

    assert receipt.sequence == 7


def test_receipt_preserves_diagnostic_code() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            code="RUN_STATUS_COUNT_MISMATCH",
        )
    )

    assert receipt.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_receipt_preserves_action() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            action="Retry status generation.",
        )
    )

    assert receipt.action == "Retry status generation."


def test_receipt_preserves_confidence() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            confidence=0.88,
        )
    )

    assert receipt.confidence == 0.88


def test_zero_confidence_is_preserved() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            confidence=0.0,
        )
    )

    assert receipt.confidence == 0.0


def test_accepted_receipt_preserves_all_identity_fields() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            sequence=9,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            confidence=0.61,
        )
    )

    assert receipt.sequence == 9
    assert receipt.diagnostic_code == "RUN_SYNC_MISMATCH"
    assert receipt.action == "Retry synchronization."
    assert receipt.confidence == 0.61


def test_rejected_receipt_preserves_sequence() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            sequence=4,
            state=DispatchState.REJECTED,
            dispatched=False,
        )
    )

    assert receipt.sequence == 4


def test_manual_receipt_preserves_sequence() -> None:
    receipt = Receipt.from_dispatch(
        dispatch(
            sequence=5,
            state=DispatchState.MANUAL,
            dispatched=False,
        )
    )

    assert receipt.sequence == 5
