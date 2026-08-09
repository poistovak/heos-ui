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
from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunPresenter,
)
from heos_ui.widgets.heos_application_run_session_operations_controller import (
    HEOSApplicationRunSessionOperationsController,
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


def test_controller_starts_empty() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()

    assert controller.latest is None
    assert controller.sequence == 0
    assert not controller.has_update


def test_update_returns_operations_update() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()

    update = controller.update(session())

    assert isinstance(
        update,
        HEOSApplicationRunSessionOperationsUpdate,
    )


def test_empty_session_becomes_idle() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()

    update = controller.update(session())

    assert update.view.status == "IDLE"
    assert update.frame.commands[1].text == "IDLE"
    assert (
        update.frame.severity
        is HEOSApplicationRunSessionSeverity.NEUTRAL
    )


def test_healthy_session_flows_through_controller() -> None:
    live = session()
    publish(
        live,
        (
            snapshot(cycle=206),
        ),
    )

    update = (
        HEOSApplicationRunSessionOperationsController.create()
        .update(live)
    )

    assert update.health.summary.healthy
    assert update.view.status == "HEALTHY"
    assert update.frame.commands[1].text == "HEALTHY"


def test_degraded_session_flows_through_controller() -> None:
    live = session()
    publish(
        live,
        (
            snapshot(
                cycle=206,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=207),
        ),
    )

    update = (
        HEOSApplicationRunSessionOperationsController.create()
        .update(live)
    )

    assert update.health.summary.degraded
    assert update.view.status == "DEGRADED"
    assert update.frame.commands[1].text == "DEGRADED"
    assert (
        update.frame.severity
        is HEOSApplicationRunSessionSeverity.WARNING
    )


def test_first_update_has_sequence_one() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()

    update = controller.update(session())

    assert update.sequence == 1
    assert controller.sequence == 1


def test_sequence_increments() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()
    live = session()

    first = controller.update(live)
    second = controller.update(live)

    assert first.sequence == 1
    assert second.sequence == 2
    assert controller.sequence == 2


def test_latest_tracks_last_update() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()
    live = session()

    controller.update(live)
    second = controller.update(live)

    assert controller.latest is second
    assert controller.has_update


def test_widget_tracks_latest_view() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()
    live = session()

    update = controller.update(live)

    assert controller.widget.view is update.view


def test_renderer_tracks_latest_frame() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()
    live = session()

    update = controller.update(live)

    assert controller.renderer.latest_frame is update.frame


def test_renderer_count_tracks_updates() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()
    live = session()

    controller.update(live)
    controller.update(live)

    assert controller.renderer.render_count == 2


def test_session_change_reaches_next_update() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()
    live = session()

    first = controller.update(live)

    publish(
        live,
        (
            snapshot(cycle=206),
        ),
    )

    second = controller.update(live)

    assert first.view.status == "IDLE"
    assert second.view.status == "HEALTHY"
    assert second.health.statistics.total_runs == 1


def test_previous_update_remains_snapshot() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()
    live = session()

    first = controller.update(live)

    publish(
        live,
        (
            snapshot(cycle=206),
        ),
    )
    controller.update(live)

    assert first.sequence == 1
    assert first.view.status == "IDLE"
    assert first.frame.commands[1].text == "IDLE"


def test_clear_removes_live_state() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()

    controller.update(session())
    controller.clear()

    assert controller.latest is None
    assert not controller.has_update
    assert controller.widget.view is None
    assert controller.renderer.latest_frame is None


def test_clear_preserves_sequence_and_render_count() -> None:
    controller = HEOSApplicationRunSessionOperationsController.create()
    live = session()

    controller.update(live)
    controller.clear()

    update = controller.update(live)

    assert update.sequence == 2
    assert controller.sequence == 2
    assert controller.renderer.render_count == 2
