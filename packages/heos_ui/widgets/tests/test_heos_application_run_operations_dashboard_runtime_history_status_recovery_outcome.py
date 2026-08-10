import importlib

import pytest

executor_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_executor"
)
outcome_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_outcome"
)

Execution = (
    executor_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecution
)
ExecutionState = (
    executor_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExecutionState
)
Outcome = (
    outcome_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcome
)
OutcomeState = (
    outcome_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcomeState
)


def execution(
    *,
    sequence: int = 1,
    state: ExecutionState,
    code: str,
    action: str,
    executed: bool,
) -> Execution:
    return Execution(
        sequence=sequence,
        state=state,
        diagnostic_code=code,
        action=action,
        executed=executed,
    )


def test_skipped_execution_is_not_needed() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.SKIPPED,
            code="RUN_HEALTHY",
            action="No recovery required.",
            executed=False,
        )
    )

    assert outcome.state is OutcomeState.NOT_NEEDED


def test_not_needed_outcome_is_successful() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.SKIPPED,
            code="RUN_HEALTHY",
            action="No recovery required.",
            executed=False,
        )
    )

    assert outcome.successful


def test_not_needed_outcome_has_message() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.SKIPPED,
            code="RUN_HEALTHY",
            action="No recovery required.",
            executed=False,
        )
    )

    assert outcome.message == "Recovery was not required."


def test_blocked_execution_produces_blocked_outcome() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.BLOCKED,
            code="RUN_MANUAL_RECOVERY",
            action="Inspect runtime manually.",
            executed=False,
        )
    )

    assert outcome.state is OutcomeState.BLOCKED


def test_blocked_outcome_is_not_successful() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.BLOCKED,
            code="RUN_MANUAL_RECOVERY",
            action="Inspect runtime manually.",
            executed=False,
        )
    )

    assert not outcome.successful


def test_blocked_outcome_has_message() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.BLOCKED,
            code="RUN_MANUAL_RECOVERY",
            action="Inspect runtime manually.",
            executed=False,
        )
    )

    assert outcome.message == "Recovery execution was blocked."


def test_executed_recovery_requires_explicit_outcome() -> None:
    with pytest.raises(
        ValueError,
        match="Executed recovery requires an explicit outcome.",
    ):
        Outcome.from_execution(
            execution(
                state=ExecutionState.EXECUTED,
                code="RUN_SYNC_MISMATCH",
                action="Retry synchronization.",
                executed=True,
            )
        )


def test_successful_execution_produces_success() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.EXECUTED,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            executed=True,
        ),
        succeeded=True,
    )

    assert outcome.state is OutcomeState.SUCCEEDED


def test_successful_execution_is_successful() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.EXECUTED,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            executed=True,
        ),
        succeeded=True,
    )

    assert outcome.successful


def test_successful_execution_has_message() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.EXECUTED,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            executed=True,
        ),
        succeeded=True,
    )

    assert outcome.message == "Recovery execution succeeded."


def test_failed_execution_produces_failure() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.EXECUTED,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            executed=True,
        ),
        succeeded=False,
    )

    assert outcome.state is OutcomeState.FAILED


def test_failed_execution_is_not_successful() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.EXECUTED,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            executed=True,
        ),
        succeeded=False,
    )

    assert not outcome.successful


def test_failed_execution_has_message() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.EXECUTED,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            executed=True,
        ),
        succeeded=False,
    )

    assert outcome.message == "Recovery execution failed."


def test_outcome_preserves_execution_sequence() -> None:
    outcome = Outcome.from_execution(
        execution(
            sequence=7,
            state=ExecutionState.EXECUTED,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            executed=True,
        ),
        succeeded=True,
    )

    assert outcome.sequence == 7


def test_outcome_preserves_diagnostic_code() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.EXECUTED,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            executed=True,
        ),
        succeeded=True,
    )

    assert outcome.diagnostic_code == "RUN_SYNC_MISMATCH"


def test_not_needed_does_not_require_success_argument() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.SKIPPED,
            code="RUN_EMPTY",
            action="No recovery required.",
            executed=False,
        )
    )

    assert outcome.state is OutcomeState.NOT_NEEDED
    assert outcome.successful


def test_blocked_does_not_require_success_argument() -> None:
    outcome = Outcome.from_execution(
        execution(
            state=ExecutionState.BLOCKED,
            code="RUN_MANUAL_RECOVERY",
            action="Inspect runtime manually.",
            executed=False,
        )
    )

    assert outcome.state is OutcomeState.BLOCKED
    assert not outcome.successful
