from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.heos_application_run_live_bridge import (
    HEOSApplicationRunLiveBridge,
)
from heos_ui.widgets.heos_application_run_live_controller import (
    HEOSApplicationRunLiveController,
)
from heos_ui.widgets.heos_application_run_live_renderer import (
    HEOSApplicationRunLiveRenderer,
)
from heos_ui.widgets.heos_application_run_live_session import (
    HEOSApplicationRunLiveSession,
)
from heos_ui.widgets.heos_application_run_live_session_statistics import (
    HEOSApplicationRunLiveSessionStatistics,
)
from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunPresenter,
)
from heos_ui.widgets.heos_application_run_status import (
    HEOSApplicationRunStatusWidget,
)
from heos_ui.widgets.heos_application_run_status_binding import (
    HEOSApplicationRunStatusBinding,
)
from heos_ui.widgets.heos_application_run_status_controller import (
    HEOSApplicationRunStatusController,
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


def session() -> HEOSApplicationRunLiveSession:
    return HEOSApplicationRunLiveSession(
        bridge=HEOSApplicationRunLiveBridge(
            controller=HEOSApplicationRunLiveController(
                controller=HEOSApplicationRunStatusController(
                    binding=HEOSApplicationRunStatusBinding(
                        presenter=HEOSApplicationRunPresenter(),
                        widget=HEOSApplicationRunStatusWidget(),
                    )
                ),
                renderer=HEOSApplicationRunLiveRenderer.create(),
            )
        )
    )


def publish(
    live: HEOSApplicationRunLiveSession,
    snapshots: tuple[BrainRuntimeSnapshot, ...],
) -> None:
    application = HEOSApplicationRuntime.create()

    result = HEOSApplicationRuntimeLoop(
        application=application,
    ).run(snapshots)

    live.publish(
        application,
        result,
        requested=len(snapshots),
    )


def test_empty_session_has_zero_statistics() -> None:
    stats = HEOSApplicationRunLiveSessionStatistics.capture(
        session()
    )

    assert stats.total_runs == 0
    assert stats.completed_runs == 0
    assert stats.interrupted_runs == 0
    assert stats.idle_runs == 0


def test_empty_session_has_zero_totals() -> None:
    stats = HEOSApplicationRunLiveSessionStatistics.capture(
        session()
    )

    assert stats.processed == 0
    assert stats.rendered == 0
    assert stats.skipped == 0


def test_empty_session_has_no_latest_sequence() -> None:
    stats = HEOSApplicationRunLiveSessionStatistics.capture(
        session()
    )

    assert stats.latest_sequence is None
    assert stats.empty
    assert not stats.successful


def test_completed_run_is_counted() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=197),
        ),
    )

    stats = HEOSApplicationRunLiveSessionStatistics.capture(live)

    assert stats.total_runs == 1
    assert stats.completed_runs == 1
    assert stats.interrupted_runs == 0
    assert stats.idle_runs == 0


def test_completed_run_counts_processed_and_rendered() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=1),
            snapshot(cycle=197),
        ),
    )

    stats = HEOSApplicationRunLiveSessionStatistics.capture(live)

    assert stats.processed == 2
    assert stats.rendered == 2
    assert stats.skipped == 0


def test_idle_run_is_counted() -> None:
    live = session()

    publish(live, ())

    stats = HEOSApplicationRunLiveSessionStatistics.capture(live)

    assert stats.total_runs == 1
    assert stats.idle_runs == 1
    assert stats.completed_runs == 0
    assert stats.active_runs == 0


def test_interrupted_run_is_counted() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(
                cycle=197,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=198),
            snapshot(cycle=199),
        ),
    )

    stats = HEOSApplicationRunLiveSessionStatistics.capture(live)

    assert stats.total_runs == 1
    assert stats.interrupted_runs == 1
    assert stats.completed_runs == 0
    assert stats.skipped == 2


def test_multiple_run_types_are_aggregated() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=1),
            snapshot(cycle=2),
        ),
    )
    publish(live, ())
    publish(
        live,
        (
            snapshot(
                cycle=3,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=4),
        ),
    )

    stats = HEOSApplicationRunLiveSessionStatistics.capture(live)

    assert stats.total_runs == 3
    assert stats.completed_runs == 1
    assert stats.idle_runs == 1
    assert stats.interrupted_runs == 1


def test_multiple_runs_aggregate_cycle_counts() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=1),
            snapshot(cycle=2),
        ),
    )
    publish(
        live,
        (
            snapshot(cycle=3),
        ),
    )

    stats = HEOSApplicationRunLiveSessionStatistics.capture(live)

    assert stats.processed == 3
    assert stats.rendered == 3
    assert stats.skipped == 0


def test_active_runs_exclude_idle_runs() -> None:
    live = session()

    publish(live, ())
    publish(
        live,
        (
            snapshot(cycle=197),
        ),
    )

    stats = HEOSApplicationRunLiveSessionStatistics.capture(live)

    assert stats.total_runs == 2
    assert stats.active_runs == 1


def test_successful_session_has_no_interruptions() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=1),
        ),
    )
    publish(
        live,
        (
            snapshot(cycle=197),
        ),
    )

    stats = HEOSApplicationRunLiveSessionStatistics.capture(live)

    assert stats.successful
    assert stats.interrupted_runs == 0


def test_interruption_makes_session_unsuccessful() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=1),
        ),
    )
    publish(
        live,
        (
            snapshot(
                cycle=197,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
        ),
    )

    stats = HEOSApplicationRunLiveSessionStatistics.capture(live)

    assert not stats.successful
    assert stats.interrupted_runs == 1


def test_latest_sequence_tracks_last_run() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=1),
        ),
    )
    publish(
        live,
        (
            snapshot(cycle=197),
        ),
    )

    stats = HEOSApplicationRunLiveSessionStatistics.capture(live)

    assert stats.latest_sequence == 2


def test_statistics_are_snapshot_of_session() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=1),
        ),
    )

    stats = HEOSApplicationRunLiveSessionStatistics.capture(live)

    publish(
        live,
        (
            snapshot(cycle=197),
        ),
    )

    assert stats.total_runs == 1
    assert stats.processed == 1
    assert stats.latest_sequence == 1
