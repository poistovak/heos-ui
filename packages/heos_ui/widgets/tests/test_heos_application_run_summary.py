from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.heos_application_run_report import HEOSApplicationRunReport
from heos_ui.widgets.heos_application_run_summary import (
    HEOSApplicationRunStatus,
    HEOSApplicationRunSummary,
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


def summary(
    snapshots: tuple[BrainRuntimeSnapshot, ...],
) -> HEOSApplicationRunSummary:
    application = HEOSApplicationRuntime.create()

    result = HEOSApplicationRuntimeLoop(
        application=application,
    ).run(snapshots)

    report = HEOSApplicationRunReport.capture(
        application,
        result,
        requested=len(snapshots),
    )

    return HEOSApplicationRunSummary.from_report(report)


def test_empty_run_has_empty_status() -> None:
    result = summary(())

    assert result.status is HEOSApplicationRunStatus.EMPTY
    assert not result.successful
    assert not result.has_cycles


def test_empty_run_has_stable_headline() -> None:
    result = summary(())

    assert result.headline == "No application cycles were processed."


def test_empty_run_has_no_cycle_range() -> None:
    result = summary(())

    assert result.cycle_range is None
    assert result.first_cycle is None
    assert result.last_cycle is None


def test_completed_run_has_completed_status() -> None:
    result = summary(
        (
            snapshot(cycle=1),
            snapshot(cycle=2),
        )
    )

    assert result.status is HEOSApplicationRunStatus.COMPLETED
    assert result.successful
    assert result.has_cycles


def test_completed_run_has_stable_headline() -> None:
    result = summary(
        (
            snapshot(cycle=1),
            snapshot(cycle=2),
        )
    )

    assert result.headline == "Application run completed with 2 cycles."


def test_completed_run_preserves_counts() -> None:
    result = summary(
        (
            snapshot(cycle=1),
            snapshot(cycle=2),
            snapshot(cycle=3),
        )
    )

    assert result.processed == 3
    assert result.rendered == 3
    assert result.skipped == 0


def test_completed_run_exposes_cycle_range() -> None:
    result = summary(
        (
            snapshot(cycle=10),
            snapshot(cycle=185),
        )
    )

    assert result.first_cycle == 10
    assert result.last_cycle == 185
    assert result.cycle_range == (10, 185)


def test_interrupted_run_has_interrupted_status() -> None:
    result = summary(
        (
            snapshot(
                cycle=1,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=2),
            snapshot(cycle=3),
        )
    )

    assert result.status is HEOSApplicationRunStatus.INTERRUPTED
    assert not result.successful
    assert result.has_cycles


def test_interrupted_run_has_stable_headline() -> None:
    result = summary(
        (
            snapshot(
                cycle=1,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=2),
        )
    )

    assert result.headline == "Application run interrupted after 1 cycles."


def test_interrupted_run_preserves_counts() -> None:
    result = summary(
        (
            snapshot(
                cycle=1,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=2),
            snapshot(cycle=3),
        )
    )

    assert result.processed == 1
    assert result.rendered == 0
    assert result.skipped == 2


def test_interrupted_cycle_range_ends_at_failure() -> None:
    result = summary(
        (
            snapshot(
                cycle=185,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=186),
        )
    )

    assert result.cycle_range == (185, 185)


def test_summary_is_immutable_snapshot() -> None:
    application = HEOSApplicationRuntime.create()
    runtime_loop = HEOSApplicationRuntimeLoop(
        application=application,
    )

    loop_result = runtime_loop.run(
        (
            snapshot(cycle=1),
        )
    )

    report = HEOSApplicationRunReport.capture(
        application,
        loop_result,
        requested=1,
    )

    result = HEOSApplicationRunSummary.from_report(report)

    application.tick(snapshot(cycle=2))

    assert result.processed == 1
    assert result.cycle_range == (1, 1)
