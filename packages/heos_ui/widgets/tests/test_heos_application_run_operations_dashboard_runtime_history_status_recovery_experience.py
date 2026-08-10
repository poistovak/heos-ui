import importlib

experience_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_experience"
)
feedback_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_feedback"
)
store_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_feedback_store"
)

Experience = (
    experience_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExperience
)
Feedback = (
    feedback_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedback
)
FeedbackState = (
    feedback_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackState
)
Store = (
    store_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackStore
)


def feedback(
    *,
    sequence: int = 1,
    state: FeedbackState,
    code: str = "RUN_SYNC_MISMATCH",
    learned: bool = True,
    retry_recommended: bool = False,
) -> Feedback:
    return Feedback(
        sequence=sequence,
        state=state,
        diagnostic_code=code,
        learned=learned,
        retry_recommended=retry_recommended,
        message="feedback",
    )


def test_empty_store_produces_empty_experience() -> None:
    experience = Experience.from_store(
        Store(),
        "RUN_SYNC_MISMATCH",
    )

    assert experience.empty
    assert experience.observations == 0


def test_empty_experience_has_no_success_rate() -> None:
    experience = Experience.from_store(
        Store(),
        "RUN_SYNC_MISMATCH",
    )

    assert experience.success_rate is None


def test_empty_experience_does_not_support_retry() -> None:
    experience = Experience.from_store(
        Store(),
        "RUN_SYNC_MISMATCH",
    )

    assert not experience.retry_supported


def test_positive_feedback_is_counted() -> None:
    store = Store()
    store.append(
        feedback(
            state=FeedbackState.POSITIVE,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    assert experience.observations == 1
    assert experience.positive == 1


def test_negative_feedback_is_counted() -> None:
    store = Store()
    store.append(
        feedback(
            state=FeedbackState.NEGATIVE,
            retry_recommended=True,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    assert experience.observations == 1
    assert experience.negative == 1


def test_manual_feedback_is_counted() -> None:
    store = Store()
    store.append(
        feedback(
            state=FeedbackState.MANUAL,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    assert experience.observations == 1
    assert experience.manual == 1


def test_none_feedback_is_not_learned() -> None:
    store = Store()
    store.append(
        feedback(
            state=FeedbackState.NONE,
            code="RUN_HEALTHY",
            learned=False,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_HEALTHY",
    )

    assert experience.empty


def test_success_rate_is_one_for_only_successes() -> None:
    store = Store()
    store.append(
        feedback(
            sequence=1,
            state=FeedbackState.POSITIVE,
        )
    )
    store.append(
        feedback(
            sequence=2,
            state=FeedbackState.POSITIVE,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    assert experience.success_rate == 1.0


def test_success_rate_is_zero_for_only_failures() -> None:
    store = Store()
    store.append(
        feedback(
            state=FeedbackState.NEGATIVE,
            retry_recommended=True,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    assert experience.success_rate == 0.0


def test_success_rate_combines_success_and_failure() -> None:
    store = Store()
    store.append(
        feedback(
            sequence=1,
            state=FeedbackState.POSITIVE,
        )
    )
    store.append(
        feedback(
            sequence=2,
            state=FeedbackState.NEGATIVE,
            retry_recommended=True,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    assert experience.success_rate == 0.5


def test_manual_feedback_is_excluded_from_success_rate() -> None:
    store = Store()
    store.append(
        feedback(
            sequence=1,
            state=FeedbackState.POSITIVE,
        )
    )
    store.append(
        feedback(
            sequence=2,
            state=FeedbackState.MANUAL,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    assert experience.success_rate == 1.0


def test_negative_feedback_can_support_retry() -> None:
    store = Store()
    store.append(
        feedback(
            state=FeedbackState.NEGATIVE,
            retry_recommended=True,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    assert experience.retry_supported


def test_negative_without_recommendation_does_not_support_retry() -> None:
    store = Store()
    store.append(
        feedback(
            state=FeedbackState.NEGATIVE,
            retry_recommended=False,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    assert not experience.retry_supported


def test_manual_feedback_blocks_retry_support() -> None:
    store = Store()
    store.append(
        feedback(
            sequence=1,
            state=FeedbackState.NEGATIVE,
            retry_recommended=True,
        )
    )
    store.append(
        feedback(
            sequence=2,
            state=FeedbackState.MANUAL,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    assert not experience.retry_supported


def test_experience_filters_by_diagnostic_code() -> None:
    store = Store()
    store.append(
        feedback(
            sequence=1,
            state=FeedbackState.POSITIVE,
            code="RUN_SYNC_MISMATCH",
        )
    )
    store.append(
        feedback(
            sequence=2,
            state=FeedbackState.NEGATIVE,
            code="RUN_STATUS_COUNT_MISMATCH",
            retry_recommended=True,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    assert experience.observations == 1
    assert experience.positive == 1
    assert experience.negative == 0


def test_experience_preserves_diagnostic_code() -> None:
    experience = Experience.from_store(
        Store(),
        "RUN_STATUS_COUNT_MISMATCH",
    )

    assert experience.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_experience_is_snapshot_of_store() -> None:
    store = Store()
    store.append(
        feedback(
            state=FeedbackState.POSITIVE,
        )
    )

    experience = Experience.from_store(
        store,
        "RUN_SYNC_MISMATCH",
    )

    store.append(
        feedback(
            sequence=2,
            state=FeedbackState.NEGATIVE,
            retry_recommended=True,
        )
    )

    assert experience.observations == 1
    assert experience.positive == 1
    assert experience.negative == 0
    assert experience.success_rate == 1.0
