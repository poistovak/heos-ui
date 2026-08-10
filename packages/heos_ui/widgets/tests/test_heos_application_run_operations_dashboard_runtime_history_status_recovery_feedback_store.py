import importlib

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
    state: FeedbackState = FeedbackState.POSITIVE,
    code: str = "RUN_SYNC_MISMATCH",
    learned: bool = True,
    retry_recommended: bool = False,
    message: str = "feedback",
) -> Feedback:
    return Feedback(
        sequence=sequence,
        state=state,
        diagnostic_code=code,
        learned=learned,
        retry_recommended=retry_recommended,
        message=message,
    )


def test_store_starts_empty() -> None:
    store = Store()

    assert store.empty
    assert store.count == 0


def test_empty_store_has_no_latest() -> None:
    store = Store()

    assert store.latest is None


def test_empty_store_has_empty_history() -> None:
    store = Store()

    assert store.history == ()


def test_append_adds_feedback() -> None:
    store = Store()
    entry = feedback()

    store.append(entry)

    assert store.count == 1
    assert not store.empty


def test_append_sets_latest() -> None:
    store = Store()
    entry = feedback()

    store.append(entry)

    assert store.latest is entry


def test_history_preserves_append_order() -> None:
    store = Store()
    first = feedback(sequence=1)
    second = feedback(sequence=2)

    store.append(first)
    store.append(second)

    assert store.history == (first, second)


def test_latest_tracks_last_feedback() -> None:
    store = Store()
    first = feedback(sequence=1)
    second = feedback(sequence=2)

    store.append(first)
    store.append(second)

    assert store.latest is second


def test_history_is_immutable_tuple() -> None:
    store = Store()
    store.append(feedback())

    assert isinstance(store.history, tuple)


def test_learned_only_returns_learned_feedback() -> None:
    store = Store()
    learned = feedback(
        sequence=1,
        learned=True,
    )
    ignored = feedback(
        sequence=2,
        state=FeedbackState.NONE,
        code="RUN_HEALTHY",
        learned=False,
    )

    store.append(learned)
    store.append(ignored)

    assert store.learned_only == (learned,)


def test_learned_only_is_empty_without_learned_entries() -> None:
    store = Store()
    store.append(
        feedback(
            state=FeedbackState.NONE,
            code="RUN_HEALTHY",
            learned=False,
        )
    )

    assert store.learned_only == ()


def test_by_code_returns_matching_feedback() -> None:
    store = Store()
    first = feedback(
        sequence=1,
        code="RUN_SYNC_MISMATCH",
    )
    second = feedback(
        sequence=2,
        code="RUN_STATUS_COUNT_MISMATCH",
    )
    third = feedback(
        sequence=3,
        code="RUN_SYNC_MISMATCH",
    )

    store.append(first)
    store.append(second)
    store.append(third)

    assert store.by_code("RUN_SYNC_MISMATCH") == (
        first,
        third,
    )


def test_by_code_returns_empty_tuple_for_unknown_code() -> None:
    store = Store()
    store.append(feedback())

    assert store.by_code("UNKNOWN") == ()


def test_clear_removes_all_feedback() -> None:
    store = Store()
    store.append(feedback(sequence=1))
    store.append(feedback(sequence=2))

    store.clear()

    assert store.empty
    assert store.count == 0


def test_clear_removes_latest() -> None:
    store = Store()
    store.append(feedback())

    store.clear()

    assert store.latest is None


def test_clear_removes_history() -> None:
    store = Store()
    store.append(feedback())

    store.clear()

    assert store.history == ()


def test_store_can_accept_feedback_after_clear() -> None:
    store = Store()
    first = feedback(sequence=1)
    second = feedback(sequence=2)

    store.append(first)
    store.clear()
    store.append(second)

    assert store.count == 1
    assert store.latest is second
    assert store.history == (second,)


def test_external_history_snapshot_does_not_change() -> None:
    store = Store()
    first = feedback(sequence=1)

    store.append(first)
    snapshot = store.history

    store.append(
        feedback(sequence=2)
    )

    assert snapshot == (first,)
    assert store.count == 2
