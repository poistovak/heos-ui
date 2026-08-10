import importlib

diagnostic_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "run_diagnostic"
)
recovery_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_plan"
)

Diagnostic = (
    diagnostic_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunDiagnostic
)
DiagnosticSeverity = (
    diagnostic_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDiagnosticSeverity
)
Plan = (
    recovery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPlan
)
Priority = (
    recovery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPriority
)


def diagnostic(
    *,
    code: str,
    healthy: bool,
    message: str,
    action: str,
    severity: DiagnosticSeverity,
) -> Diagnostic:
    return Diagnostic(
        code=code,
        severity=severity,
        message=message,
        action=action,
        healthy=healthy,
    )


def test_healthy_run_requires_no_recovery() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_HEALTHY",
            healthy=True,
            message="Runtime history status run is healthy.",
            action="No action required.",
            severity=DiagnosticSeverity.SUCCESS,
        )
    )

    assert not plan.required


def test_healthy_run_is_not_retryable() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_HEALTHY",
            healthy=True,
            message="Runtime history status run is healthy.",
            action="No action required.",
            severity=DiagnosticSeverity.SUCCESS,
        )
    )

    assert not plan.retryable


def test_healthy_run_has_no_priority() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_HEALTHY",
            healthy=True,
            message="Runtime history status run is healthy.",
            action="No action required.",
            severity=DiagnosticSeverity.SUCCESS,
        )
    )

    assert plan.priority is Priority.NONE


def test_empty_run_requires_no_recovery() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_EMPTY",
            healthy=True,
            message="Run completed without runtime steps.",
            action="No action required.",
            severity=DiagnosticSeverity.INFO,
        )
    )

    assert not plan.required
    assert not plan.retryable


def test_empty_run_has_no_priority() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_EMPTY",
            healthy=True,
            message="Run completed without runtime steps.",
            action="No action required.",
            severity=DiagnosticSeverity.INFO,
        )
    )

    assert plan.priority is Priority.NONE


def test_sync_mismatch_requires_recovery() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_SYNC_MISMATCH",
            healthy=False,
            message="Runtime and status updates are not synchronized.",
            action="Inspect runtime and status synchronization.",
            severity=DiagnosticSeverity.WARNING,
        )
    )

    assert plan.required


def test_sync_mismatch_is_retryable() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_SYNC_MISMATCH",
            healthy=False,
            message="Runtime and status updates are not synchronized.",
            action="Inspect runtime and status synchronization.",
            severity=DiagnosticSeverity.WARNING,
        )
    )

    assert plan.retryable


def test_sync_mismatch_has_high_priority() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_SYNC_MISMATCH",
            healthy=False,
            message="Runtime and status updates are not synchronized.",
            action="Inspect runtime and status synchronization.",
            severity=DiagnosticSeverity.WARNING,
        )
    )

    assert plan.priority is Priority.HIGH


def test_sync_mismatch_has_retry_action() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_SYNC_MISMATCH",
            healthy=False,
            message="Runtime and status updates are not synchronized.",
            action="Inspect runtime and status synchronization.",
            severity=DiagnosticSeverity.WARNING,
        )
    )

    assert plan.action == (
        "Inspect synchronization and retry the runtime status run."
    )


def test_status_count_mismatch_requires_recovery() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_STATUS_COUNT_MISMATCH",
            healthy=False,
            message="Status update count does not match step count.",
            action="Inspect status update generation.",
            severity=DiagnosticSeverity.WARNING,
        )
    )

    assert plan.required


def test_status_count_mismatch_is_retryable() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_STATUS_COUNT_MISMATCH",
            healthy=False,
            message="Status update count does not match step count.",
            action="Inspect status update generation.",
            severity=DiagnosticSeverity.WARNING,
        )
    )

    assert plan.retryable


def test_status_count_mismatch_has_normal_priority() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_STATUS_COUNT_MISMATCH",
            healthy=False,
            message="Status update count does not match step count.",
            action="Inspect status update generation.",
            severity=DiagnosticSeverity.WARNING,
        )
    )

    assert plan.priority is Priority.NORMAL


def test_status_count_mismatch_has_retry_action() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_STATUS_COUNT_MISMATCH",
            healthy=False,
            message="Status update count does not match step count.",
            action="Inspect status update generation.",
            severity=DiagnosticSeverity.WARNING,
        )
    )

    assert plan.action == (
        "Inspect status update generation and retry the runtime status run."
    )


def test_plan_preserves_diagnostic_code() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_SYNC_MISMATCH",
            healthy=False,
            message="Runtime and status updates are not synchronized.",
            action="Inspect runtime and status synchronization.",
            severity=DiagnosticSeverity.WARNING,
        )
    )

    assert plan.diagnostic_code == "RUN_SYNC_MISMATCH"


def test_no_recovery_action_is_explicit() -> None:
    plan = Plan.from_diagnostic(
        diagnostic(
            code="RUN_HEALTHY",
            healthy=True,
            message="Runtime history status run is healthy.",
            action="No action required.",
            severity=DiagnosticSeverity.SUCCESS,
        )
    )

    assert plan.action == "No recovery required."
