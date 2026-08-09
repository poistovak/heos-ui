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
from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunPresenter,
)
from heos_ui.widgets.heos_application_run_session_operations_controller import (
    HEOSApplicationRunSessionOperationsUpdate,
)
from heos_ui.widgets.heos_application_run_session_presenter import (
    HEOSApplicationRunSessionSeverity,
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


def test_operations_session_starts_empty() -> None:
    operations = HEOSApplicationRunOperationsSession.create()

    assert operations.history == ()
    assert operations.latest is None
    assert operations.update_count == 0
    assert not operations.has_updates


def test_refresh_returns_operations_update() -> None:
    operations = HEOSApplicationRunOperationsSession.create()

    update = operations.refresh(live_session())

    assert isinstance(
        update,
        HEOSApplicationRunSessionOperationsUpdate,
    )


def test_first_refresh_is_stored() -> None:
    operations = HEOSApplicationRunOperationsSession.create()

    update = operations.refresh(live_session())

    assert operations.history == (update,)
    assert operations.latest is update
    assert operations.update_count == 1
    assert operations.has_updates


def test_empty_live_session_creates_idle_update() -> None:
    operations = HEOSApplicationRunOperationsSession.create()

    update = operations.refresh(live_session())

    assert update.view.status == "IDLE"
    assert update.frame.commands[1].text == "IDLE"
    assert (
        update.frame.severity
        is HEOSApplicationRunSessionSeverity.NEUTRAL
    )


def test_healthy_live_session_creates_healthy_update() -> None:
    live = live_session()
    publish(
        live,
        (
            snapshot(cycle=207),
        ),
    )

    update = HEOSApplicationRunOperationsSession.create().refresh(
        live
    )

    assert update.health.summary.healthy
    assert update.view.status == "HEALTHY"
    assert (
        update.frame.severity
        is HEOSApplicationRunSessionSeverity.SUCCESS
    )


def test_degraded_live_session_creates_warning_update() -> None:
    live = live_session()
    publish(
        live,
        (
            snapshot(
                cycle=207,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=208),
        ),
    )

    update = HEOSApplicationRunOperationsSession.create().refresh(
        live
    )

    assert update.health.summary.degraded
    assert update.view.status == "DEGRADED"
    assert (
        update.frame.severity
        is HEOSApplicationRunSessionSeverity.WARNING
    )


def test_multiple_refreshes_preserve_order() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    first = operations.refresh(live)

    publish(
        live,
        (
            snapshot(cycle=207),
        ),
    )
    second = operations.refresh(live)

    assert operations.history == (first, second)
    assert operations.latest is second
    assert operations.update_count == 2


def test_controller_sequence_flows_to_history() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    first = operations.refresh(live)
    second = operations.refresh(live)

    assert first.sequence == 1
    assert second.sequence == 2


def test_history_is_tuple_snapshot() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    operations.refresh(live)
    history = operations.history
    operations.refresh(live)

    assert isinstance(history, tuple)
    assert len(history) == 1
    assert len(operations.history) == 2


def test_previous_update_remains_snapshot() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    first = operations.refresh(live)

    publish(
        live,
        (
            snapshot(cycle=207),
        ),
    )
    operations.refresh(live)

    assert first.view.status == "IDLE"
    assert first.frame.commands[1].text == "IDLE"
    assert first.sequence == 1


def test_live_session_change_is_visible_on_refresh() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    first = operations.refresh(live)

    publish(
        live,
        (
            snapshot(cycle=207),
        ),
    )

    second = operations.refresh(live)

    assert first.health.statistics.total_runs == 0
    assert second.health.statistics.total_runs == 1
    assert second.view.status == "HEALTHY"


def test_clear_removes_operations_history() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    operations.refresh(live)
    operations.clear()

    assert operations.history == ()
    assert operations.latest is None
    assert operations.update_count == 0
    assert not operations.has_updates


def test_clear_removes_controller_live_state() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    operations.refresh(live)
    operations.clear()

    assert operations.controller.latest is None
    assert operations.controller.widget.view is None
    assert operations.controller.renderer.latest_frame is None


def test_refresh_after_clear_starts_new_history() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    operations.refresh(live)
    operations.clear()

    update = operations.refresh(live)

    assert operations.history == (update,)
    assert operations.update_count == 1


def test_refresh_after_clear_preserves_controller_sequence() -> None:
    operations = HEOSApplicationRunOperationsSession.create()
    live = live_session()

    first = operations.refresh(live)
    operations.clear()
    second = operations.refresh(live)

    assert first.sequence == 1
    assert second.sequence == 2
    assert operations.controller.sequence == 2
