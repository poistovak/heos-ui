import importlib

completion_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_completion"
)
start_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_start"
)

Completion = (
    completion_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletion
)
CompletionState = (
    completion_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletionState
)
Start = (
    start_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStart
)
StartState = (
    start_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionStartState
)


def start(
    *,
    sequence: int = 1,
    state: StartState = StartState.STARTED,
    code: str = "RUN_SYNC_MISMATCH",
    action: str = "Retry synchronization.",
    started: bool = True,
    confidence: float = 0.75,
) -> Start:
    return Start(
        sequence=sequence,
        state=state,
        diagnostic_code=code,
        action=action,
        started=started,
        confidence=confidence,
        reason="start",
    )


def test_started_execution_becomes_completed() -> None:
    completion = Completion.from_start(
        start()
    )

    assert completion.state is CompletionState.COMPLETED


def test_completed_execution_sets_completed_true() -> None:
    completion = Completion.from_start(
        start()
    )

    assert completion.completed


def test_completed_execution_has_reason() -> None:
    completion = Completion.from_start(
        start()
    )

    assert completion.reason == "Recovery execution completed."


def test_blocked_start_becomes_not_started() -> None:
    completion = Completion.from_start(
        start(
            state=StartState.BLOCKED,
            started=False,
        )
    )

    assert completion.state is CompletionState.NOT_STARTED


def test_not_started_completion_is_false() -> None:
    completion = Completion.from_start(
        start(
            state=StartState.BLOCKED,
            started=False,
        )
    )

    assert not completion.completed


def test_not_started_has_reason() -> None:
    completion = Completion.from_start(
        start(
            state=StartState.BLOCKED,
            started=False,
        )
    )

    assert completion.reason == "Recovery execution was not started."


def test_manual_start_becomes_manual_completion() -> None:
    completion = Completion.from_start(
        start(
            state=StartState.MANUAL,
            started=False,
        )
    )

    assert completion.state is CompletionState.MANUAL


def test_manual_completion_is_false() -> None:
    completion = Completion.from_start(
        start(
            state=StartState.MANUAL,
            started=False,
        )
    )

    assert not completion.completed


def test_manual_completion_has_reason() -> None:
    completion = Completion.from_start(
        start(
            state=StartState.MANUAL,
            started=False,
        )
    )

    assert completion.reason == (
        "Recovery execution completion requires manual handling."
    )


def test_started_state_without_started_flag_is_not_started() -> None:
    completion = Completion.from_start(
        start(
            state=StartState.STARTED,
            started=False,
        )
    )

    assert completion.state is CompletionState.NOT_STARTED
    assert not completion.completed


def test_completion_preserves_sequence() -> None:
    completion = Completion.from_start(
        start(sequence=15)
    )

    assert completion.sequence == 15


def test_completion_preserves_diagnostic_code() -> None:
    completion = Completion.from_start(
        start(
            code="RUN_STATUS_COUNT_MISMATCH",
        )
    )

    assert completion.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_completion_preserves_action() -> None:
    completion = Completion.from_start(
        start(
            action="Retry status generation.",
        )
    )

    assert completion.action == "Retry status generation."


def test_completion_preserves_confidence() -> None:
    completion = Completion.from_start(
        start(
            confidence=0.94,
        )
    )

    assert completion.confidence == 0.94


def test_zero_confidence_is_preserved() -> None:
    completion = Completion.from_start(
        start(
            confidence=0.0,
        )
    )

    assert completion.confidence == 0.0


def test_completed_snapshot_preserves_identity() -> None:
    completion = Completion.from_start(
        start(
            sequence=11,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            confidence=0.68,
        )
    )

    assert completion.sequence == 11
    assert completion.diagnostic_code == "RUN_SYNC_MISMATCH"
    assert completion.action == "Retry synchronization."
    assert completion.confidence == 0.68


def test_not_started_preserves_sequence() -> None:
    completion = Completion.from_start(
        start(
            sequence=4,
            state=StartState.BLOCKED,
            started=False,
        )
    )

    assert completion.sequence == 4


def test_manual_completion_preserves_sequence() -> None:
    completion = Completion.from_start(
        start(
            sequence=5,
            state=StartState.MANUAL,
            started=False,
        )
    )

    assert completion.sequence == 5
