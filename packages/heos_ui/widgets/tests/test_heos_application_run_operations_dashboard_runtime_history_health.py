from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_health import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth,
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_statistics import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics,
)


def statistics(
    *,
    total_cycles: int = 5,
    idle_cycles: int = 1,
    healthy_cycles: int = 4,
    degraded_cycles: int = 0,
    rendered_frames: int = 5,
    latest_cycle: int | None = 5,
) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics:
    return HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics(
        total_cycles=total_cycles,
        idle_cycles=idle_cycles,
        healthy_cycles=healthy_cycles,
        degraded_cycles=degraded_cycles,
        rendered_frames=rendered_frames,
        latest_cycle=latest_cycle,
    )


def test_empty_statistics_produce_empty_health() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(
                total_cycles=0,
                idle_cycles=0,
                healthy_cycles=0,
                degraded_cycles=0,
                rendered_frames=0,
                latest_cycle=None,
            )
        )
    )

    assert (
        summary.health
        is HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.EMPTY
    )


def test_empty_summary_reports_empty() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(
                total_cycles=0,
                idle_cycles=0,
                healthy_cycles=0,
                degraded_cycles=0,
                rendered_frames=0,
                latest_cycle=None,
            )
        )
    )

    assert summary.empty
    assert not summary.healthy
    assert not summary.degraded


def test_clean_statistics_produce_healthy_health() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics()
        )
    )

    assert (
        summary.health
        is HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.HEALTHY
    )


def test_healthy_summary_reports_healthy() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics()
        )
    )

    assert summary.healthy
    assert not summary.empty
    assert not summary.degraded


def test_degraded_cycles_produce_degraded_health() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(
                healthy_cycles=3,
                degraded_cycles=1,
            )
        )
    )

    assert (
        summary.health
        is HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.DEGRADED
    )


def test_degraded_summary_reports_degraded() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(
                healthy_cycles=3,
                degraded_cycles=1,
            )
        )
    )

    assert summary.degraded
    assert not summary.empty
    assert not summary.healthy


def test_idle_cycles_do_not_degrade_health() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(
                total_cycles=5,
                idle_cycles=3,
                healthy_cycles=2,
                degraded_cycles=0,
            )
        )
    )

    assert summary.healthy


def test_one_degraded_cycle_is_enough_to_degrade() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(
                total_cycles=100,
                idle_cycles=9,
                healthy_cycles=90,
                degraded_cycles=1,
                rendered_frames=100,
                latest_cycle=100,
            )
        )
    )

    assert summary.degraded


def test_summary_preserves_total_cycles() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(total_cycles=230)
        )
    )

    assert summary.total_cycles == 230


def test_summary_preserves_healthy_cycles() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(healthy_cycles=7)
        )
    )

    assert summary.healthy_cycles == 7


def test_summary_preserves_degraded_cycles() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(
                healthy_cycles=3,
                degraded_cycles=2,
            )
        )
    )

    assert summary.degraded_cycles == 2


def test_summary_preserves_idle_cycles() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(idle_cycles=3)
        )
    )

    assert summary.idle_cycles == 3


def test_summary_preserves_rendered_frames() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(rendered_frames=229)
        )
    )

    assert summary.rendered_frames == 229


def test_summary_preserves_latest_cycle() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(latest_cycle=230)
        )
    )

    assert summary.latest_cycle == 230


def test_empty_summary_preserves_missing_latest_cycle() -> None:
    summary = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary.from_statistics(
            statistics(
                total_cycles=0,
                idle_cycles=0,
                healthy_cycles=0,
                degraded_cycles=0,
                rendered_frames=0,
                latest_cycle=None,
            )
        )
    )

    assert summary.latest_cycle is None
