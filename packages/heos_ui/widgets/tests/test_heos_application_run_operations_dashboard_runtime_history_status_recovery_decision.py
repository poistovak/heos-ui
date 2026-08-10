import importlib

decision_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_decision"
)
recovery_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_plan"
)

Decision = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecision
)
DecisionState = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecisionState
)
Plan = (
    recovery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPlan
)
Priority = (
    recovery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPriority
)


def recovery_plan(
    *,
    code: str,
    required: bool,
    retryable: bool,
    priority: Priority,
    action: str,
) -> Plan:
    return Plan(
        diagnostic_code=code,
        required=required,
        retryable=retryable,
        priority=priority,
        action=action,
    )


def test_healthy_plan_is_skipped() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_HEALTHY",
            required=False,
            retryable=False,
            priority=Priority.NONE,
            action="No recovery required.",
        )
    )

    assert decision.state is DecisionState.SKIP


def test_skipped_plan_is_not_executed() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_HEALTHY",
            required=False,
            retryable=False,
            priority=Priority.NONE,
            action="No recovery required.",
        )
    )

    assert not decision.execute


def test_skipped_plan_has_reason() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_HEALTHY",
            required=False,
            retryable=False,
            priority=Priority.NONE,
            action="No recovery required.",
        )
    )

    assert decision.reason == "Recovery is not required."


def test_empty_plan_is_skipped() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_EMPTY",
            required=False,
            retryable=False,
            priority=Priority.NONE,
            action="No recovery required.",
        )
    )

    assert decision.state is DecisionState.SKIP
    assert not decision.execute


def test_sync_mismatch_is_retry() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_SYNC_MISMATCH",
            required=True,
            retryable=True,
            priority=Priority.HIGH,
            action="Retry synchronization.",
        )
    )

    assert decision.state is DecisionState.RETRY


def test_sync_mismatch_retry_is_executable() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_SYNC_MISMATCH",
            required=True,
            retryable=True,
            priority=Priority.HIGH,
            action="Retry synchronization.",
        )
    )

    assert decision.execute


def test_sync_mismatch_retry_has_reason() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_SYNC_MISMATCH",
            required=True,
            retryable=True,
            priority=Priority.HIGH,
            action="Retry synchronization.",
        )
    )

    assert decision.reason == "Recovery retry is permitted."


def test_status_mismatch_is_retry() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_STATUS_COUNT_MISMATCH",
            required=True,
            retryable=True,
            priority=Priority.NORMAL,
            action="Retry status generation.",
        )
    )

    assert decision.state is DecisionState.RETRY
    assert decision.execute


def test_non_retryable_recovery_is_held() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_MANUAL_RECOVERY",
            required=True,
            retryable=False,
            priority=Priority.HIGH,
            action="Inspect runtime manually.",
        )
    )

    assert decision.state is DecisionState.HOLD


def test_held_recovery_is_not_executed() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_MANUAL_RECOVERY",
            required=True,
            retryable=False,
            priority=Priority.HIGH,
            action="Inspect runtime manually.",
        )
    )

    assert not decision.execute


def test_held_recovery_has_reason() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_MANUAL_RECOVERY",
            required=True,
            retryable=False,
            priority=Priority.HIGH,
            action="Inspect runtime manually.",
        )
    )

    assert decision.reason == "Recovery requires manual intervention."


def test_decision_preserves_diagnostic_code() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_SYNC_MISMATCH",
            required=True,
            retryable=True,
            priority=Priority.HIGH,
            action="Retry synchronization.",
        )
    )

    assert decision.diagnostic_code == "RUN_SYNC_MISMATCH"


def test_decision_preserves_action() -> None:
    action = "Retry synchronization."

    decision = Decision.decide(
        recovery_plan(
            code="RUN_SYNC_MISMATCH",
            required=True,
            retryable=True,
            priority=Priority.HIGH,
            action=action,
        )
    )

    assert decision.action == action


def test_normal_priority_retry_is_permitted() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_STATUS_COUNT_MISMATCH",
            required=True,
            retryable=True,
            priority=Priority.NORMAL,
            action="Retry status generation.",
        )
    )

    assert decision.state is DecisionState.RETRY
    assert decision.execute


def test_high_priority_retry_is_permitted() -> None:
    decision = Decision.decide(
        recovery_plan(
            code="RUN_SYNC_MISMATCH",
            required=True,
            retryable=True,
            priority=Priority.HIGH,
            action="Retry synchronization.",
        )
    )

    assert decision.state is DecisionState.RETRY
    assert decision.execute


def test_decision_is_stable_snapshot() -> None:
    plan = recovery_plan(
        code="RUN_SYNC_MISMATCH",
        required=True,
        retryable=True,
        priority=Priority.HIGH,
        action="Retry synchronization.",
    )

    decision = Decision.decide(plan)

    assert decision.state is DecisionState.RETRY
    assert decision.execute
    assert decision.diagnostic_code == "RUN_SYNC_MISMATCH"
    assert decision.action == "Retry synchronization."
