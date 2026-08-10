import importlib

import pytest

bridge_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "runtime_bridge"
)

Bridge = (
    bridge_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeBridge
)
RuntimeStep = (
    bridge_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeStep
)


def running_bridge() -> Bridge:
    bridge = Bridge.create()
    bridge.start()
    return bridge


def test_bridge_starts_stopped() -> None:
    bridge = Bridge.create()

    assert not bridge.running
    assert bridge.step_count == 0
    assert bridge.latest is None
    assert not bridge.has_steps


def test_create_builds_application() -> None:
    bridge = Bridge.create()

    assert bridge.application is not None


def test_start_launches_application() -> None:
    bridge = Bridge.create()

    bridge.start()

    assert bridge.running
    assert bridge.application.running


def test_start_is_idempotent() -> None:
    bridge = Bridge.create()

    bridge.start()
    bridge.start()

    assert bridge.running
    assert bridge.step_count == 0


def test_step_requires_running_bridge() -> None:
    bridge = Bridge.create()

    with pytest.raises(
        RuntimeError,
        match="Runtime history status bridge is not running.",
    ):
        bridge.step()


def test_step_returns_runtime_step() -> None:
    bridge = running_bridge()

    step = bridge.step()

    assert isinstance(step, RuntimeStep)


def test_first_step_has_sequence_one() -> None:
    bridge = running_bridge()

    step = bridge.step()

    assert step.sequence == 1
    assert bridge.step_count == 1


def test_first_step_stores_latest() -> None:
    bridge = running_bridge()

    step = bridge.step()

    assert bridge.latest is step
    assert bridge.has_steps


def test_step_executes_runtime_cycle() -> None:
    bridge = running_bridge()

    step = bridge.step()

    assert step.runtime_update.sequence == 1
    assert step.runtime_update.statistics.total_cycles == 1


def test_step_executes_status_update() -> None:
    bridge = running_bridge()

    step = bridge.step()

    assert step.status_update.sequence == 1
    assert step.status_update.view.status == "RUNNING"


def test_runtime_and_status_are_synchronized() -> None:
    bridge = running_bridge()

    step = bridge.step()

    assert step.runtime_update.statistics.total_cycles == 1
    assert step.status_update.view.cycles == "Cycles 1"
    assert step.status_update.view.runs == "Runs 1"
    assert step.status_update.view.refreshes == "Refreshes 1"


def test_latest_sequence_flows_to_status() -> None:
    bridge = running_bridge()

    step = bridge.step()

    assert step.runtime_update.sequence == 1
    assert step.status_update.view.latest == "Latest sequence 1"


def test_multiple_steps_increment_counts() -> None:
    bridge = running_bridge()

    first = bridge.step()
    second = bridge.step()
    third = bridge.step()

    assert first.sequence == 1
    assert second.sequence == 2
    assert third.sequence == 3
    assert bridge.step_count == 3


def test_multiple_steps_accumulate_runtime_cycles() -> None:
    bridge = running_bridge()

    bridge.step()
    bridge.step()
    third = bridge.step()

    assert third.runtime_update.statistics.total_cycles == 3
    assert third.status_update.view.cycles == "Cycles 3"
    assert third.status_update.view.latest == "Latest sequence 3"


def test_stop_stops_bridge() -> None:
    bridge = running_bridge()

    bridge.stop()

    assert not bridge.running
    assert not bridge.application.running


def test_stop_preserves_latest_step() -> None:
    bridge = running_bridge()

    step = bridge.step()
    bridge.stop()

    assert bridge.latest is step
    assert bridge.step_count == 1
    assert bridge.has_steps


def test_step_after_stop_is_rejected() -> None:
    bridge = running_bridge()

    bridge.stop()

    with pytest.raises(
        RuntimeError,
        match="Runtime history status bridge is not running.",
    ):
        bridge.step()


def test_bridge_can_restart() -> None:
    bridge = running_bridge()

    first = bridge.step()
    bridge.stop()
    bridge.start()
    second = bridge.step()

    assert first.sequence == 1
    assert second.sequence == 2
    assert second.runtime_update.sequence == 2
    assert bridge.step_count == 2


def test_reset_clears_bridge_state() -> None:
    bridge = running_bridge()

    bridge.step()
    bridge.step()
    bridge.reset()

    assert not bridge.running
    assert bridge.step_count == 0
    assert bridge.latest is None
    assert not bridge.has_steps


def test_reset_clears_application_state() -> None:
    bridge = running_bridge()

    bridge.step()
    bridge.reset()

    assert bridge.application.update_count == 0
    assert bridge.application.latest is None


def test_bridge_can_step_after_reset_and_start() -> None:
    bridge = running_bridge()

    bridge.step()
    bridge.reset()
    bridge.start()

    step = bridge.step()

    assert step.sequence == 1
    assert step.runtime_update.statistics.total_cycles == 1
    assert step.status_update.view.cycles == "Cycles 1"


def test_previous_step_remains_snapshot() -> None:
    bridge = running_bridge()

    first = bridge.step()
    bridge.step()

    assert first.sequence == 1
    assert first.runtime_update.statistics.total_cycles == 1
    assert first.status_update.view.cycles == "Cycles 1"
    assert first.status_update.view.latest == "Latest sequence 1"
