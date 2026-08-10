import importlib

import pytest

runner_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "runtime_runner"
)

Runner = (
    runner_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeRunner
)
RunResult = (
    runner_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunResult
)


def running_runner() -> Runner:
    runner = Runner.create()
    runner.start()
    return runner


def test_runner_starts_stopped() -> None:
    runner = Runner.create()

    assert not runner.running
    assert runner.run_count == 0
    assert runner.latest is None
    assert not runner.has_runs


def test_create_builds_bridge() -> None:
    runner = Runner.create()

    assert runner.bridge is not None


def test_start_starts_bridge() -> None:
    runner = Runner.create()

    runner.start()

    assert runner.running
    assert runner.bridge.running


def test_run_requires_running_runner() -> None:
    runner = Runner.create()

    with pytest.raises(
        RuntimeError,
        match="Runtime history status runner is not running.",
    ):
        runner.run(1)


def test_negative_steps_are_rejected() -> None:
    runner = running_runner()

    with pytest.raises(
        ValueError,
        match="Runtime history status runner steps cannot be negative.",
    ):
        runner.run(-1)


def test_zero_step_run_is_valid() -> None:
    runner = running_runner()

    result = runner.run(0)

    assert isinstance(result, RunResult)
    assert result.steps == ()
    assert result.step_count == 0
    assert result.latest is None


def test_first_run_increments_count() -> None:
    runner = running_runner()

    runner.run(1)

    assert runner.run_count == 1


def test_single_step_run_returns_one_step() -> None:
    runner = running_runner()

    result = runner.run(1)

    assert result.step_count == 1
    assert result.latest is result.steps[0]


def test_single_step_synchronizes_runtime_and_status() -> None:
    runner = running_runner()

    result = runner.run(1)
    step = result.latest

    assert step is not None
    assert step.runtime_update.statistics.total_cycles == 1
    assert step.status_update.view.cycles == "Cycles 1"


def test_multiple_steps_are_recorded() -> None:
    runner = running_runner()

    result = runner.run(3)

    assert result.step_count == 3
    assert tuple(step.sequence for step in result.steps) == (
        1,
        2,
        3,
    )


def test_multiple_steps_accumulate_runtime() -> None:
    runner = running_runner()

    result = runner.run(3)
    latest = result.latest

    assert latest is not None
    assert latest.runtime_update.statistics.total_cycles == 3
    assert latest.status_update.view.cycles == "Cycles 3"


def test_run_stores_latest_result() -> None:
    runner = running_runner()

    result = runner.run(2)

    assert runner.latest is result
    assert runner.has_runs


def test_multiple_runs_increment_run_count() -> None:
    runner = running_runner()

    runner.run(1)
    runner.run(2)
    runner.run(3)

    assert runner.run_count == 3


def test_runtime_steps_continue_between_runs() -> None:
    runner = running_runner()

    first = runner.run(2)
    second = runner.run(2)

    assert first.steps[-1].sequence == 2
    assert second.steps[0].sequence == 3
    assert second.steps[-1].sequence == 4


def test_stop_stops_runner() -> None:
    runner = running_runner()

    runner.stop()

    assert not runner.running
    assert not runner.bridge.running


def test_stop_preserves_latest_run() -> None:
    runner = running_runner()

    result = runner.run(2)
    runner.stop()

    assert runner.latest is result
    assert runner.run_count == 1
    assert runner.has_runs


def test_run_after_stop_is_rejected() -> None:
    runner = running_runner()

    runner.stop()

    with pytest.raises(
        RuntimeError,
        match="Runtime history status runner is not running.",
    ):
        runner.run(1)


def test_runner_can_restart() -> None:
    runner = running_runner()

    first = runner.run(1)
    runner.stop()
    runner.start()
    second = runner.run(1)

    assert first.steps[-1].sequence == 1
    assert second.steps[-1].sequence == 2
    assert runner.run_count == 2


def test_reset_clears_runner_state() -> None:
    runner = running_runner()

    runner.run(3)
    runner.reset()

    assert not runner.running
    assert runner.run_count == 0
    assert runner.latest is None
    assert not runner.has_runs


def test_reset_clears_bridge_state() -> None:
    runner = running_runner()

    runner.run(2)
    runner.reset()

    assert runner.bridge.step_count == 0
    assert runner.bridge.latest is None


def test_runner_can_run_after_reset_and_start() -> None:
    runner = running_runner()

    runner.run(2)
    runner.reset()
    runner.start()

    result = runner.run(1)

    assert result.step_count == 1
    assert result.steps[0].sequence == 1
    assert result.steps[0].status_update.view.cycles == "Cycles 1"


def test_previous_run_remains_snapshot() -> None:
    runner = running_runner()

    first = runner.run(1)
    runner.run(2)

    assert first.step_count == 1
    assert first.steps[0].sequence == 1
    assert first.steps[0].status_update.view.cycles == "Cycles 1"
