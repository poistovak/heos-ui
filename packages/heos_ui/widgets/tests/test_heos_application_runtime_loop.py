from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.heos_application_runtime import (
    HEOSApplicationRuntime,
    HEOSApplicationState,
)
from heos_ui.widgets.heos_application_runtime_loop import (
    HEOSApplicationRuntimeLoop,
)


def snapshot(
    *,
    cycle: int,
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


def loop() -> HEOSApplicationRuntimeLoop:
    return HEOSApplicationRuntimeLoop(
        application=HEOSApplicationRuntime.create(),
    )


def test_empty_loop_starts_application() -> None:
    runtime_loop = loop()

    result = runtime_loop.run(())

    assert runtime_loop.application.running
    assert result.processed == 0


def test_empty_loop_returns_no_results() -> None:
    result = loop().run(())

    assert result.results == ()
    assert result.last_result is None
    assert result.completed


def test_single_snapshot_is_processed() -> None:
    runtime_loop = loop()

    result = runtime_loop.run(
        (
            snapshot(cycle=182),
        )
    )

    assert result.processed == 1
    assert result.last_result is not None
    assert result.last_result.cycle == 182


def test_multiple_snapshots_are_processed_in_order() -> None:
    runtime_loop = loop()

    result = runtime_loop.run(
        (
            snapshot(cycle=1),
            snapshot(cycle=2),
            snapshot(cycle=3),
        )
    )

    assert tuple(
        item.cycle
        for item in result.results
    ) == (
        1,
        2,
        3,
    )


def test_processed_count_matches_ticks() -> None:
    runtime_loop = loop()

    result = runtime_loop.run(
        (
            snapshot(cycle=1),
            snapshot(cycle=2),
            snapshot(cycle=3),
        )
    )

    assert result.processed == 3
    assert runtime_loop.application.ticks == 3


def test_healthy_loop_completes_without_stop() -> None:
    result = loop().run(
        (
            snapshot(cycle=1),
            snapshot(cycle=2),
        )
    )

    assert result.completed
    assert not result.stopped


def test_critical_snapshot_stops_loop() -> None:
    runtime_loop = loop()

    result = runtime_loop.run(
        (
            snapshot(
                cycle=1,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=2),
        )
    )

    assert result.stopped
    assert result.processed == 1
    assert runtime_loop.application.stopped


def test_later_degraded_snapshot_can_continue_with_caution() -> None:
    result = loop().run(
        (
            snapshot(cycle=1),
            snapshot(
                cycle=2,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=3),
        )
    )

    assert result.processed == 3
    assert not result.stopped
    assert tuple(
        item.cycle
        for item in result.results
    ) == (
        1,
        2,
        3,
    )


def test_loop_can_use_already_running_application() -> None:
    app = HEOSApplicationRuntime.create()
    app.start()

    runtime_loop = HEOSApplicationRuntimeLoop(
        application=app,
    )

    result = runtime_loop.run(
        (
            snapshot(cycle=182),
        )
    )

    assert result.processed == 1
    assert app.ticks == 1


def test_last_result_tracks_final_processed_cycle() -> None:
    result = loop().run(
        (
            snapshot(cycle=10),
            snapshot(cycle=182),
        )
    )

    assert result.last_result is not None
    assert result.last_result.cycle == 182


def test_loop_result_is_snapshot() -> None:
    runtime_loop = loop()

    result = runtime_loop.run(
        (
            snapshot(cycle=1),
        )
    )

    runtime_loop.application.tick(
        snapshot(cycle=2)
    )

    assert result.processed == 1
    assert len(result.results) == 1


def test_application_state_remains_running_after_healthy_loop() -> None:
    runtime_loop = loop()

    runtime_loop.run(
        (
            snapshot(cycle=1),
        )
    )

    assert (
        runtime_loop.application.state
        is HEOSApplicationState.RUNNING
    )

