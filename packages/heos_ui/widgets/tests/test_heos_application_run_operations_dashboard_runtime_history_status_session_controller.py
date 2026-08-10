import importlib

controller_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "session_controller"
)
orchestrator_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_orchestrator"
)
snapshot_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_snapshot"
)

Controller = (
    controller_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSessionController
)
Orchestrator = (
    orchestrator_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestrator
)
Snapshot = (
    snapshot_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySnapshot
)


def idle_snapshot() -> Snapshot:
    return Snapshot.capture(
        Orchestrator.create()
    )


def running_snapshot(
    *,
    cycles: int = 0,
) -> Snapshot:
    orchestrator = Orchestrator.create()
    orchestrator.start()

    for _ in range(cycles):
        orchestrator.cycle()

    return Snapshot.capture(orchestrator)


def test_controller_starts_empty() -> None:
    controller = Controller.create()

    assert controller.tick_count == 0
    assert controller.latest_update is None
    assert not controller.has_updates


def test_create_builds_session() -> None:
    controller = Controller.create()

    assert controller.session is not None


def test_first_tick_returns_update() -> None:
    controller = Controller.create()

    update = controller.tick(
        idle_snapshot()
    )

    assert update is controller.latest_update


def test_first_tick_increments_count() -> None:
    controller = Controller.create()

    controller.tick(
        idle_snapshot()
    )

    assert controller.tick_count == 1


def test_first_tick_refreshes_session() -> None:
    controller = Controller.create()

    controller.tick(
        idle_snapshot()
    )

    assert controller.session.refresh_count == 1


def test_idle_tick_produces_idle_status() -> None:
    controller = Controller.create()

    update = controller.tick(
        idle_snapshot()
    )

    assert update.view.status == "IDLE"
    assert update.frame.commands[1].text == "IDLE"


def test_running_tick_produces_running_status() -> None:
    controller = Controller.create()

    update = controller.tick(
        running_snapshot()
    )

    assert update.view.status == "RUNNING"
    assert update.frame.commands[1].text == "RUNNING"


def test_cycle_counts_flow_through_controller() -> None:
    controller = Controller.create()

    update = controller.tick(
        running_snapshot(cycles=4)
    )

    assert update.view.cycles == "Cycles 4"
    assert update.view.runs == "Runs 4"
    assert update.frame.commands[3].text == "Cycles: Cycles 4"
    assert update.frame.commands[4].text == "Runs: Runs 4"


def test_multiple_ticks_increment_count() -> None:
    controller = Controller.create()

    controller.tick(
        idle_snapshot()
    )
    controller.tick(
        running_snapshot()
    )
    controller.tick(
        running_snapshot(cycles=2)
    )

    assert controller.tick_count == 3
    assert controller.session.refresh_count == 3


def test_latest_update_tracks_last_tick() -> None:
    controller = Controller.create()

    controller.tick(
        idle_snapshot()
    )
    latest = controller.tick(
        running_snapshot(cycles=2)
    )

    assert controller.latest_update is latest
    assert latest.sequence == 2
    assert latest.view.cycles == "Cycles 2"


def test_controller_reports_updates() -> None:
    controller = Controller.create()

    controller.tick(
        idle_snapshot()
    )

    assert controller.has_updates
    assert controller.session.has_updates


def test_reset_clears_tick_count() -> None:
    controller = Controller.create()

    controller.tick(
        running_snapshot(cycles=2)
    )
    controller.reset()

    assert controller.tick_count == 0


def test_reset_clears_session() -> None:
    controller = Controller.create()

    controller.tick(
        running_snapshot(cycles=2)
    )
    controller.reset()

    assert controller.latest_update is None
    assert not controller.has_updates
    assert controller.session.refresh_count == 0


def test_reset_clears_rendered_state() -> None:
    controller = Controller.create()

    controller.tick(
        running_snapshot(cycles=2)
    )
    controller.reset()

    assert controller.session.widget.view is None
    assert controller.session.live_renderer.latest_frame is None


def test_controller_can_tick_after_reset() -> None:
    controller = Controller.create()

    controller.tick(
        running_snapshot(cycles=3)
    )
    controller.reset()

    update = controller.tick(
        idle_snapshot()
    )

    assert controller.tick_count == 1
    assert controller.session.refresh_count == 1
    assert update.sequence == 1
    assert update.view.status == "IDLE"


def test_tick_and_session_counts_stay_synchronized() -> None:
    controller = Controller.create()

    for cycles in range(5):
        controller.tick(
            running_snapshot(cycles=cycles)
        )

    assert controller.tick_count == 5
    assert controller.session.refresh_count == 5
    assert controller.latest_update is not None
    assert controller.latest_update.sequence == 5
