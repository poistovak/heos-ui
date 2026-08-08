import pytest
from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.heos_application_runtime import (
    HEOSApplicationRuntime,
    HEOSApplicationState,
)


def snapshot(
    *,
    cycle: int = 181,
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


def test_application_starts_created() -> None:
    app = HEOSApplicationRuntime.create()

    assert app.state is HEOSApplicationState.CREATED
    assert not app.running
    assert not app.stopped
    assert app.ticks == 0


def test_start_moves_application_to_running() -> None:
    app = HEOSApplicationRuntime.create()

    app.start()

    assert app.state is HEOSApplicationState.RUNNING
    assert app.running


def test_start_activates_brain() -> None:
    app = HEOSApplicationRuntime.create()

    app.start()

    assert app.brain.active


def test_tick_processes_snapshot() -> None:
    app = HEOSApplicationRuntime.create()
    app.start()

    result = app.tick(snapshot())

    assert result.cycle == 181
    assert result.rendered


def test_tick_counter_increments() -> None:
    app = HEOSApplicationRuntime.create()
    app.start()

    app.tick(snapshot(cycle=1))
    app.tick(snapshot(cycle=2))

    assert app.ticks == 2


def test_last_result_is_exposed() -> None:
    app = HEOSApplicationRuntime.create()
    app.start()

    result = app.tick(snapshot())

    assert app.last_result is result


def test_multiple_ticks_keep_application_running() -> None:
    app = HEOSApplicationRuntime.create()
    app.start()

    app.tick(snapshot(cycle=1))
    app.tick(snapshot(cycle=181))

    assert app.running
    assert app.brain.active
    assert app.ticks == 2


def test_manual_stop_stops_application_and_brain() -> None:
    app = HEOSApplicationRuntime.create()
    app.start()
    app.tick(snapshot())

    app.stop()

    assert app.stopped
    assert app.brain.stopped


def test_critical_brain_cycle_stops_application() -> None:
    app = HEOSApplicationRuntime.create()
    app.start()

    result = app.tick(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert result.stopped
    assert app.stopped
    assert app.brain.stopped


def test_critical_tick_is_counted() -> None:
    app = HEOSApplicationRuntime.create()
    app.start()

    app.tick(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert app.ticks == 1


def test_tick_before_start_is_rejected() -> None:
    app = HEOSApplicationRuntime.create()

    with pytest.raises(
        RuntimeError,
        match="Cannot tick application in state created",
    ):
        app.tick(snapshot())


def test_tick_after_stop_is_rejected() -> None:
    app = HEOSApplicationRuntime.create()
    app.start()
    app.stop()

    with pytest.raises(
        RuntimeError,
        match="Cannot tick application in state stopped",
    ):
        app.tick(snapshot())


def test_application_cannot_start_twice() -> None:
    app = HEOSApplicationRuntime.create()
    app.start()

    with pytest.raises(
        RuntimeError,
        match="Cannot start application from state running",
    ):
        app.start()


def test_application_cannot_stop_before_start() -> None:
    app = HEOSApplicationRuntime.create()

    with pytest.raises(
        RuntimeError,
        match="Cannot stop application from state created",
    ):
        app.stop()


def test_independent_applications_have_independent_brains() -> None:
    first = HEOSApplicationRuntime.create()
    second = HEOSApplicationRuntime.create()

    first.start()
    first.tick(snapshot(cycle=1))

    assert first.ticks == 1
    assert second.ticks == 0
    assert second.state is HEOSApplicationState.CREATED
    assert second.brain.processed_cycles == 0
