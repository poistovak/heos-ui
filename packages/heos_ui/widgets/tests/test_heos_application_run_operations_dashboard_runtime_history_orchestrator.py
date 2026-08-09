import importlib

import pytest

orchestrator_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_orchestrator"
)

Orchestrator = (
    orchestrator_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestrator
)
OrchestratorState = (
    orchestrator_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestratorState
)


def running_orchestrator() -> Orchestrator:
    orchestrator = Orchestrator.create()
    orchestrator.start()
    return orchestrator


def test_orchestrator_starts_stopped() -> None:
    orchestrator = Orchestrator.create()

    assert orchestrator.state is OrchestratorState.STOPPED
    assert not orchestrator.running
    assert orchestrator.cycle_count == 0
    assert orchestrator.latest is None
    assert not orchestrator.has_updates


def test_create_builds_operations_session() -> None:
    orchestrator = Orchestrator.create()

    assert orchestrator.operations is not None


def test_create_builds_supervisor() -> None:
    orchestrator = Orchestrator.create()

    assert orchestrator.supervisor is not None


def test_start_marks_orchestrator_running() -> None:
    orchestrator = Orchestrator.create()

    orchestrator.start()

    assert orchestrator.running
    assert orchestrator.state is OrchestratorState.RUNNING


def test_start_is_idempotent() -> None:
    orchestrator = Orchestrator.create()

    orchestrator.start()
    orchestrator.start()

    assert orchestrator.running
    assert orchestrator.cycle_count == 0


def test_cycle_requires_running_orchestrator() -> None:
    orchestrator = Orchestrator.create()

    with pytest.raises(
        RuntimeError,
        match="Runtime history orchestrator is not running.",
    ):
        orchestrator.cycle()


def test_first_cycle_returns_update() -> None:
    orchestrator = running_orchestrator()

    update = orchestrator.cycle()

    assert update is orchestrator.latest


def test_first_cycle_increments_count() -> None:
    orchestrator = running_orchestrator()

    orchestrator.cycle()

    assert orchestrator.cycle_count == 1


def test_first_cycle_updates_supervisor_count() -> None:
    orchestrator = running_orchestrator()

    orchestrator.cycle()

    assert orchestrator.supervisor.run_count == 1


def test_first_cycle_produces_history() -> None:
    orchestrator = running_orchestrator()

    update = orchestrator.cycle()

    assert orchestrator.has_updates
    assert update.sequence == 1
    assert update.statistics.total_cycles == 1


def test_multiple_cycles_increment_count() -> None:
    orchestrator = running_orchestrator()

    orchestrator.cycle()
    orchestrator.cycle()
    orchestrator.cycle()

    assert orchestrator.cycle_count == 3
    assert orchestrator.supervisor.run_count == 3


def test_multiple_cycles_accumulate_history() -> None:
    orchestrator = running_orchestrator()

    orchestrator.cycle()
    orchestrator.cycle()
    third = orchestrator.cycle()

    assert third.sequence == 3
    assert third.statistics.total_cycles == 3


def test_stop_marks_orchestrator_stopped() -> None:
    orchestrator = running_orchestrator()

    orchestrator.stop()

    assert not orchestrator.running
    assert orchestrator.state is OrchestratorState.STOPPED


def test_stop_preserves_existing_history() -> None:
    orchestrator = running_orchestrator()

    update = orchestrator.cycle()
    orchestrator.stop()

    assert orchestrator.latest is update
    assert orchestrator.cycle_count == 1
    assert orchestrator.has_updates


def test_cycle_after_stop_is_rejected() -> None:
    orchestrator = running_orchestrator()

    orchestrator.stop()

    with pytest.raises(
        RuntimeError,
        match="Runtime history orchestrator is not running.",
    ):
        orchestrator.cycle()


def test_orchestrator_can_restart() -> None:
    orchestrator = running_orchestrator()

    first = orchestrator.cycle()
    orchestrator.stop()
    orchestrator.start()
    second = orchestrator.cycle()

    assert first.sequence == 1
    assert second.sequence == 2
    assert orchestrator.cycle_count == 2
    assert orchestrator.running


def test_reset_stops_orchestrator() -> None:
    orchestrator = running_orchestrator()

    orchestrator.cycle()
    orchestrator.reset()

    assert not orchestrator.running
    assert orchestrator.state is OrchestratorState.STOPPED


def test_reset_clears_cycle_count() -> None:
    orchestrator = running_orchestrator()

    orchestrator.cycle()
    orchestrator.cycle()
    orchestrator.reset()

    assert orchestrator.cycle_count == 0


def test_reset_clears_history_updates() -> None:
    orchestrator = running_orchestrator()

    orchestrator.cycle()
    orchestrator.reset()

    assert orchestrator.latest is None
    assert not orchestrator.has_updates
    assert orchestrator.supervisor.run_count == 0


def test_orchestrator_can_cycle_after_reset_and_start() -> None:
    orchestrator = running_orchestrator()

    orchestrator.cycle()
    orchestrator.reset()
    orchestrator.start()

    update = orchestrator.cycle()

    assert orchestrator.running
    assert orchestrator.cycle_count == 1
    assert update.sequence == 1


def test_runtime_cycle_continues_after_reset() -> None:
    orchestrator = running_orchestrator()

    first = orchestrator.cycle()
    orchestrator.reset()
    orchestrator.start()
    second = orchestrator.cycle()

    assert first.statistics.latest_cycle == 1
    assert second.statistics.latest_cycle == 2
