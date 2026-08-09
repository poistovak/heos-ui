from heos_ui.widgets.heos_application_run_operations_health import (
    HEOSApplicationRunOperationsHealth,
    HEOSApplicationRunOperationsHealthSummary,
)
from heos_ui.widgets.heos_application_run_operations_session_statistics import (
    HEOSApplicationRunOperationsSessionStatistics,
)


def statistics(
    *,
    total_updates: int = 0,
    idle_updates: int = 0,
    healthy_updates: int = 0,
    degraded_updates: int = 0,
    rendered_frames: int = 0,
    latest_sequence: int | None = None,
) -> HEOSApplicationRunOperationsSessionStatistics:
    return HEOSApplicationRunOperationsSessionStatistics(
        total_updates=total_updates,
        idle_updates=idle_updates,
        healthy_updates=healthy_updates,
        degraded_updates=degraded_updates,
        rendered_frames=rendered_frames,
        latest_sequence=latest_sequence,
    )


def test_empty_statistics_create_empty_health() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics()
    )

    assert summary.health is HEOSApplicationRunOperationsHealth.EMPTY
    assert summary.empty
    assert not summary.healthy
    assert not summary.degraded


def test_empty_health_has_stable_headline() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics()
    )

    assert summary.headline == "No operations updates recorded."


def test_healthy_statistics_create_healthy_health() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics(
            total_updates=3,
            healthy_updates=3,
            rendered_frames=3,
            latest_sequence=3,
        )
    )

    assert summary.health is HEOSApplicationRunOperationsHealth.HEALTHY
    assert summary.healthy
    assert not summary.empty
    assert not summary.degraded


def test_idle_updates_do_not_degrade_health() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics(
            total_updates=4,
            idle_updates=1,
            healthy_updates=3,
            rendered_frames=4,
            latest_sequence=4,
        )
    )

    assert summary.healthy
    assert summary.idle_updates == 1


def test_healthy_health_has_stable_headline() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics(
            total_updates=4,
            healthy_updates=4,
            rendered_frames=4,
            latest_sequence=4,
        )
    )

    assert summary.headline == "Operations healthy across 4 updates."


def test_degraded_update_creates_degraded_health() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics(
            total_updates=4,
            healthy_updates=3,
            degraded_updates=1,
            rendered_frames=4,
            latest_sequence=4,
        )
    )

    assert summary.health is HEOSApplicationRunOperationsHealth.DEGRADED
    assert summary.degraded
    assert not summary.healthy


def test_degraded_health_has_stable_headline() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics(
            total_updates=5,
            healthy_updates=3,
            degraded_updates=2,
            rendered_frames=5,
            latest_sequence=5,
        )
    )

    assert (
        summary.headline
        == "Operations degraded with 2 degraded updates."
    )


def test_summary_preserves_update_counts() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics(
            total_updates=7,
            idle_updates=1,
            healthy_updates=4,
            degraded_updates=2,
            rendered_frames=7,
            latest_sequence=7,
        )
    )

    assert summary.total_updates == 7
    assert summary.idle_updates == 1
    assert summary.healthy_updates == 4
    assert summary.degraded_updates == 2


def test_summary_preserves_rendered_frames() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics(
            total_updates=6,
            healthy_updates=6,
            rendered_frames=6,
            latest_sequence=6,
        )
    )

    assert summary.rendered_frames == 6


def test_summary_preserves_latest_sequence() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics(
            total_updates=209,
            healthy_updates=209,
            rendered_frames=209,
            latest_sequence=209,
        )
    )

    assert summary.latest_sequence == 209


def test_empty_summary_has_no_latest_sequence() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics()
    )

    assert summary.latest_sequence is None


def test_single_idle_update_is_healthy() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics(
            total_updates=1,
            idle_updates=1,
            rendered_frames=1,
            latest_sequence=1,
        )
    )

    assert summary.healthy
    assert summary.headline == "Operations healthy across 1 updates."


def test_single_degraded_update_is_degraded() -> None:
    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        statistics(
            total_updates=1,
            degraded_updates=1,
            rendered_frames=1,
            latest_sequence=1,
        )
    )

    assert summary.degraded
    assert (
        summary.headline
        == "Operations degraded with 1 degraded updates."
    )


def test_summary_is_immutable_snapshot() -> None:
    source = statistics(
        total_updates=3,
        healthy_updates=3,
        rendered_frames=3,
        latest_sequence=3,
    )

    summary = HEOSApplicationRunOperationsHealthSummary.from_statistics(
        source
    )

    assert summary.total_updates == 3
    assert summary.rendered_frames == 3
    assert summary.latest_sequence == 3
    assert summary.healthy
