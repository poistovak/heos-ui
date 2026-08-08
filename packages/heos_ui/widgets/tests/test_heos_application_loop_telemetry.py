from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.heos_application_loop_telemetry import (
    HEOSApplicationLoopTelemetry,
)
from heos_ui.widgets.heos_application_runtime import HEOSApplicationRuntime
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


def run(
    snapshots: tuple[BrainRuntimeSnapshot, ...],
):
    runtime_loop = HEOSApplicationRuntimeLoop(
        application=HEOSApplicationRuntime.create(),
    )
    return runtime_loop.run(snapshots)


def test_empty_result_has_zero_telemetry() -> None:
    result = run(())

    telemetry = HEOSApplicationLoopTelemetry.capture(
        result,
        requested=0,
    )

    assert telemetry.requested == 0
    assert telemetry.processed == 0
    assert telemetry.rendered == 0


def test_empty_result_has_no_cycle_range() -> None:
    telemetry = HEOSApplicationLoopTelemetry.capture(
        run(()),
        requested=0,
    )

    assert telemetry.first_cycle is None
    assert telemetry.last_cycle is None


def test_empty_result_is_completed() -> None:
    telemetry = HEOSApplicationLoopTelemetry.capture(
        run(()),
        requested=0,
    )

    assert telemetry.completed
    assert not telemetry.early_stop
    assert telemetry.skipped == 0


def test_single_cycle_is_captured() -> None:
    telemetry = HEOSApplicationLoopTelemetry.capture(
        run(
            (
                snapshot(cycle=183),
            )
        ),
        requested=1,
    )

    assert telemetry.processed == 1
    assert telemetry.rendered == 1
    assert telemetry.first_cycle == 183
    assert telemetry.last_cycle == 183


def test_multiple_cycles_capture_range() -> None:
    telemetry = HEOSApplicationLoopTelemetry.capture(
        run(
            (
                snapshot(cycle=10),
                snapshot(cycle=20),
                snapshot(cycle=183),
            )
        ),
        requested=3,
    )

    assert telemetry.first_cycle == 10
    assert telemetry.last_cycle == 183


def test_healthy_run_is_completed() -> None:
    telemetry = HEOSApplicationLoopTelemetry.capture(
        run(
            (
                snapshot(cycle=1),
                snapshot(cycle=2),
                snapshot(cycle=3),
            )
        ),
        requested=3,
    )

    assert telemetry.completed
    assert not telemetry.stopped
    assert not telemetry.early_stop
    assert telemetry.skipped == 0


def test_rendered_count_matches_healthy_cycles() -> None:
    telemetry = HEOSApplicationLoopTelemetry.capture(
        run(
            (
                snapshot(cycle=1),
                snapshot(cycle=2),
                snapshot(cycle=3),
            )
        ),
        requested=3,
    )

    assert telemetry.rendered == 3


def test_critical_first_cycle_reports_early_stop() -> None:
    telemetry = HEOSApplicationLoopTelemetry.capture(
        run(
            (
                snapshot(
                    cycle=1,
                    health=SystemHealth.DEGRADED,
                    successful=False,
                ),
                snapshot(cycle=2),
                snapshot(cycle=3),
            )
        ),
        requested=3,
    )

    assert telemetry.stopped
    assert telemetry.early_stop
    assert telemetry.processed == 1


def test_critical_cycle_is_not_rendered() -> None:
    telemetry = HEOSApplicationLoopTelemetry.capture(
        run(
            (
                snapshot(
                    cycle=1,
                    health=SystemHealth.DEGRADED,
                    successful=False,
                ),
                snapshot(cycle=2),
            )
        ),
        requested=2,
    )

    assert telemetry.rendered == 0


def test_early_stop_reports_skipped_cycles() -> None:
    telemetry = HEOSApplicationLoopTelemetry.capture(
        run(
            (
                snapshot(
                    cycle=1,
                    health=SystemHealth.DEGRADED,
                    successful=False,
                ),
                snapshot(cycle=2),
                snapshot(cycle=3),
            )
        ),
        requested=3,
    )

    assert telemetry.processed == 1
    assert telemetry.skipped == 2


def test_early_stop_last_cycle_is_failure_cycle() -> None:
    telemetry = HEOSApplicationLoopTelemetry.capture(
        run(
            (
                snapshot(
                    cycle=10,
                    health=SystemHealth.DEGRADED,
                    successful=False,
                ),
                snapshot(cycle=20),
            )
        ),
        requested=2,
    )

    assert telemetry.first_cycle == 10
    assert telemetry.last_cycle == 10


def test_telemetry_is_snapshot_of_loop_result() -> None:
    result = run(
        (
            snapshot(cycle=1),
        )
    )

    telemetry = HEOSApplicationLoopTelemetry.capture(
        result,
        requested=1,
    )

    assert telemetry.processed == 1
    assert telemetry.first_cycle == 1
    assert telemetry.last_cycle == 1
