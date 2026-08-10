import importlib

orchestrator_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_orchestrator"
)
session_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_session"
)
snapshot_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_snapshot"
)

Orchestrator = (
    orchestrator_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestrator
)
Session = (
    session_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSession
)
SessionUpdate = (
    session_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSessionUpdate
)
Snapshot = (
    snapshot_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySnapshot
)


def snapshot():
    orchestrator = Orchestrator.create()
    return Snapshot.capture(orchestrator)


def running_snapshot(*, cycles: int = 0):
    orchestrator = Orchestrator.create()
    orchestrator.start()

    for _ in range(cycles):
        orchestrator.cycle()

    return Snapshot.capture(orchestrator)


def test_session_starts_empty() -> None:
    session = Session.create()

    assert session.refresh_count == 0
    assert session.latest_update is None
    assert not session.has_updates


def test_create_builds_presenter() -> None:
    session = Session.create()

    assert session.presenter is not None


def test_create_builds_widget() -> None:
    session = Session.create()

    assert session.widget is not None


def test_create_builds_live_renderer() -> None:
    session = Session.create()

    assert session.live_renderer is not None


def test_refresh_returns_update() -> None:
    session = Session.create()

    update = session.refresh(snapshot())

    assert isinstance(update, SessionUpdate)


def test_first_refresh_has_sequence_one() -> None:
    session = Session.create()

    update = session.refresh(snapshot())

    assert update.sequence == 1
    assert session.refresh_count == 1


def test_refresh_stores_latest_update() -> None:
    session = Session.create()

    update = session.refresh(snapshot())

    assert session.latest_update is update
    assert session.has_updates


def test_refresh_updates_widget() -> None:
    session = Session.create()

    update = session.refresh(snapshot())

    assert session.widget.view is update.view
    assert session.widget.has_view


def test_refresh_updates_live_renderer() -> None:
    session = Session.create()

    update = session.refresh(snapshot())

    assert session.live_renderer.latest_frame is update.frame
    assert session.live_renderer.has_frame


def test_idle_snapshot_produces_idle_view() -> None:
    session = Session.create()

    update = session.refresh(snapshot())

    assert update.view.status == "IDLE"
    assert update.frame.commands[1].text == "IDLE"


def test_running_snapshot_produces_running_view() -> None:
    session = Session.create()

    update = session.refresh(
        running_snapshot()
    )

    assert update.view.status == "RUNNING"
    assert update.frame.commands[1].text == "RUNNING"


def test_cycle_counts_flow_to_frame() -> None:
    session = Session.create()

    update = session.refresh(
        running_snapshot(cycles=3)
    )

    assert update.view.cycles == "Cycles 3"
    assert update.view.runs == "Runs 3"
    assert update.frame.commands[3].text == "Cycles: Cycles 3"
    assert update.frame.commands[4].text == "Runs: Runs 3"


def test_multiple_refreshes_increment_sequence() -> None:
    session = Session.create()

    first = session.refresh(snapshot())
    second = session.refresh(running_snapshot())
    third = session.refresh(running_snapshot(cycles=2))

    assert first.sequence == 1
    assert second.sequence == 2
    assert third.sequence == 3
    assert session.refresh_count == 3


def test_latest_update_tracks_last_refresh() -> None:
    session = Session.create()

    session.refresh(snapshot())
    latest = session.refresh(
        running_snapshot(cycles=2)
    )

    assert session.latest_update is latest
    assert latest.sequence == 2
    assert latest.view.cycles == "Cycles 2"


def test_reset_clears_session_state() -> None:
    session = Session.create()

    session.refresh(
        running_snapshot(cycles=2)
    )
    session.reset()

    assert session.refresh_count == 0
    assert session.latest_update is None
    assert not session.has_updates
    assert session.widget.view is None
    assert session.live_renderer.latest_frame is None


def test_session_can_refresh_after_reset() -> None:
    session = Session.create()

    session.refresh(
        running_snapshot(cycles=3)
    )
    session.reset()

    update = session.refresh(snapshot())

    assert update.sequence == 1
    assert session.refresh_count == 1
    assert session.has_updates
    assert update.view.status == "IDLE"
