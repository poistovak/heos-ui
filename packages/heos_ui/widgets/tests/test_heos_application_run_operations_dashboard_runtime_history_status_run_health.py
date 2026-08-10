import importlib
from dataclasses import replace

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

Health = (
    health_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealth
)
HealthState = (
    health_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealthState
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


def summary_for(steps: int) -> Summary:
    runner = running_runner()
    return Summary.capture(
        runner.run(steps)
    )


def test_empty_run_is_empty_health_state() -> None:
    health = Health.evaluate(
        summary_for(0)
    )

    assert health.state is HealthState.EMPTY


def test_empty_run_is_healthy() -> None:
    health = Health.evaluate(
        summary_for(0)
    )

    assert health.healthy


def test_empty_run_has_zero_counts() -> None:
    health = Health.evaluate(
        summary_for(0)
    )

    assert health.step_count == 0
    assert health.runtime_cycles == 0
    assert health.status_updates == 0


def test_empty_run_has_reason() -> None:
    health = Health.evaluate(
        summary_for(0)
    )

    assert health.reason == "Run completed without runtime steps."


def test_single_step_run_is_healthy() -> None:
    health = Health.evaluate(
        summary_for(1)
    )

    assert health.state is HealthState.HEALTHY
    assert health.healthy


def test_single_step_health_preserves_counts() -> None:
    health = Health.evaluate(
        summary_for(1)
    )

    assert health.step_count == 1
    assert health.runtime_cycles == 1
    assert health.status_updates == 1


def test_multiple_step_run_is_healthy() -> None:
    health = Health.evaluate(
        summary_for(4)
    )

    assert health.state is HealthState.HEALTHY
    assert health.healthy


def test_multiple_step_health_preserves_counts() -> None:
    health = Health.evaluate(
        summary_for(4)
    )

    assert health.step_count == 4
    assert health.runtime_cycles == 4
    assert health.status_updates == 4


def test_healthy_run_has_reason() -> None:
    health = Health.evaluate(
        summary_for(3)
    )

    assert health.reason == "Runtime history status run is healthy."


def test_unsynchronized_run_is_degraded() -> None:
    summary = replace(
        summary_for(2),
        synchronized=False,
    )

    health = Health.evaluate(summary)

    assert health.state is HealthState.DEGRADED
    assert not health.healthy


def test_unsynchronized_run_has_reason() -> None:
    summary = replace(
        summary_for(2),
        synchronized=False,
    )

    health = Health.evaluate(summary)

    assert (
        health.reason
        == "Runtime and status updates are not synchronized."
    )


def test_unsynchronized_run_preserves_counts() -> None:
    summary = replace(
        summary_for(3),
        synchronized=False,
    )

    health = Health.evaluate(summary)

    assert health.step_count == 3
    assert health.runtime_cycles == 3
    assert health.status_updates == 3


def test_status_count_mismatch_is_degraded() -> None:
    summary = replace(
        summary_for(3),
        status_updates=2,
    )

    health = Health.evaluate(summary)

    assert health.state is HealthState.DEGRADED
    assert not health.healthy


def test_status_count_mismatch_has_reason() -> None:
    summary = replace(
        summary_for(3),
        status_updates=2,
    )

    health = Health.evaluate(summary)

    assert health.reason == "Status update count does not match step count."


def test_status_count_mismatch_preserves_values() -> None:
    summary = replace(
        summary_for(3),
        status_updates=2,
    )

    health = Health.evaluate(summary)

    assert health.step_count == 3
    assert health.runtime_cycles == 3
    assert health.status_updates == 2


def test_health_result_is_immutable_snapshot() -> None:
    summary = summary_for(2)
    health = Health.evaluate(summary)

    changed = replace(
        summary,
        synchronized=False,
    )

    assert not changed.synchronized
    assert health.state is HealthState.HEALTHY
    assert health.healthy
    assert health.step_count == 2
