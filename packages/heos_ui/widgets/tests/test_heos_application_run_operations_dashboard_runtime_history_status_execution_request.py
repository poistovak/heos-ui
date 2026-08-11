import importlib

intake_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_intake"
)
request_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_request"
)

Intake = (
    intake_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntake
)
IntakeState = (
    intake_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionIntakeState
)
Request = (
    request_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequest
)
RequestState = (
    request_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequestState
)


def intake(
    *,
    sequence: int = 1,
    state: IntakeState = IntakeState.ACCEPTED,
    code: str = "RUN_SYNC_MISMATCH",
    action: str = "Retry synchronization.",
    accepted: bool = True,
    confidence: float = 0.75,
) -> Intake:
    return Intake(
        sequence=sequence,
        state=state,
        diagnostic_code=code,
        action=action,
        accepted=accepted,
        confidence=confidence,
        reason="intake",
    )


def test_accepted_intake_builds_ready_request() -> None:
    request = Request.from_intake(
        intake()
    )

    assert request.state is RequestState.READY


def test_ready_request_is_executable() -> None:
    request = Request.from_intake(
        intake()
    )

    assert request.executable


def test_ready_request_has_reason() -> None:
    request = Request.from_intake(
        intake()
    )

    assert request.reason == "Recovery execution request is ready."


def test_rejected_intake_builds_rejected_request() -> None:
    request = Request.from_intake(
        intake(
            state=IntakeState.REJECTED,
            accepted=False,
        )
    )

    assert request.state is RequestState.REJECTED


def test_rejected_request_is_not_executable() -> None:
    request = Request.from_intake(
        intake(
            state=IntakeState.REJECTED,
            accepted=False,
        )
    )

    assert not request.executable


def test_rejected_request_has_reason() -> None:
    request = Request.from_intake(
        intake(
            state=IntakeState.REJECTED,
            accepted=False,
        )
    )

    assert request.reason == "Recovery execution request was rejected."


def test_manual_intake_builds_manual_request() -> None:
    request = Request.from_intake(
        intake(
            state=IntakeState.MANUAL,
            accepted=False,
        )
    )

    assert request.state is RequestState.MANUAL


def test_manual_request_is_not_executable() -> None:
    request = Request.from_intake(
        intake(
            state=IntakeState.MANUAL,
            accepted=False,
        )
    )

    assert not request.executable


def test_manual_request_has_reason() -> None:
    request = Request.from_intake(
        intake(
            state=IntakeState.MANUAL,
            accepted=False,
        )
    )

    assert request.reason == (
        "Recovery execution request requires manual handling."
    )


def test_request_preserves_sequence() -> None:
    request = Request.from_intake(
        intake(sequence=13)
    )

    assert request.sequence == 13


def test_request_preserves_diagnostic_code() -> None:
    request = Request.from_intake(
        intake(
            code="RUN_STATUS_COUNT_MISMATCH",
        )
    )

    assert request.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_request_preserves_action() -> None:
    request = Request.from_intake(
        intake(
            action="Retry status generation.",
        )
    )

    assert request.action == "Retry status generation."


def test_request_preserves_confidence() -> None:
    request = Request.from_intake(
        intake(
            confidence=0.92,
        )
    )

    assert request.confidence == 0.92


def test_zero_confidence_is_preserved() -> None:
    request = Request.from_intake(
        intake(
            confidence=0.0,
        )
    )

    assert request.confidence == 0.0


def test_ready_snapshot_preserves_identity() -> None:
    request = Request.from_intake(
        intake(
            sequence=9,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            confidence=0.66,
        )
    )

    assert request.sequence == 9
    assert request.diagnostic_code == "RUN_SYNC_MISMATCH"
    assert request.action == "Retry synchronization."
    assert request.confidence == 0.66


def test_rejected_request_preserves_sequence() -> None:
    request = Request.from_intake(
        intake(
            sequence=4,
            state=IntakeState.REJECTED,
            accepted=False,
        )
    )

    assert request.sequence == 4


def test_manual_request_preserves_sequence() -> None:
    request = Request.from_intake(
        intake(
            sequence=5,
            state=IntakeState.MANUAL,
            accepted=False,
        )
    )

    assert request.sequence == 5
