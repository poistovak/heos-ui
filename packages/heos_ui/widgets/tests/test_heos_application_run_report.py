from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.heos_application_run_report import HEOSApplicationRunReport
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


def run_and_report(
    snapshots: tuple[BrainRuntimeSnapshot, ...],
) -> tuple[
    HEOSApplicationRuntime,
    HEOSApplicationRunReport,
]:
    application = HEOSApplicationRuntime.create()

    result = HEOSApplicationRuntimeLoop(
        application=application,
    ).run(snapshots)

    report = HEOSApplicationRunReport.capture(
        application,
        result,
        requested=len(snapshots),
    )

    return application, report


def test_empty_run_creates_report() -> None:
    _, report = run_and_report(())

    assert report.requested == 0
    assert report.processed == 0
    assert report.rendered == 0
    assert report.skipped == 0


def test_empty_run_is_empty() -> None:
    _, report = run_and_report(())

    assert report.empty
    assert report.completed
    assert not report.interrupted


def test_empty_run_has_no_cycle_range() -> None:
    _, report = run_and_report(())

    assert report.first_cycle is None
    assert report.last_cycle is None


def test_empty_run_reports_running_application() -> None:
    application, report = run_and_report(())

    assert application.running
    assert report.state is HEOSApplicationState.RUNNING


def test_single_cycle_report() -> None:
    _, report = run_and_report(
        (
            snapshot(cycle=184),
        )
    )

    assert report.processed == 1
    assert report.rendered == 1
    assert report.first_cycle == 184
    assert report.last_cycle == 184


def test_healthy_run_is_completed() -> None:
    _, report = run_and_report(
        (
            snapshot(cycle=1),
            snapshot(cycle=2),
            snapshot(cycle=184),
        )
    )

    assert report.completed
    assert not report.stopped
    assert not report.interrupted


def test_healthy_report_counts_all_cycles() -> None:
    _, report = run_and_report(
        (
            snapshot(cycle=1),
            snapshot(cycle=2),
            snapshot(cycle=3),
        )
    )

    assert report.requested == 3
    assert report.processed == 3
    assert report.rendered == 3
    assert report.skipped == 0


def test_report_tracks_cycle_range() -> None:
    _, report = run_and_report(
        (
            snapshot(cycle=10),
            snapshot(cycle=20),
            snapshot(cycle=184),
        )
    )

    assert report.first_cycle == 10
    assert report.last_cycle == 184


def test_critical_run_reports_stopped_application() -> None:
    application, report = run_and_report(
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

    assert application.stopped
    assert report.state is HEOSApplicationState.STOPPED
    assert report.stopped


def test_critical_run_is_interrupted() -> None:
    _, report = run_and_report(
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

    assert report.interrupted
    assert not report.completed


def test_critical_report_counts_skipped_cycles() -> None:
    _, report = run_and_report(
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

    assert report.requested == 3
    assert report.processed == 1
    assert report.rendered == 0
    assert report.skipped == 2


def test_critical_report_ends_on_failure_cycle() -> None:
    _, report = run_and_report(
        (
            snapshot(
                cycle=184,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=185),
        )
    )

    assert report.first_cycle == 184
    assert report.last_cycle == 184


def test_report_is_immutable_snapshot() -> None:
    application = HEOSApplicationRuntime.create()
    runtime_loop = HEOSApplicationRuntimeLoop(
        application=application,
    )

    result = runtime_loop.run(
        (
            snapshot(cycle=1),
        )
    )

    report = HEOSApplicationRunReport.capture(
        application,
        result,
        requested=1,
    )

    application.tick(
        snapshot(cycle=2)
    )

    assert report.processed == 1
    assert report.last_cycle == 1
    assert report.state is HEOSApplicationState.RUNNING
