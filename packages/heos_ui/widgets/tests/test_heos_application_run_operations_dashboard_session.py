from heos_ui.widgets.heos_application_run_operations_dashboard_session import (
    HEOSApplicationRunOperationsDashboardSession,
)
from heos_ui.widgets.heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsSeverity,
)
from heos_ui.widgets.heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)


def operations_session() -> HEOSApplicationRunOperationsSession:
    return HEOSApplicationRunOperationsSession.create()


def test_dashboard_session_starts_empty() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()

    assert dashboard.history == ()
    assert dashboard.latest is None
    assert dashboard.refresh_count == 0
    assert not dashboard.has_updates


def test_refresh_adds_first_update() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()

    update = dashboard.refresh(
        operations_session()
    )

    assert dashboard.history == (update,)
    assert dashboard.latest is update
    assert dashboard.refresh_count == 1
    assert dashboard.has_updates


def test_first_refresh_has_sequence_one() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()

    update = dashboard.refresh(
        operations_session()
    )

    assert update.sequence == 1


def test_empty_operations_session_renders_idle() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()

    update = dashboard.refresh(
        operations_session()
    )

    assert update.view.status == "IDLE"
    assert update.frame.commands[1].text == "IDLE"
    assert (
        update.frame.severity
        is HEOSApplicationRunOperationsSeverity.NEUTRAL
    )


def test_multiple_refreshes_preserve_order() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()
    operations = operations_session()

    first = dashboard.refresh(operations)
    second = dashboard.refresh(operations)
    third = dashboard.refresh(operations)

    assert dashboard.history == (
        first,
        second,
        third,
    )
    assert dashboard.latest is third
    assert dashboard.refresh_count == 3


def test_controller_sequence_flows_to_history() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()
    operations = operations_session()

    first = dashboard.refresh(operations)
    second = dashboard.refresh(operations)

    assert first.sequence == 1
    assert second.sequence == 2


def test_history_is_tuple_snapshot() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()
    operations = operations_session()

    dashboard.refresh(operations)
    history = dashboard.history

    dashboard.refresh(operations)

    assert isinstance(history, tuple)
    assert len(history) == 1
    assert len(dashboard.history) == 2


def test_previous_dashboard_update_remains_snapshot() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()
    operations = operations_session()

    first = dashboard.refresh(operations)

    dashboard.refresh(operations)

    assert first.sequence == 1
    assert first.statistics.total_updates == 0
    assert first.view.status == "IDLE"
    assert first.frame.commands[1].text == "IDLE"


def test_latest_tracks_last_refresh() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()
    operations = operations_session()

    dashboard.refresh(operations)
    second = dashboard.refresh(operations)

    assert dashboard.latest is second


def test_controller_tracks_latest_update() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()

    update = dashboard.refresh(
        operations_session()
    )

    assert dashboard.controller.latest is update


def test_renderer_count_matches_refresh_count() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()
    operations = operations_session()

    dashboard.refresh(operations)
    dashboard.refresh(operations)
    dashboard.refresh(operations)

    assert dashboard.refresh_count == 3
    assert dashboard.controller.renderer.render_count == 3


def test_clear_removes_dashboard_history() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()

    dashboard.refresh(
        operations_session()
    )
    dashboard.clear()

    assert dashboard.history == ()
    assert dashboard.latest is None
    assert dashboard.refresh_count == 0
    assert not dashboard.has_updates


def test_clear_removes_controller_state() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()

    dashboard.refresh(
        operations_session()
    )
    dashboard.clear()

    assert dashboard.controller.latest is None
    assert dashboard.controller.widget.view is None
    assert dashboard.controller.renderer.latest_frame is None


def test_refresh_after_clear_starts_new_history() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()
    operations = operations_session()

    dashboard.refresh(operations)
    dashboard.clear()

    update = dashboard.refresh(operations)

    assert dashboard.history == (update,)
    assert dashboard.refresh_count == 1


def test_refresh_after_clear_preserves_controller_sequence() -> None:
    dashboard = HEOSApplicationRunOperationsDashboardSession.create()
    operations = operations_session()

    first = dashboard.refresh(operations)
    dashboard.clear()
    second = dashboard.refresh(operations)

    assert first.sequence == 1
    assert second.sequence == 2
    assert dashboard.controller.sequence == 2
