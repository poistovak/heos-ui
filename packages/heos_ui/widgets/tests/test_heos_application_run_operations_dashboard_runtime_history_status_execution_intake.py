import importlib

delivery_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_delivery"
)
intake_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_intake"
)

Delivery = (
    delivery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDelivery
)
DeliveryState = (
    delivery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDeliveryState
)
Intake = (
    intake_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntake
)
IntakeState = (
    intake_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntakeState
)


def delivery(
    *,
    sequence: int = 1,
    state: DeliveryState = DeliveryState.DELIVERED,
    code: str = "RUN_SYNC_MISMATCH",
    action: str = "Retry synchronization.",
    delivered: bool = True,
    confidence: float = 0.75,
) -> Delivery:
    return Delivery(
        sequence=sequence,
        state=state,
        diagnostic_code=code,
        action=action,
        delivered=delivered,
        confidence=confidence,
        reason="delivery",
    )


def test_delivered_command_is_accepted() -> None:
    intake = Intake.from_delivery(
        delivery()
    )

    assert intake.state is IntakeState.ACCEPTED


def test_accepted_intake_sets_accepted_true() -> None:
    intake = Intake.from_delivery(
        delivery()
    )

    assert intake.accepted


def test_accepted_intake_has_reason() -> None:
    intake = Intake.from_delivery(
        delivery()
    )

    assert intake.reason == (
        "Recovery delivery was accepted for execution."
    )


def test_failed_delivery_is_rejected() -> None:
    intake = Intake.from_delivery(
        delivery(
            state=DeliveryState.FAILED,
            delivered=False,
        )
    )

    assert intake.state is IntakeState.REJECTED


def test_rejected_intake_is_not_accepted() -> None:
    intake = Intake.from_delivery(
        delivery(
            state=DeliveryState.FAILED,
            delivered=False,
        )
    )

    assert not intake.accepted


def test_rejected_intake_has_reason() -> None:
    intake = Intake.from_delivery(
        delivery(
            state=DeliveryState.FAILED,
            delivered=False,
        )
    )

    assert intake.reason == (
        "Recovery delivery was rejected by execution intake."
    )


def test_manual_delivery_remains_manual() -> None:
    intake = Intake.from_delivery(
        delivery(
            state=DeliveryState.MANUAL,
            delivered=False,
        )
    )

    assert intake.state is IntakeState.MANUAL


def test_manual_intake_is_not_accepted() -> None:
    intake = Intake.from_delivery(
        delivery(
            state=DeliveryState.MANUAL,
            delivered=False,
        )
    )

    assert not intake.accepted


def test_manual_intake_has_reason() -> None:
    intake = Intake.from_delivery(
        delivery(
            state=DeliveryState.MANUAL,
            delivered=False,
        )
    )

    assert intake.reason == (
        "Recovery execution intake requires manual handling."
    )


def test_intake_preserves_sequence() -> None:
    intake = Intake.from_delivery(
        delivery(sequence=12)
    )

    assert intake.sequence == 12


def test_intake_preserves_diagnostic_code() -> None:
    intake = Intake.from_delivery(
        delivery(
            code="RUN_STATUS_COUNT_MISMATCH",
        )
    )

    assert intake.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_intake_preserves_action() -> None:
    intake = Intake.from_delivery(
        delivery(
            action="Retry status generation.",
        )
    )

    assert intake.action == "Retry status generation."


def test_intake_preserves_confidence() -> None:
    intake = Intake.from_delivery(
        delivery(
            confidence=0.91,
        )
    )

    assert intake.confidence == 0.91


def test_zero_confidence_is_preserved() -> None:
    intake = Intake.from_delivery(
        delivery(
            confidence=0.0,
        )
    )

    assert intake.confidence == 0.0


def test_accepted_snapshot_preserves_identity() -> None:
    intake = Intake.from_delivery(
        delivery(
            sequence=8,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            confidence=0.64,
        )
    )

    assert intake.sequence == 8
    assert intake.diagnostic_code == "RUN_SYNC_MISMATCH"
    assert intake.action == "Retry synchronization."
    assert intake.confidence == 0.64


def test_rejected_intake_preserves_sequence() -> None:
    intake = Intake.from_delivery(
        delivery(
            sequence=4,
            state=DeliveryState.FAILED,
            delivered=False,
        )
    )

    assert intake.sequence == 4


def test_manual_intake_preserves_sequence() -> None:
    intake = Intake.from_delivery(
        delivery(
            sequence=5,
            state=DeliveryState.MANUAL,
            delivered=False,
        )
    )

    assert intake.sequence == 5
