import importlib

import pytest

application_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_application"
)

Application = (
    application_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusApplication
)


def running_application() -> Application:
    application = Application.create()
    application.launch()
    return application


def test_application_starts_stopped() -> None:
    application = Application.create()

    assert not application.running
    assert application.update_count == 0
    assert application.latest is None
    assert not application.has_updates


def test_create_builds_supervisor() -> None:
    application = Application.create()

    assert application.supervisor is not None


def test_launch_starts_application() -> None:
    application = Application.create()

    application.launch()

    assert application.running
    assert application.supervisor.running


def test_launch_is_idempotent() -> None:
    application = Application.create()

    application.launch()
    application.launch()

    assert application.running
    assert application.update_count == 0


def test_update_requires_running_application() -> None:
    application = Application.create()

    with pytest.raises(
        RuntimeError,
        match="Runtime history status application is not running.",
    ):
        application.update()


def test_first_update_returns_latest() -> None:
    application = running_application()

    update = application.update()

    assert update is application.latest


def test_first_update_increments_count() -> None:
    application = running_application()

    application.update()

    assert application.update_count == 1


def test_first_update_refreshes_supervisor() -> None:
    application = running_application()

    application.update()

    assert application.supervisor.refresh_count == 1


def test_first_update_produces_running_status() -> None:
    application = running_application()

    update = application.update()

    assert update.view.status == "RUNNING"
    assert update.frame.commands[1].text == "RUNNING"


def test_runtime_cycle_flows_through_application() -> None:
    application = running_application()

    application.supervisor.orchestrator.cycle()
    update = application.update()

    assert update.view.cycles == "Cycles 1"
    assert update.view.runs == "Runs 1"
    assert update.view.refreshes == "Refreshes 1"


def test_multiple_cycles_flow_through_application() -> None:
    application = running_application()

    for _ in range(3):
        application.supervisor.orchestrator.cycle()

    update = application.update()

    assert update.view.cycles == "Cycles 3"
    assert update.view.latest == "Latest sequence 3"


def test_multiple_updates_increment_count() -> None:
    application = running_application()

    application.update()
    application.update()
    application.update()

    assert application.update_count == 3
    assert application.supervisor.refresh_count == 3


def test_latest_tracks_last_update() -> None:
    application = running_application()

    application.update()
    application.supervisor.orchestrator.cycle()
    latest = application.update()

    assert application.latest is latest
    assert latest.sequence == 2


def test_shutdown_stops_application() -> None:
    application = running_application()

    application.shutdown()

    assert not application.running
    assert not application.supervisor.running


def test_shutdown_preserves_latest_update() -> None:
    application = running_application()

    update = application.update()
    application.shutdown()

    assert application.latest is update
    assert application.has_updates
    assert application.update_count == 1


def test_update_after_shutdown_is_rejected() -> None:
    application = running_application()

    application.shutdown()

    with pytest.raises(
        RuntimeError,
        match="Runtime history status application is not running.",
    ):
        application.update()


def test_application_can_relaunch() -> None:
    application = running_application()

    first = application.update()
    application.shutdown()
    application.launch()
    second = application.update()

    assert first.sequence == 1
    assert second.sequence == 2
    assert application.update_count == 2


def test_reset_stops_application() -> None:
    application = running_application()

    application.update()
    application.reset()

    assert not application.running


def test_reset_clears_counts() -> None:
    application = running_application()

    application.update()
    application.update()
    application.reset()

    assert application.update_count == 0
    assert application.supervisor.refresh_count == 0


def test_reset_clears_latest_update() -> None:
    application = running_application()

    application.update()
    application.reset()

    assert application.latest is None
    assert not application.has_updates


def test_application_can_update_after_reset_and_launch() -> None:
    application = running_application()

    application.update()
    application.reset()
    application.launch()

    update = application.update()

    assert application.running
    assert application.update_count == 1
    assert update.sequence == 1


def test_reset_restarts_runtime_history() -> None:
    application = running_application()

    application.supervisor.orchestrator.cycle()
    first = application.update()

    assert first.view.cycles == "Cycles 1"

    application.reset()
    application.launch()

    application.supervisor.orchestrator.cycle()
    second = application.update()

    assert second.view.cycles == "Cycles 1"
    assert second.view.latest == "Latest sequence 1"
    assert second.sequence == 1
