import importlib

decision_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_decision"
)
executor_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_executor"
)

Decision = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecision
)
DecisionState = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecisionState
)
Executor = (
    executor_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecutor
)
ExecutionState = (
    executor_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecutionState
)


def decision(
    *,
    state: DecisionState,
    code: str,
    execute: bool,
    reason: str,
    action: str,
) -> Decision:
    return Decision(
        state=state,
        diagnostic_code=code,
        execute=execute,
        reason=reason,
        action=action,
    )


def test_executor_starts_empty() -> None:
    executor = Executor()

    assert executor.execution_count == 0
    assert executor.latest is None
    assert not executor.has_executions


def test_skip_produces_skipped_execution() -> None:
    executor = Executor()

    execution = executor.execute(
        decision(
            state=DecisionState.SKIP,
            code="RUN_HEALTHY",
            execute=False,
            reason="Recovery is not required.",
            action="No recovery required.",
        )
    )

    assert execution.state is ExecutionState.SKIPPED


def test_skip_does_not_execute_action() -> None:
    executor = Executor()

    execution = executor.execute(
        decision(
            state=DecisionState.SKIP,
            code="RUN_HEALTHY",
            execute=False,
            reason="Recovery is not required.",
            action="No recovery required.",
        )
    )

    assert not execution.executed


def test_retry_produces_executed_execution() -> None:
    executor = Executor()

    execution = executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )

    assert execution.state is ExecutionState.EXECUTED


def test_retry_executes_action() -> None:
    executor = Executor()

    execution = executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )

    assert execution.executed


def test_hold_produces_blocked_execution() -> None:
    executor = Executor()

    execution = executor.execute(
        decision(
            state=DecisionState.HOLD,
            code="RUN_MANUAL_RECOVERY",
            execute=False,
            reason="Recovery requires manual intervention.",
            action="Inspect runtime manually.",
        )
    )

    assert execution.state is ExecutionState.BLOCKED


def test_hold_does_not_execute_action() -> None:
    executor = Executor()

    execution = executor.execute(
        decision(
            state=DecisionState.HOLD,
            code="RUN_MANUAL_RECOVERY",
            execute=False,
            reason="Recovery requires manual intervention.",
            action="Inspect runtime manually.",
        )
    )

    assert not execution.executed


def test_first_execution_has_sequence_one() -> None:
    executor = Executor()

    execution = executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )

    assert execution.sequence == 1
    assert executor.execution_count == 1


def test_multiple_executions_increment_sequence() -> None:
    executor = Executor()

    first = executor.execute(
        decision(
            state=DecisionState.SKIP,
            code="RUN_HEALTHY",
            execute=False,
            reason="Recovery is not required.",
            action="No recovery required.",
        )
    )
    second = executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )
    third = executor.execute(
        decision(
            state=DecisionState.HOLD,
            code="RUN_MANUAL_RECOVERY",
            execute=False,
            reason="Recovery requires manual intervention.",
            action="Inspect runtime manually.",
        )
    )

    assert first.sequence == 1
    assert second.sequence == 2
    assert third.sequence == 3
    assert executor.execution_count == 3


def test_latest_tracks_last_execution() -> None:
    executor = Executor()

    executor.execute(
        decision(
            state=DecisionState.SKIP,
            code="RUN_HEALTHY",
            execute=False,
            reason="Recovery is not required.",
            action="No recovery required.",
        )
    )
    latest = executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )

    assert executor.latest is latest
    assert executor.has_executions


def test_execution_preserves_diagnostic_code() -> None:
    executor = Executor()

    execution = executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )

    assert execution.diagnostic_code == "RUN_SYNC_MISMATCH"


def test_execution_preserves_action() -> None:
    executor = Executor()

    execution = executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )

    assert execution.action == "Retry synchronization."


def test_reset_clears_execution_count() -> None:
    executor = Executor()

    executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )
    executor.reset()

    assert executor.execution_count == 0


def test_reset_clears_latest_execution() -> None:
    executor = Executor()

    executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )
    executor.reset()

    assert executor.latest is None
    assert not executor.has_executions


def test_execution_restarts_at_one_after_reset() -> None:
    executor = Executor()

    executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )
    executor.reset()

    execution = executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )

    assert execution.sequence == 1


def test_previous_execution_remains_snapshot() -> None:
    executor = Executor()

    first = executor.execute(
        decision(
            state=DecisionState.SKIP,
            code="RUN_HEALTHY",
            execute=False,
            reason="Recovery is not required.",
            action="No recovery required.",
        )
    )

    executor.execute(
        decision(
            state=DecisionState.RETRY,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            reason="Recovery retry is permitted.",
            action="Retry synchronization.",
        )
    )

    assert first.sequence == 1
    assert first.state is ExecutionState.SKIPPED
    assert not first.executed
