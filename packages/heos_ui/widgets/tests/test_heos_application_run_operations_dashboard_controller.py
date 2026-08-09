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
from heos_ui.widgets.heos_application_run_operations_dashboard_controller import (
    HEOSApplicationRunOperationsDashboardController,
    HEOSApplicationRunOperationsDashboardUpdate,
)
from heos_ui.widgets.heos_application_run_operations_health import (
    HEOSApplicationRunOperationsHealth,
)
from heos_ui.widgets.heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsSeverity,
)
from heos_ui.widgets.heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
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


def operations_session() -> HEOSApplicationRunOperationsSession:
    return HEOSApplicationRunOperationsSession.create()


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


def test_dashboard_controller_starts_empty() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()

    assert controller.latest is None
    assert controller.sequence == 0
    assert not controller.has_update


def test_update_returns_dashboard_update() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()

    update = controller.update(
        operations_session()
    )

    assert isinstance(
        update,
        HEOSApplicationRunOperationsDashboardUpdate,
    )


def test_empty_session_produces_empty_health() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()

    update = controller.update(
        operations_session()
    )

    assert update.statistics.empty
    assert (
        update.health.health
        is HEOSApplicationRunOperationsHealth.EMPTY
    )


def test_empty_session_produces_idle_view() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()

    update = controller.update(
        operations_session()
    )

    assert update.presentation.status == "IDLE"
    assert update.view.status == "IDLE"
    assert (
        update.view.severity
        is HEOSApplicationRunOperationsSeverity.NEUTRAL
    )


def test_empty_session_produces_idle_frame() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()

    update = controller.update(
        operations_session()
    )

    assert update.frame.commands[1].text == "IDLE"
    assert update.frame.command_count == 5


def test_first_update_has_sequence_one() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()

    update = controller.update(
        operations_session()
    )

    assert update.sequence == 1
    assert controller.sequence == 1


def test_sequence_increments() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()
    operations = operations_session()

    first = controller.update(operations)
    second = controller.update(operations)

    assert first.sequence == 1
    assert second.sequence == 2
    assert controller.sequence == 2


def test_latest_tracks_last_update() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()
    operations = operations_session()

    controller.update(operations)
    second = controller.update(operations)

    assert controller.latest is second
    assert controller.has_update


def test_widget_tracks_latest_view() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()

    update = controller.update(
        operations_session()
    )

    assert controller.widget.view is update.view


def test_renderer_tracks_latest_frame() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()

    update = controller.update(
        operations_session()
    )

    assert controller.renderer.latest_frame is update.frame


def test_renderer_count_tracks_dashboard_updates() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()
    operations = operations_session()

    controller.update(operations)
    controller.update(operations)

    assert controller.renderer.render_count == 2


def test_session_refresh_reaches_dashboard() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()
    operations = operations_session()

    first = controller.update(operations)

    operations.refresh(
        live_session()
    )

    second = controller.update(operations)

    assert first.statistics.total_updates == 0
    assert second.statistics.total_updates == 1
    assert second.presentation.updates == "Updates 1"


def test_previous_dashboard_update_remains_snapshot() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()
    operations = operations_session()

    first = controller.update(operations)
    controller.update(operations)

    assert first.sequence == 1
    assert first.statistics.total_updates == 0
    assert first.frame.commands[1].text == "IDLE"


def test_clear_removes_dashboard_state() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()

    controller.update(
        operations_session()
    )
    controller.clear()

    assert controller.latest is None
    assert not controller.has_update
    assert controller.widget.view is None
    assert controller.renderer.latest_frame is None


def test_clear_preserves_sequence_and_render_count() -> None:
    controller = HEOSApplicationRunOperationsDashboardController.create()
    operations = operations_session()

    controller.update(operations)
    controller.clear()
    update = controller.update(operations)

    assert update.sequence == 2
    assert controller.sequence == 2
    assert controller.renderer.render_count == 2
