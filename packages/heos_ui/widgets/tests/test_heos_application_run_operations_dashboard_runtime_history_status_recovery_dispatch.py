import importlib

command_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_command"
)
dispatch_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_dispatch"
)

Command = (
    command_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommand
)
CommandState = (
    command_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommandState
)
Dispatcher = (
    dispatch_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatcher
)
DispatchState = (
    dispatch_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDispatchState
)


def command(
    *,
    state: CommandState = CommandState.READY,
    code: str = "RUN_SYNC_MISMATCH",
    action: str = "Retry synchronization.",
    executable: bool = True,
    confidence: float = 0.75,
) -> Command:
    return Command(
        state=state,
        diagnostic_code=code,
        action=action,
        executable=executable,
        confidence=confidence,
        reason="command",
    )


def test_dispatcher_starts_empty() -> None:
    dispatcher = Dispatcher()

    assert dispatcher.dispatch_count == 0
    assert dispatcher.latest is None
    assert not dispatcher.has_dispatches


def test_ready_command_is_dispatched() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command()
    )

    assert result.state is DispatchState.DISPATCHED


def test_dispatched_command_sets_dispatched_true() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command()
    )

    assert result.dispatched


def test_dispatched_command_has_reason() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command()
    )

    assert result.reason == "Recovery command was dispatched."


def test_blocked_command_is_rejected() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command(
            state=CommandState.BLOCKED,
            executable=False,
        )
    )

    assert result.state is DispatchState.REJECTED


def test_rejected_command_is_not_dispatched() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command(
            state=CommandState.BLOCKED,
            executable=False,
        )
    )

    assert not result.dispatched


def test_rejected_command_has_reason() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command(
            state=CommandState.BLOCKED,
            executable=False,
        )
    )

    assert result.reason == (
        "Recovery command was rejected by dispatcher."
    )


def test_manual_command_remains_manual() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command(
            state=CommandState.MANUAL,
            executable=False,
        )
    )

    assert result.state is DispatchState.MANUAL


def test_manual_command_is_not_dispatched() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command(
            state=CommandState.MANUAL,
            executable=False,
        )
    )

    assert not result.dispatched


def test_manual_command_has_reason() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command(
            state=CommandState.MANUAL,
            executable=False,
        )
    )

    assert result.reason == (
        "Recovery command requires manual dispatch."
    )


def test_non_executable_ready_command_is_rejected() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command(
            state=CommandState.READY,
            executable=False,
        )
    )

    assert result.state is DispatchState.REJECTED
    assert not result.dispatched


def test_first_dispatch_has_sequence_one() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command()
    )

    assert result.sequence == 1
    assert dispatcher.dispatch_count == 1


def test_multiple_dispatches_increment_sequence() -> None:
    dispatcher = Dispatcher()

    first = dispatcher.dispatch(
        command()
    )
    second = dispatcher.dispatch(
        command(
            state=CommandState.BLOCKED,
            executable=False,
        )
    )

    assert first.sequence == 1
    assert second.sequence == 2
    assert dispatcher.dispatch_count == 2


def test_latest_tracks_last_dispatch() -> None:
    dispatcher = Dispatcher()

    dispatcher.dispatch(
        command()
    )
    latest = dispatcher.dispatch(
        command(
            state=CommandState.BLOCKED,
            executable=False,
        )
    )

    assert dispatcher.latest is latest
    assert dispatcher.has_dispatches


def test_dispatch_preserves_diagnostic_code() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command(
            code="RUN_STATUS_COUNT_MISMATCH",
        )
    )

    assert result.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_dispatch_preserves_action() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command(
            action="Retry status generation.",
        )
    )

    assert result.action == "Retry status generation."


def test_dispatch_preserves_confidence() -> None:
    dispatcher = Dispatcher()

    result = dispatcher.dispatch(
        command(
            confidence=0.83,
        )
    )

    assert result.confidence == 0.83


def test_reset_clears_dispatcher() -> None:
    dispatcher = Dispatcher()

    dispatcher.dispatch(
        command()
    )
    dispatcher.reset()

    assert dispatcher.dispatch_count == 0
    assert dispatcher.latest is None
    assert not dispatcher.has_dispatches


def test_dispatch_restarts_at_one_after_reset() -> None:
    dispatcher = Dispatcher()

    dispatcher.dispatch(
        command()
    )
    dispatcher.reset()

    result = dispatcher.dispatch(
        command()
    )

    assert result.sequence == 1


def test_previous_dispatch_remains_snapshot() -> None:
    dispatcher = Dispatcher()

    first = dispatcher.dispatch(
        command()
    )

    dispatcher.dispatch(
        command(
            state=CommandState.BLOCKED,
            executable=False,
        )
    )

    assert first.sequence == 1
    assert first.state is DispatchState.DISPATCHED
    assert first.dispatched
