import pytest
from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.brain_runtime_service import BrainRuntimeServiceState
from heos_ui.widgets.heos_brain_runtime import HEOSBrainRuntime


def snapshot(
    *,
    cycle: int = 180,
    health: SystemHealth = SystemHealth.HEALTHY,
    successful: bool = True,
) -> BrainRuntimeSnapshot:
    return BrainRuntimeSnapshot(
        cycle_sequence=cycle,
        system_health=health,
        accepted=4,
        blocked=0,
        executed=4,
        healthy_targets=5,
        unhealthy_targets=0,
        successful=successful,
    )


def test_create_returns_brain_runtime() -> None:
    brain = HEOSBrainRuntime.create()

    assert isinstance(brain, HEOSBrainRuntime)


def test_runtime_starts_created() -> None:
    brain = HEOSBrainRuntime.create()

    assert brain.state is BrainRuntimeServiceState.CREATED
    assert not brain.active
    assert not brain.stopped
    assert brain.processed_cycles == 0


def test_start_activates_brain_runtime() -> None:
    brain = HEOSBrainRuntime.create()

    brain.start()

    assert brain.active
    assert brain.state is BrainRuntimeServiceState.ACTIVE


def test_process_runs_brain_cycle() -> None:
    brain = HEOSBrainRuntime.create()
    brain.start()

    result = brain.process(snapshot())

    assert result.cycle == 180
    assert result.rendered


def test_process_counter_is_exposed() -> None:
    brain = HEOSBrainRuntime.create()
    brain.start()

    brain.process(snapshot(cycle=1))
    brain.process(snapshot(cycle=2))

    assert brain.processed_cycles == 2


def test_runtime_state_is_exposed() -> None:
    brain = HEOSBrainRuntime.create()
    brain.start()
    brain.process(snapshot(cycle=180))

    state = brain.runtime_state

    assert state.running
    assert state.has_data
    assert state.cycle == 180


def test_diagnostics_are_exposed() -> None:
    brain = HEOSBrainRuntime.create()
    brain.start()
    brain.process(snapshot())

    report = brain.diagnostics

    assert report.healthy
    assert report.latest_cycle == 180


def test_last_result_is_exposed() -> None:
    brain = HEOSBrainRuntime.create()
    brain.start()

    result = brain.process(snapshot())

    assert brain.last_result is result


def test_stop_stops_brain_runtime() -> None:
    brain = HEOSBrainRuntime.create()
    brain.start()
    brain.process(snapshot())

    brain.stop()

    assert brain.stopped
    assert brain.state is BrainRuntimeServiceState.STOPPED


def test_critical_snapshot_stops_runtime() -> None:
    brain = HEOSBrainRuntime.create()
    brain.start()

    result = brain.process(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert result.stopped
    assert brain.stopped


def test_runtime_rejects_process_before_start() -> None:
    brain = HEOSBrainRuntime.create()

    with pytest.raises(
        RuntimeError,
        match="Cannot process snapshot in service state created",
    ):
        brain.process(snapshot())


def test_runtime_rejects_process_after_stop() -> None:
    brain = HEOSBrainRuntime.create()
    brain.start()
    brain.stop()

    with pytest.raises(
        RuntimeError,
        match="Cannot process snapshot in service state stopped",
    ):
        brain.process(snapshot())


def test_multiple_brains_are_independent() -> None:
    first = HEOSBrainRuntime.create()
    second = HEOSBrainRuntime.create()

    first.start()
    first.process(snapshot(cycle=1))

    assert first.processed_cycles == 1
    assert second.processed_cycles == 0
    assert second.state is BrainRuntimeServiceState.CREATED


def test_facade_keeps_application_api_small() -> None:
    brain = HEOSBrainRuntime.create()

    brain.start()
    result = brain.process(snapshot())
    brain.stop()

    assert result.rendered
    assert brain.processed_cycles == 1
    assert brain.stopped
