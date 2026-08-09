from heos_ui.widgets.heos_application_run_operations_dashboard_session import (
    HEOSApplicationRunOperationsDashboardSession,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_statistics import (
    HEOSApplicationRunOperationsDashboardStatistics,
)
from heos_ui.widgets.heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)


def dashboard_session() -> HEOSApplicationRunOperationsDashboardSession:
    return HEOSApplicationRunOperationsDashboardSession.create()


def operations_session() -> HEOSApplicationRunOperationsSession:
    return HEOSApplicationRunOperationsSession.create()


def test_empty_dashboard_has_zero_statistics() -> None:
    statistics = HEOSApplicationRunOperationsDashboardStatistics.capture(
        dashboard_session()
    )

    assert statistics.total_refreshes == 0
    assert statistics.idle_refreshes == 0
    assert statistics.healthy_refreshes == 0
    assert statistics.degraded_refreshes == 0


def test_empty_dashboard_has_no_frames() -> None:
    statistics = HEOSApplicationRunOperationsDashboardStatistics.capture(
        dashboard_session()
    )

    assert statistics.rendered_frames == 0
    assert statistics.latest_sequence is None
    assert statistics.empty
    assert not statistics.healthy


def test_idle_refresh_is_counted() -> None:
    dashboard = dashboard_session()

    dashboard.refresh(
        operations_session()
    )

    statistics = HEOSApplicationRunOperationsDashboardStatistics.capture(
        dashboard
    )

    assert statistics.total_refreshes == 1
    assert statistics.idle_refreshes == 1
    assert statistics.active_refreshes == 0


def test_multiple_idle_refreshes_are_counted() -> None:
    dashboard = dashboard_session()
    operations = operations_session()

    dashboard.refresh(operations)
    dashboard.refresh(operations)
    dashboard.refresh(operations)

    statistics = HEOSApplicationRunOperationsDashboardStatistics.capture(
        dashboard
    )

    assert statistics.total_refreshes == 3
    assert statistics.idle_refreshes == 3


def test_every_dashboard_refresh_produces_frame() -> None:
    dashboard = dashboard_session()
    operations = operations_session()

    dashboard.refresh(operations)
    dashboard.refresh(operations)
    dashboard.refresh(operations)

    statistics = HEOSApplicationRunOperationsDashboardStatistics.capture(
        dashboard
    )

    assert statistics.rendered_frames == 3


def test_latest_sequence_tracks_last_refresh() -> None:
    dashboard = dashboard_session()
    operations = operations_session()

    dashboard.refresh(operations)
    dashboard.refresh(operations)

    statistics = HEOSApplicationRunOperationsDashboardStatistics.capture(
        dashboard
    )

    assert statistics.latest_sequence == 2


def test_idle_only_dashboard_is_healthy() -> None:
    dashboard = dashboard_session()

    dashboard.refresh(
        operations_session()
    )

    statistics = HEOSApplicationRunOperationsDashboardStatistics.capture(
        dashboard
    )

    assert statistics.healthy


def test_active_refreshes_exclude_idle() -> None:
    statistics = HEOSApplicationRunOperationsDashboardStatistics(
        total_refreshes=6,
        idle_refreshes=2,
        healthy_refreshes=3,
        degraded_refreshes=1,
        rendered_frames=6,
        latest_sequence=6,
    )

    assert statistics.active_refreshes == 4


def test_degraded_refresh_makes_statistics_unhealthy() -> None:
    statistics = HEOSApplicationRunOperationsDashboardStatistics(
        total_refreshes=4,
        idle_refreshes=1,
        healthy_refreshes=2,
        degraded_refreshes=1,
        rendered_frames=4,
        latest_sequence=4,
    )

    assert not statistics.healthy


def test_healthy_refreshes_are_active() -> None:
    statistics = HEOSApplicationRunOperationsDashboardStatistics(
        total_refreshes=5,
        idle_refreshes=1,
        healthy_refreshes=4,
        degraded_refreshes=0,
        rendered_frames=5,
        latest_sequence=5,
    )

    assert statistics.active_refreshes == 4
    assert statistics.healthy


def test_statistics_preserve_all_counts() -> None:
    statistics = HEOSApplicationRunOperationsDashboardStatistics(
        total_refreshes=8,
        idle_refreshes=2,
        healthy_refreshes=4,
        degraded_refreshes=2,
        rendered_frames=8,
        latest_sequence=8,
    )

    assert statistics.total_refreshes == 8
    assert statistics.idle_refreshes == 2
    assert statistics.healthy_refreshes == 4
    assert statistics.degraded_refreshes == 2
    assert statistics.rendered_frames == 8


def test_statistics_are_snapshot() -> None:
    dashboard = dashboard_session()
    operations = operations_session()

    dashboard.refresh(operations)

    statistics = HEOSApplicationRunOperationsDashboardStatistics.capture(
        dashboard
    )

    dashboard.refresh(operations)

    assert statistics.total_refreshes == 1
    assert statistics.rendered_frames == 1
    assert statistics.latest_sequence == 1


def test_clear_produces_empty_statistics() -> None:
    dashboard = dashboard_session()

    dashboard.refresh(
        operations_session()
    )
    dashboard.clear()

    statistics = HEOSApplicationRunOperationsDashboardStatistics.capture(
        dashboard
    )

    assert statistics.empty
    assert statistics.total_refreshes == 0
    assert statistics.rendered_frames == 0
    assert statistics.latest_sequence is None


def test_sequence_continues_after_clear() -> None:
    dashboard = dashboard_session()
    operations = operations_session()

    dashboard.refresh(operations)
    dashboard.clear()
    dashboard.refresh(operations)

    statistics = HEOSApplicationRunOperationsDashboardStatistics.capture(
        dashboard
    )

    assert statistics.total_refreshes == 1
    assert statistics.latest_sequence == 2
