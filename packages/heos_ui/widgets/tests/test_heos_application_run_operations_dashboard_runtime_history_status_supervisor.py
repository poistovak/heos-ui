import importlib

import pytest

supervisor_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_supervisor"
)

Supervisor = (
    supervisor_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSupervisor
)


def running_supervisor() -> Supervisor:
    supervisor = Supervisor.create()
    supervisor.start()
    return supervisor


def test_supervisor_starts_stopped() -> None:
    supervisor = Supervisor.create()

    assert not supervisor.running
    assert supervisor.refresh_count == 0
    assert supervisor.latest is None
    assert not supervisor.has_updates


def test_create_builds_orchestrator() -> None:
    supervisor = Supervisor.create()

    assert supervisor.orchestrator is not None


def test_create_builds_controller() -> None:
    supervisor = Supervisor.create()

    assert supervisor.controller is not None


def test_start_marks_supervisor_running() -> None:
    supervisor = Supervisor.create()

    supervisor.start()

    assert supervisor.running
    assert supervisor.orchestrator.running


def test_start_is_idempotent() -> None:
    supervisor = Supervisor.create()

    supervisor.start()
    supervisor.start()

    assert supervisor.running
    assert supervisor.refresh_count == 0


def test_refresh_requires_running_supervisor() -> None:
    supervisor = Supervisor.create()

    with pytest.raises(
        RuntimeError,
        match="Runtime history status supervisor is not running.",
    ):
        supervisor.refresh()


def test_first_refresh_returns_update() -> None:
    supervisor = running_supervisor()

    update = supervisor.refresh()

    assert update is supervisor.latest


def test_first_refresh_increments_count() -> None:
    supervisor = running_supervisor()

    supervisor.refresh()

    assert supervisor.refresh_count == 1


def test_first_refresh_updates_controller() -> None:
    supervisor = running_supervisor()

    supervisor.refresh()

    assert supervisor.controller.tick_count == 1


def test_first_refresh_produces_running_view() -> None:
    supervisor = running_supervisor()

    update = supervisor.refresh()

    assert update.view.status == "RUNNING"
    assert update.frame.commands[1].text == "RUNNING"


def test_multiple_refreshes_increment_count() -> None:
    supervisor = running_supervisor()

    supervisor.refresh()
    supervisor.refresh()
    supervisor.refresh()

    assert supervisor.refresh_count == 3
    assert supervisor.controller.tick_count == 3


def test_refresh_without_cycles_keeps_zero_counts() -> None:
    supervisor = running_supervisor()

    update = supervisor.refresh()

    assert update.view.cycles == "Cycles 0"
    assert update.view.runs == "Runs 0"
    assert update.view.refreshes == "Refreshes 0"


def test_orchestrator_cycle_flows_to_status() -> None:
    supervisor = running_supervisor()

    supervisor.orchestrator.cycle()
    update = supervisor.refresh()

    assert update.view.cycles == "Cycles 1"
    assert update.view.runs == "Runs 1"
    assert update.view.refreshes == "Refreshes 1"


def test_multiple_orchestrator_cycles_flow_to_status() -> None:
    supervisor = running_supervisor()

    supervisor.orchestrator.cycle()
    supervisor.orchestrator.cycle()
    supervisor.orchestrator.cycle()

    update = supervisor.refresh()

    assert update.view.cycles == "Cycles 3"
    assert update.view.runs == "Runs 3"
    assert update.view.refreshes == "Refreshes 3"
    assert update.view.latest == "Latest sequence 3"


def test_stop_marks_supervisor_stopped() -> None:
    supervisor = running_supervisor()

    supervisor.stop()

    assert not supervisor.running
    assert not supervisor.orchestrator.running


def test_stop_preserves_existing_status() -> None:
    supervisor = running_supervisor()

    update = supervisor.refresh()
    supervisor.stop()

    assert supervisor.latest is update
    assert supervisor.has_updates
    assert supervisor.refresh_count == 1


def test_refresh_after_stop_is_rejected() -> None:
    supervisor = running_supervisor()

    supervisor.stop()

    with pytest.raises(
        RuntimeError,
        match="Runtime history status supervisor is not running.",
    ):
        supervisor.refresh()


def test_supervisor_can_restart() -> None:
    supervisor = running_supervisor()

    first = supervisor.refresh()
    supervisor.stop()
    supervisor.start()
    second = supervisor.refresh()

    assert first.sequence == 1
    assert second.sequence == 2
    assert supervisor.refresh_count == 2
    assert supervisor.running


def test_reset_stops_supervisor() -> None:
    supervisor = running_supervisor()

    supervisor.refresh()
    supervisor.reset()

    assert not supervisor.running
    assert not supervisor.orchestrator.running


def test_reset_clears_counts() -> None:
    supervisor = running_supervisor()

    supervisor.refresh()
    supervisor.refresh()
    supervisor.reset()

    assert supervisor.refresh_count == 0
    assert supervisor.controller.tick_count == 0


def test_reset_clears_updates() -> None:
    supervisor = running_supervisor()

    supervisor.refresh()
    supervisor.reset()

    assert supervisor.latest is None
    assert not supervisor.has_updates


def test_supervisor_can_refresh_after_reset_and_start() -> None:
    supervisor = running_supervisor()

    supervisor.refresh()
    supervisor.reset()
    supervisor.start()

    update = supervisor.refresh()

    assert supervisor.running
    assert supervisor.refresh_count == 1
    assert update.sequence == 1


def test_runtime_cycle_restarts_after_reset() -> None:
    supervisor = running_supervisor()

    supervisor.orchestrator.cycle()
    first = supervisor.refresh()

    assert first.view.cycles == "Cycles 1"
    assert first.view.latest == "Latest sequence 1"
    assert first.sequence == 1

    supervisor.reset()

    assert supervisor.refresh_count == 0
    assert supervisor.controller.tick_count == 0
    assert supervisor.latest is None

    supervisor.start()
    supervisor.orchestrator.cycle()
    second = supervisor.refresh()

    assert second.view.cycles == "Cycles 1"
    assert second.view.runs == "Runs 1"
    assert second.view.refreshes == "Refreshes 1"
    assert second.view.latest == "Latest sequence 1"
    assert second.sequence == 1