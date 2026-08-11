import importlib

request_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_request"
)
start_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_start"
)

Request = (
    request_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequest
)
RequestState = (
    request_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionRequestState
)
Start = (
    start_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStart
)
StartState = (
    start_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStartState
)


def request(
    *,
    sequence: int = 1,
    state: RequestState = RequestState.READY,
    code: str = "RUN_SYNC_MISMATCH",
    action: str = "Retry synchronization.",
    executable: bool = True,
    confidence: float = 0.75,
) -> Request:
    return Request(
        sequence=sequence,
        state=state,
        diagnostic_code=code,
        action=action,
        executable=executable,
        confidence=confidence,
        reason="request",
    )


def test_ready_request_starts_execution() -> None:
    start = Start.from_request(
        request()
    )

    assert start.state is StartState.STARTED


def test_started_execution_sets_started_true() -> None:
    start = Start.from_request(
        request()
    )

    assert start.started


def test_started_execution_has_reason() -> None:
    start = Start.from_request(
        request()
    )

    assert start.reason == "Recovery execution was started."


def test_rejected_request_is_blocked() -> None:
    start = Start.from_request(
        request(
            state=RequestState.REJECTED,
            executable=False,
        )
    )

    assert start.state is StartState.BLOCKED


def test_blocked_execution_is_not_started() -> None:
    start = Start.from_request(
        request(
            state=RequestState.REJECTED,
            executable=False,
        )
    )

    assert not start.started


def test_blocked_execution_has_reason() -> None:
    start = Start.from_request(
        request(
            state=RequestState.REJECTED,
            executable=False,
        )
    )

    assert start.reason == "Recovery execution start was blocked."


def test_manual_request_remains_manual() -> None:
    start = Start.from_request(
        request(
            state=RequestState.MANUAL,
            executable=False,
        )
    )

    assert start.state is StartState.MANUAL


def test_manual_execution_is_not_started() -> None:
    start = Start.from_request(
        request(
            state=RequestState.MANUAL,
            executable=False,
        )
    )

    assert not start.started


def test_manual_execution_has_reason() -> None:
    start = Start.from_request(
        request(
            state=RequestState.MANUAL,
            executable=False,
        )
    )

    assert start.reason == (
        "Recovery execution start requires manual handling."
    )


def test_ready_but_non_executable_request_is_blocked() -> None:
    start = Start.from_request(
        request(
            state=RequestState.READY,
            executable=False,
        )
    )

    assert start.state is StartState.BLOCKED
    assert not start.started


def test_start_preserves_sequence() -> None:
    start = Start.from_request(
        request(sequence=14)
    )

    assert start.sequence == 14


def test_start_preserves_diagnostic_code() -> None:
    start = Start.from_request(
        request(
            code="RUN_STATUS_COUNT_MISMATCH",
        )
    )

    assert start.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_start_preserves_action() -> None:
    start = Start.from_request(
        request(
            action="Retry status generation.",
        )
    )

    assert start.action == "Retry status generation."


def test_start_preserves_confidence() -> None:
    start = Start.from_request(
        request(
            confidence=0.93,
        )
    )

    assert start.confidence == 0.93


def test_zero_confidence_can_start() -> None:
    start = Start.from_request(
        request(
            confidence=0.0,
        )
    )

    assert start.state is StartState.STARTED
    assert start.started
    assert start.confidence == 0.0


def test_started_snapshot_preserves_identity() -> None:
    start = Start.from_request(
        request(
            sequence=10,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            confidence=0.67,
        )
    )

    assert start.sequence == 10
    assert start.diagnostic_code == "RUN_SYNC_MISMATCH"
    assert start.action == "Retry synchronization."
    assert start.confidence == 0.67


def test_manual_start_preserves_sequence() -> None:
    start = Start.from_request(
        request(
            sequence=5,
            state=RequestState.MANUAL,
            executable=False,
        )
    )

    assert start.sequence == 5
