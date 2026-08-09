import importlib

orchestrator_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_orchestrator"
)
snapshot_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_snapshot"
)

Orchestrator = (
    orchestrator_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestrator
)
OrchestratorState = (
    orchestrator_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestratorState
)
Snapshot = (
    snapshot_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySnapshot
)


def running_orchestrator() -> Orchestrator:
    orchestrator = Orchestrator.create()
    orchestrator.start()
    return orchestrator


def test_capture_returns_snapshot() -> None:
    orchestrator = Orchestrator.create()

    snapshot = Snapshot.capture(orchestrator)

    assert isinstance(snapshot, Snapshot)


def test_initial_snapshot_is_stopped() -> None:
    snapshot = Snapshot.capture(
        Orchestrator.create()
    )

    assert snapshot.state is OrchestratorState.STOPPED
    assert not snapshot.running


def test_initial_snapshot_has_zero_cycle_count() -> None:
    snapshot = Snapshot.capture(
        Orchestrator.create()
    )

    assert snapshot.cycle_count == 0


def test_initial_snapshot_has_zero_run_count() -> None:
    snapshot = Snapshot.capture(
        Orchestrator.create()
    )

    assert snapshot.run_count == 0


def test_initial_snapshot_has_zero_refresh_count() -> None:
    snapshot = Snapshot.capture(
        Orchestrator.create()
    )

    assert snapshot.refresh_count == 0


def test_initial_snapshot_has_no_updates() -> None:
    snapshot = Snapshot.capture(
        Orchestrator.create()
    )

    assert not snapshot.has_updates
    assert snapshot.latest_sequence is None


def test_started_snapshot_is_running() -> None:
    orchestrator = running_orchestrator()

    snapshot = Snapshot.capture(orchestrator)

    assert snapshot.state is OrchestratorState.RUNNING
    assert snapshot.running


def test_one_cycle_is_captured() -> None:
    orchestrator = running_orchestrator()
    orchestrator.cycle()

    snapshot = Snapshot.capture(orchestrator)

    assert snapshot.cycle_count == 1
    assert snapshot.run_count == 1
    assert snapshot.refresh_count == 1


def test_one_cycle_sets_latest_sequence() -> None:
    orchestrator = running_orchestrator()
    orchestrator.cycle()

    snapshot = Snapshot.capture(orchestrator)

    assert snapshot.has_updates
    assert snapshot.latest_sequence == 1


def test_multiple_cycles_are_captured() -> None:
    orchestrator = running_orchestrator()

    orchestrator.cycle()
    orchestrator.cycle()
    orchestrator.cycle()

    snapshot = Snapshot.capture(orchestrator)

    assert snapshot.cycle_count == 3
    assert snapshot.run_count == 3
    assert snapshot.refresh_count == 3
    assert snapshot.latest_sequence == 3


def test_stopped_snapshot_preserves_counts() -> None:
    orchestrator = running_orchestrator()

    orchestrator.cycle()
    orchestrator.cycle()
    orchestrator.stop()

    snapshot = Snapshot.capture(orchestrator)

    assert snapshot.state is OrchestratorState.STOPPED
    assert not snapshot.running
    assert snapshot.cycle_count == 2
    assert snapshot.run_count == 2
    assert snapshot.refresh_count == 2
    assert snapshot.latest_sequence == 2


def test_reset_snapshot_is_empty() -> None:
    orchestrator = running_orchestrator()

    orchestrator.cycle()
    orchestrator.cycle()
    orchestrator.reset()

    snapshot = Snapshot.capture(orchestrator)

    assert snapshot.state is OrchestratorState.STOPPED
    assert not snapshot.running
    assert snapshot.cycle_count == 0
    assert snapshot.run_count == 0
    assert snapshot.refresh_count == 0
    assert not snapshot.has_updates
    assert snapshot.latest_sequence is None


def test_snapshot_is_immutable() -> None:
    orchestrator = running_orchestrator()
    orchestrator.cycle()

    snapshot = Snapshot.capture(orchestrator)

    try:
        snapshot.cycle_count = 99
    except AttributeError:
        pass
    else:
        raise AssertionError("Snapshot must be immutable.")


def test_previous_snapshot_remains_unchanged() -> None:
    orchestrator = running_orchestrator()
    orchestrator.cycle()

    first = Snapshot.capture(orchestrator)

    orchestrator.cycle()
    second = Snapshot.capture(orchestrator)

    assert first.cycle_count == 1
    assert first.latest_sequence == 1
    assert second.cycle_count == 2
    assert second.latest_sequence == 2


def test_snapshot_counts_remain_synchronized() -> None:
    orchestrator = running_orchestrator()

    for _ in range(5):
        orchestrator.cycle()

    snapshot = Snapshot.capture(orchestrator)

    assert snapshot.cycle_count == 5
    assert snapshot.run_count == 5
    assert snapshot.refresh_count == 5
    assert snapshot.latest_sequence == 5
