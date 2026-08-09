from heos_ui.widgets import (
    heos_application_run_operations_dashboard_runtime_history_session as history_session,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_health import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_presenter import (
    HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity,
)
from heos_ui.widgets.heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)

HistorySession = (
    history_session.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySession
)
HistorySessionUpdate = (
    history_session.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySessionUpdate
)


def operations_session() -> HEOSApplicationRunOperationsSession:
    return HEOSApplicationRunOperationsSession.create()


def test_session_starts_empty() -> None:
    session = HistorySession.create()

    assert session.history == ()
    assert session.latest is None
    assert session.refresh_count == 0
    assert not session.has_updates


def test_refresh_returns_session_update() -> None:
    session = HistorySession.create()

    update = session.refresh(
        operations_session()
    )

    assert isinstance(
        update,
        HistorySessionUpdate,
    )


def test_first_refresh_has_sequence_one() -> None:
    session = HistorySession.create()

    update = session.refresh(
        operations_session()
    )

    assert update.sequence == 1


def test_first_refresh_is_recorded() -> None:
    session = HistorySession.create()

    update = session.refresh(
        operations_session()
    )

    assert session.history == (update,)
    assert session.latest is update
    assert session.refresh_count == 1
    assert session.has_updates


def test_refresh_updates_runtime_history_statistics() -> None:
    session = HistorySession.create()

    update = session.refresh(
        operations_session()
    )

    assert update.statistics.total_cycles == 1
    assert update.statistics.latest_cycle == 1


def test_refresh_updates_health() -> None:
    session = HistorySession.create()

    update = session.refresh(
        operations_session()
    )

    assert (
        update.health.health
        is HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.HEALTHY
    )


def test_refresh_updates_presentation() -> None:
    session = HistorySession.create()

    update = session.refresh(
        operations_session()
    )

    assert update.presentation.status == "HEALTHY"
    assert (
        update.presentation.severity
        is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.SUCCESS
    )


def test_refresh_updates_widget_view() -> None:
    session = HistorySession.create()

    update = session.refresh(
        operations_session()
    )

    assert session.widget.view is update.view
    assert update.view.status == "HEALTHY"


def test_refresh_updates_live_renderer() -> None:
    session = HistorySession.create()

    update = session.refresh(
        operations_session()
    )

    assert session.renderer.latest_result is update.frame_result
    assert session.renderer.latest_frame is update.frame_result.frame


def test_multiple_refreshes_preserve_order() -> None:
    session = HistorySession.create()
    operations = operations_session()

    first = session.refresh(operations)
    second = session.refresh(operations)
    third = session.refresh(operations)

    assert session.history == (
        first,
        second,
        third,
    )


def test_multiple_refreshes_increment_sequence() -> None:
    session = HistorySession.create()
    operations = operations_session()

    first = session.refresh(operations)
    second = session.refresh(operations)
    third = session.refresh(operations)

    assert first.sequence == 1
    assert second.sequence == 2
    assert third.sequence == 3


def test_multiple_refreshes_accumulate_runtime_history() -> None:
    session = HistorySession.create()
    operations = operations_session()

    session.refresh(operations)
    session.refresh(operations)
    third = session.refresh(operations)

    assert third.statistics.total_cycles == 3
    assert third.statistics.latest_cycle == 3


def test_previous_update_remains_snapshot() -> None:
    session = HistorySession.create()
    operations = operations_session()

    first = session.refresh(operations)
    session.refresh(operations)

    assert first.sequence == 1
    assert first.statistics.total_cycles == 1
    assert first.presentation.cycles == "Cycles 1"
    assert first.presentation.latest == "Latest cycle 1"


def test_clear_removes_session_history() -> None:
    session = HistorySession.create()

    session.refresh(
        operations_session()
    )
    session.clear()

    assert session.history == ()
    assert session.latest is None
    assert session.refresh_count == 0
    assert not session.has_updates


def test_clear_removes_controller_history() -> None:
    session = HistorySession.create()

    session.refresh(
        operations_session()
    )
    session.clear()

    assert session.controller.history.count == 0
    assert session.controller.latest is None


def test_clear_removes_widget_state() -> None:
    session = HistorySession.create()

    session.refresh(
        operations_session()
    )
    session.clear()

    assert session.widget.view is None


def test_clear_removes_renderer_state() -> None:
    session = HistorySession.create()

    session.refresh(
        operations_session()
    )
    session.clear()

    assert session.renderer.latest_result is None
    assert session.renderer.latest_frame is None


def test_refresh_after_clear_starts_new_session_history() -> None:
    session = HistorySession.create()
    operations = operations_session()

    session.refresh(operations)
    session.clear()

    update = session.refresh(operations)

    assert session.history == (update,)
    assert update.sequence == 1
    assert session.refresh_count == 1


def test_runtime_cycle_number_continues_after_clear() -> None:
    session = HistorySession.create()
    operations = operations_session()

    first = session.refresh(operations)
    session.clear()
    second = session.refresh(operations)

    assert first.statistics.latest_cycle == 1
    assert second.statistics.latest_cycle == 2
