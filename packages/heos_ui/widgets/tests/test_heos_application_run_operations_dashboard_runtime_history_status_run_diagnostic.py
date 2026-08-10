import importlib
from dataclasses import replace

diagnostic_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "run_diagnostic"
)
health_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "run_health"
)
runner_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "runtime_runner"
)
summary_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "run_summary"
)

Diagnostic = (
    diagnostic_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunDiagnostic
)
Severity = (
    diagnostic_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDiagnosticSeverity
)
Health = (
    health_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealth
)
Runner = (
    runner_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeRunner
)
Summary = (
    summary_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunSummary
)


def running_runner() -> Runner:
    runner = Runner.create()
    runner.start()
    return runner


def health_for(steps: int):
    runner = running_runner()
    summary = Summary.capture(
        runner.run(steps)
    )
    return Health.evaluate(summary)


def test_empty_run_diagnostic_code() -> None:
    diagnostic = Diagnostic.diagnose(
        health_for(0)
    )

    assert diagnostic.code == "RUN_EMPTY"


def test_empty_run_is_info() -> None:
    diagnostic = Diagnostic.diagnose(
        health_for(0)
    )

    assert diagnostic.severity is Severity.INFO
    assert diagnostic.healthy


def test_empty_run_requires_no_action() -> None:
    diagnostic = Diagnostic.diagnose(
        health_for(0)
    )

    assert diagnostic.action == "No action required."


def test_healthy_run_diagnostic_code() -> None:
    diagnostic = Diagnostic.diagnose(
        health_for(2)
    )

    assert diagnostic.code == "RUN_HEALTHY"


def test_healthy_run_is_success() -> None:
    diagnostic = Diagnostic.diagnose(
        health_for(2)
    )

    assert diagnostic.severity is Severity.SUCCESS
    assert diagnostic.healthy


def test_healthy_run_has_message() -> None:
    diagnostic = Diagnostic.diagnose(
        health_for(2)
    )

    assert diagnostic.message == "Runtime history status run is healthy."


def test_healthy_run_requires_no_action() -> None:
    diagnostic = Diagnostic.diagnose(
        health_for(2)
    )

    assert diagnostic.action == "No action required."


def test_sync_mismatch_diagnostic_code() -> None:
    health = health_for(2)
    health = replace(
        health,
        state=health.state.DEGRADED,
        healthy=False,
        reason="Runtime and status updates are not synchronized.",
    )

    diagnostic = Diagnostic.diagnose(health)

    assert diagnostic.code == "RUN_SYNC_MISMATCH"


def test_sync_mismatch_is_warning() -> None:
    health = health_for(2)
    health = replace(
        health,
        state=health.state.DEGRADED,
        healthy=False,
        reason="Runtime and status updates are not synchronized.",
    )

    diagnostic = Diagnostic.diagnose(health)

    assert diagnostic.severity is Severity.WARNING
    assert not diagnostic.healthy


def test_sync_mismatch_recommends_inspection() -> None:
    health = health_for(2)
    health = replace(
        health,
        state=health.state.DEGRADED,
        healthy=False,
        reason="Runtime and status updates are not synchronized.",
    )

    diagnostic = Diagnostic.diagnose(health)

    assert diagnostic.action == (
        "Inspect runtime and status synchronization."
    )


def test_status_count_mismatch_diagnostic_code() -> None:
    health = health_for(3)
    health = replace(
        health,
        state=health.state.DEGRADED,
        healthy=False,
        reason="Status update count does not match step count.",
    )

    diagnostic = Diagnostic.diagnose(health)

    assert diagnostic.code == "RUN_STATUS_COUNT_MISMATCH"


def test_status_count_mismatch_is_warning() -> None:
    health = health_for(3)
    health = replace(
        health,
        state=health.state.DEGRADED,
        healthy=False,
        reason="Status update count does not match step count.",
    )

    diagnostic = Diagnostic.diagnose(health)

    assert diagnostic.severity is Severity.WARNING
    assert not diagnostic.healthy


def test_status_count_mismatch_recommends_status_inspection() -> None:
    health = health_for(3)
    health = replace(
        health,
        state=health.state.DEGRADED,
        healthy=False,
        reason="Status update count does not match step count.",
    )

    diagnostic = Diagnostic.diagnose(health)

    assert diagnostic.action == "Inspect status update generation."


def test_diagnostic_preserves_health_message() -> None:
    health = health_for(3)
    health = replace(
        health,
        state=health.state.DEGRADED,
        healthy=False,
        reason="Status update count does not match step count.",
    )

    diagnostic = Diagnostic.diagnose(health)

    assert diagnostic.message == health.reason


def test_diagnostic_is_immutable_snapshot() -> None:
    diagnostic = Diagnostic.diagnose(
        health_for(2)
    )

    assert diagnostic.code == "RUN_HEALTHY"
    assert diagnostic.healthy
    assert diagnostic.severity is Severity.SUCCESS
