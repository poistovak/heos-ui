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
from heos_ui.widgets.heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)
from heos_ui.widgets.heos_application_run_operations_session_statistics import (
    HEOSApplicationRunOperationsSessionStatistics,
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


def live_session() -> HEOSApplicationRunLiveSession:
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
    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        HEOSApplicationRunOperationsSession.create()
    )

    assert stats.total_updates == 0
    assert stats.idle_updates == 0
    assert stats.healthy_updates == 0
    assert stats.degraded_updates == 0


def test_empty_session_has_no_frames() -> None:
    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        HEOSApplicationRunOperationsSession.create()
    )

    assert stats.rendered_frames == 0
    assert stats.latest_sequence is None
    assert stats.empty
    assert not stats.healthy


def test_idle_update_is_counted() -> None:
    operations = HEOSApplicationRunOperationsSession.create()

    operations.refresh(live_session())

    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        operations
    )

    assert stats.total_updates == 1
    assert stats.idle_updates == 1
    assert stats.active_updates == 0


def test_healthy_update_is_counted() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    publish(
        live,
        (
            snapshot(cycle=208),
        ),
    )
    operations.refresh(live)

    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        operations
    )

    assert stats.total_updates == 1
    assert stats.healthy_updates == 1
    assert stats.degraded_updates == 0


def test_degraded_update_is_counted() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    publish(
        live,
        (
            snapshot(
                cycle=208,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
        ),
    )
    operations.refresh(live)

    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        operations
    )

    assert stats.total_updates == 1
    assert stats.degraded_updates == 1
    assert stats.healthy_updates == 0


def test_multiple_update_types_are_aggregated() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    operations.refresh(live)

    publish(
        live,
        (
            snapshot(cycle=1),
        ),
    )
    operations.refresh(live)

    degraded = live_session()
    publish(
        degraded,
        (
            snapshot(
                cycle=208,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
        ),
    )
    operations.refresh(degraded)

    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        operations
    )

    assert stats.total_updates == 3
    assert stats.idle_updates == 1
    assert stats.healthy_updates == 1
    assert stats.degraded_updates == 1


def test_active_updates_exclude_idle() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    operations.refresh(live)

    publish(
        live,
        (
            snapshot(cycle=208),
        ),
    )
    operations.refresh(live)

    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        operations
    )

    assert stats.total_updates == 2
    assert stats.active_updates == 1


def test_every_refresh_produces_rendered_frame() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    operations.refresh(live)
    operations.refresh(live)
    operations.refresh(live)

    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        operations
    )

    assert stats.rendered_frames == 3


def test_latest_sequence_tracks_last_update() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    operations.refresh(live)
    operations.refresh(live)

    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        operations
    )

    assert stats.latest_sequence == 2


def test_session_without_degradation_is_healthy() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    operations.refresh(live)

    publish(
        live,
        (
            snapshot(cycle=208),
        ),
    )
    operations.refresh(live)

    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        operations
    )

    assert stats.healthy


def test_degraded_update_makes_statistics_unhealthy() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    publish(
        live,
        (
            snapshot(
                cycle=208,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
        ),
    )
    operations.refresh(live)

    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        operations
    )

    assert not stats.healthy


def test_statistics_are_snapshot() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    operations.refresh(live)

    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        operations
    )

    operations.refresh(live)

    assert stats.total_updates == 1
    assert stats.rendered_frames == 1
    assert stats.latest_sequence == 1


def test_clear_produces_empty_statistics() -> None:
    operations = HEOSApplicationRunOperationsSession.create()

    operations.refresh(live_session())
    operations.clear()

    stats = HEOSApplicationRunOperationsSessionStatistics.capture(
        operations
    )

    assert stats.empty
    assert stats.total_updates == 0
    assert stats.latest_sequence is None
