import importlib

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


def test_empty_run_produces_empty_summary() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(0)
    )

    assert summary.empty
    assert summary.step_count == 0


def test_empty_run_has_no_sequences() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(0)
    )

    assert summary.first_sequence is None
    assert summary.last_sequence is None


def test_empty_run_has_zero_runtime_cycles() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(0)
    )

    assert summary.runtime_cycles == 0
    assert summary.status_updates == 0


def test_empty_run_is_synchronized() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(0)
    )

    assert summary.synchronized


def test_single_step_summary_has_one_step() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(1)
    )

    assert summary.step_count == 1
    assert not summary.empty


def test_single_step_sequences_are_one() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(1)
    )

    assert summary.first_sequence == 1
    assert summary.last_sequence == 1


def test_single_step_runtime_cycle_is_one() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(1)
    )

    assert summary.runtime_cycles == 1


def test_single_step_status_update_is_one() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(1)
    )

    assert summary.status_updates == 1


def test_single_step_is_synchronized() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(1)
    )

    assert summary.synchronized


def test_multiple_steps_preserve_sequence_range() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(4)
    )

    assert summary.first_sequence == 1
    assert summary.last_sequence == 4


def test_multiple_steps_count_runtime_cycles() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(4)
    )

    assert summary.runtime_cycles == 4


def test_multiple_steps_count_status_updates() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(4)
    )

    assert summary.status_updates == 4


def test_multiple_steps_remain_synchronized() -> None:
    runner = running_runner()

    summary = Summary.capture(
        runner.run(4)
    )

    assert summary.synchronized


def test_second_run_preserves_global_sequences() -> None:
    runner = running_runner()

    runner.run(2)
    summary = Summary.capture(
        runner.run(3)
    )

    assert summary.first_sequence == 3
    assert summary.last_sequence == 5


def test_second_run_preserves_runtime_cycle_total() -> None:
    runner = running_runner()

    runner.run(2)
    summary = Summary.capture(
        runner.run(3)
    )

    assert summary.runtime_cycles == 5


def test_summary_is_snapshot() -> None:
    runner = running_runner()

    first = Summary.capture(
        runner.run(1)
    )

    runner.run(3)

    assert first.step_count == 1
    assert first.first_sequence == 1
    assert first.last_sequence == 1
    assert first.runtime_cycles == 1
    assert first.status_updates == 1
    assert first.synchronized
