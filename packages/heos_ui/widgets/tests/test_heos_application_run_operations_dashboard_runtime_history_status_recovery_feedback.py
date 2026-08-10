import importlib

feedback_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_feedback"
)
outcome_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_outcome"
)

Feedback = (
    feedback_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedback
)
FeedbackState = (
    feedback_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackState
)
Outcome = (
    outcome_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcome
)
OutcomeState = (
    outcome_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryOutcomeState
)


def outcome(
    *,
    sequence: int = 1,
    state: OutcomeState,
    code: str,
    successful: bool,
    message: str,
) -> Outcome:
    return Outcome(
        sequence=sequence,
        state=state,
        diagnostic_code=code,
        successful=successful,
        message=message,
    )


def test_not_needed_produces_no_feedback() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.NOT_NEEDED,
            code="RUN_HEALTHY",
            successful=True,
            message="Recovery was not required.",
        )
    )

    assert feedback.state is FeedbackState.NONE


def test_not_needed_does_not_learn() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.NOT_NEEDED,
            code="RUN_HEALTHY",
            successful=True,
            message="Recovery was not required.",
        )
    )

    assert not feedback.learned


def test_not_needed_does_not_recommend_retry() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.NOT_NEEDED,
            code="RUN_HEALTHY",
            successful=True,
            message="Recovery was not required.",
        )
    )

    assert not feedback.retry_recommended


def test_success_produces_positive_feedback() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.SUCCEEDED,
            code="RUN_SYNC_MISMATCH",
            successful=True,
            message="Recovery execution succeeded.",
        )
    )

    assert feedback.state is FeedbackState.POSITIVE


def test_success_is_learned() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.SUCCEEDED,
            code="RUN_SYNC_MISMATCH",
            successful=True,
            message="Recovery execution succeeded.",
        )
    )

    assert feedback.learned


def test_success_does_not_recommend_retry() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.SUCCEEDED,
            code="RUN_SYNC_MISMATCH",
            successful=True,
            message="Recovery execution succeeded.",
        )
    )

    assert not feedback.retry_recommended


def test_success_has_positive_message() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.SUCCEEDED,
            code="RUN_SYNC_MISMATCH",
            successful=True,
            message="Recovery execution succeeded.",
        )
    )

    assert feedback.message == (
        "Recovery succeeded and produced positive feedback."
    )


def test_failure_produces_negative_feedback() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.FAILED,
            code="RUN_SYNC_MISMATCH",
            successful=False,
            message="Recovery execution failed.",
        )
    )

    assert feedback.state is FeedbackState.NEGATIVE


def test_failure_is_learned() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.FAILED,
            code="RUN_SYNC_MISMATCH",
            successful=False,
            message="Recovery execution failed.",
        )
    )

    assert feedback.learned


def test_failure_recommends_retry() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.FAILED,
            code="RUN_SYNC_MISMATCH",
            successful=False,
            message="Recovery execution failed.",
        )
    )

    assert feedback.retry_recommended


def test_failure_has_negative_message() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.FAILED,
            code="RUN_SYNC_MISMATCH",
            successful=False,
            message="Recovery execution failed.",
        )
    )

    assert feedback.message == (
        "Recovery failed and requires further evaluation."
    )


def test_blocked_produces_manual_feedback() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.BLOCKED,
            code="RUN_MANUAL_RECOVERY",
            successful=False,
            message="Recovery execution was blocked.",
        )
    )

    assert feedback.state is FeedbackState.MANUAL


def test_blocked_is_learned() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.BLOCKED,
            code="RUN_MANUAL_RECOVERY",
            successful=False,
            message="Recovery execution was blocked.",
        )
    )

    assert feedback.learned


def test_blocked_does_not_recommend_retry() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.BLOCKED,
            code="RUN_MANUAL_RECOVERY",
            successful=False,
            message="Recovery execution was blocked.",
        )
    )

    assert not feedback.retry_recommended


def test_blocked_requires_manual_intervention() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.BLOCKED,
            code="RUN_MANUAL_RECOVERY",
            successful=False,
            message="Recovery execution was blocked.",
        )
    )

    assert feedback.message == (
        "Recovery was blocked and requires manual intervention."
    )


def test_feedback_preserves_sequence() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            sequence=9,
            state=OutcomeState.SUCCEEDED,
            code="RUN_SYNC_MISMATCH",
            successful=True,
            message="Recovery execution succeeded.",
        )
    )

    assert feedback.sequence == 9


def test_feedback_preserves_diagnostic_code() -> None:
    feedback = Feedback.from_outcome(
        outcome(
            state=OutcomeState.FAILED,
            code="RUN_STATUS_COUNT_MISMATCH",
            successful=False,
            message="Recovery execution failed.",
        )
    )

    assert feedback.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"
