from heos_ui.widgets.heos_application_run_operations_dashboard_health import (
    HEOSApplicationRunOperationsDashboardHealth,
    HEOSApplicationRunOperationsDashboardHealthSummary,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_statistics import (
    HEOSApplicationRunOperationsDashboardStatistics,
)


def statistics(
    *,
    total_refreshes: int = 0,
    idle_refreshes: int = 0,
    healthy_refreshes: int = 0,
    degraded_refreshes: int = 0,
    rendered_frames: int = 0,
    latest_sequence: int | None = None,
) -> HEOSApplicationRunOperationsDashboardStatistics:
    return HEOSApplicationRunOperationsDashboardStatistics(
        total_refreshes=total_refreshes,
        idle_refreshes=idle_refreshes,
        healthy_refreshes=healthy_refreshes,
        degraded_refreshes=degraded_refreshes,
        rendered_frames=rendered_frames,
        latest_sequence=latest_sequence,
    )


def test_empty_statistics_create_empty_health() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics()
        )
    )

    assert (
        summary.health
        is HEOSApplicationRunOperationsDashboardHealth.EMPTY
    )
    assert summary.empty
    assert not summary.healthy
    assert not summary.degraded


def test_empty_health_has_stable_headline() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics()
        )
    )

    assert summary.headline == "No dashboard refreshes recorded."


def test_healthy_statistics_create_healthy_health() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics(
                total_refreshes=4,
                healthy_refreshes=4,
                rendered_frames=4,
                latest_sequence=4,
            )
        )
    )

    assert (
        summary.health
        is HEOSApplicationRunOperationsDashboardHealth.HEALTHY
    )
    assert summary.healthy
    assert not summary.empty
    assert not summary.degraded


def test_idle_refreshes_do_not_degrade_health() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics(
                total_refreshes=5,
                idle_refreshes=2,
                healthy_refreshes=3,
                rendered_frames=5,
                latest_sequence=5,
            )
        )
    )

    assert summary.healthy
    assert summary.idle_refreshes == 2


def test_idle_only_dashboard_is_healthy() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics(
                total_refreshes=3,
                idle_refreshes=3,
                rendered_frames=3,
                latest_sequence=3,
            )
        )
    )

    assert summary.healthy


def test_healthy_health_has_stable_headline() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics(
                total_refreshes=6,
                healthy_refreshes=6,
                rendered_frames=6,
                latest_sequence=6,
            )
        )
    )

    assert summary.headline == "Dashboard healthy across 6 refreshes."


def test_degraded_refresh_creates_degraded_health() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics(
                total_refreshes=5,
                healthy_refreshes=4,
                degraded_refreshes=1,
                rendered_frames=5,
                latest_sequence=5,
            )
        )
    )

    assert (
        summary.health
        is HEOSApplicationRunOperationsDashboardHealth.DEGRADED
    )
    assert summary.degraded
    assert not summary.healthy


def test_degraded_health_has_stable_headline() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics(
                total_refreshes=7,
                healthy_refreshes=5,
                degraded_refreshes=2,
                rendered_frames=7,
                latest_sequence=7,
            )
        )
    )

    assert (
        summary.headline
        == "Dashboard degraded with 2 degraded refreshes."
    )


def test_summary_preserves_refresh_counts() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics(
                total_refreshes=9,
                idle_refreshes=2,
                healthy_refreshes=5,
                degraded_refreshes=2,
                rendered_frames=9,
                latest_sequence=9,
            )
        )
    )

    assert summary.total_refreshes == 9
    assert summary.idle_refreshes == 2
    assert summary.healthy_refreshes == 5
    assert summary.degraded_refreshes == 2


def test_summary_preserves_rendered_frames() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics(
                total_refreshes=8,
                healthy_refreshes=8,
                rendered_frames=8,
                latest_sequence=8,
            )
        )
    )

    assert summary.rendered_frames == 8


def test_summary_preserves_latest_sequence() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics(
                total_refreshes=219,
                healthy_refreshes=219,
                rendered_frames=219,
                latest_sequence=219,
            )
        )
    )

    assert summary.latest_sequence == 219


def test_empty_summary_has_no_latest_sequence() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics()
        )
    )

    assert summary.latest_sequence is None


def test_single_idle_refresh_is_healthy() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics(
                total_refreshes=1,
                idle_refreshes=1,
                rendered_frames=1,
                latest_sequence=1,
            )
        )
    )

    assert summary.healthy
    assert summary.headline == "Dashboard healthy across 1 refreshes."


def test_single_degraded_refresh_is_degraded() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            statistics(
                total_refreshes=1,
                degraded_refreshes=1,
                rendered_frames=1,
                latest_sequence=1,
            )
        )
    )

    assert summary.degraded
    assert (
        summary.headline
        == "Dashboard degraded with 1 degraded refreshes."
    )


def test_summary_is_immutable_snapshot() -> None:
    source = statistics(
        total_refreshes=3,
        healthy_refreshes=3,
        rendered_frames=3,
        latest_sequence=3,
    )

    summary = (
        HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
            source
        )
    )

    assert summary.total_refreshes == 3
    assert summary.rendered_frames == 3
    assert summary.latest_sequence == 3
    assert summary.healthy
