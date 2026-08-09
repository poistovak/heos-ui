from heos_ui.widgets.heos_application_run_live_session_statistics import (
    HEOSApplicationRunLiveSessionStatistics,
)
from heos_ui.widgets.heos_application_run_session_health import (
    HEOSApplicationRunSessionHealth,
    HEOSApplicationRunSessionHealthSummary,
)


def statistics(
    *,
    total_runs: int = 0,
    completed_runs: int = 0,
    interrupted_runs: int = 0,
    idle_runs: int = 0,
    processed: int = 0,
    rendered: int = 0,
    skipped: int = 0,
    latest_sequence: int | None = None,
) -> HEOSApplicationRunLiveSessionStatistics:
    return HEOSApplicationRunLiveSessionStatistics(
        total_runs=total_runs,
        completed_runs=completed_runs,
        interrupted_runs=interrupted_runs,
        idle_runs=idle_runs,
        processed=processed,
        rendered=rendered,
        skipped=skipped,
        latest_sequence=latest_sequence,
    )


def test_empty_statistics_create_empty_health() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics()
    )

    assert summary.health is HEOSApplicationRunSessionHealth.EMPTY
    assert summary.empty
    assert not summary.healthy
    assert not summary.degraded


def test_empty_summary_has_stable_headline() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics()
    )

    assert summary.headline == "No application runs recorded."


def test_healthy_statistics_create_healthy_health() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics(
            total_runs=2,
            completed_runs=2,
            processed=4,
            rendered=4,
            latest_sequence=2,
        )
    )

    assert summary.health is HEOSApplicationRunSessionHealth.HEALTHY
    assert summary.healthy
    assert not summary.degraded
    assert not summary.empty


def test_healthy_summary_has_stable_headline() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics(
            total_runs=2,
            completed_runs=2,
            latest_sequence=2,
        )
    )

    assert summary.headline == "Session healthy across 2 runs."


def test_idle_runs_do_not_degrade_session() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics(
            total_runs=3,
            completed_runs=2,
            idle_runs=1,
            latest_sequence=3,
        )
    )

    assert summary.healthy
    assert summary.idle_runs == 1


def test_interruption_creates_degraded_health() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics(
            total_runs=3,
            completed_runs=2,
            interrupted_runs=1,
            skipped=2,
            latest_sequence=3,
        )
    )

    assert summary.health is HEOSApplicationRunSessionHealth.DEGRADED
    assert summary.degraded
    assert not summary.healthy


def test_degraded_summary_has_stable_headline() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics(
            total_runs=4,
            completed_runs=2,
            interrupted_runs=2,
            latest_sequence=4,
        )
    )

    assert summary.headline == "Session degraded with 2 interrupted runs."


def test_summary_preserves_run_counts() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics(
            total_runs=5,
            completed_runs=3,
            interrupted_runs=1,
            idle_runs=1,
            latest_sequence=5,
        )
    )

    assert summary.total_runs == 5
    assert summary.completed_runs == 3
    assert summary.interrupted_runs == 1
    assert summary.idle_runs == 1


def test_summary_preserves_cycle_totals() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics(
            total_runs=3,
            completed_runs=2,
            interrupted_runs=1,
            processed=8,
            rendered=7,
            skipped=2,
            latest_sequence=3,
        )
    )

    assert summary.processed == 8
    assert summary.rendered == 7
    assert summary.skipped == 2


def test_summary_preserves_latest_sequence() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics(
            total_runs=198,
            completed_runs=198,
            processed=198,
            rendered=198,
            latest_sequence=198,
        )
    )

    assert summary.latest_sequence == 198


def test_empty_summary_has_no_latest_sequence() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics()
    )

    assert summary.latest_sequence is None


def test_single_completed_run_is_healthy() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics(
            total_runs=1,
            completed_runs=1,
            processed=1,
            rendered=1,
            latest_sequence=1,
        )
    )

    assert summary.healthy
    assert summary.headline == "Session healthy across 1 runs."


def test_single_interrupted_run_is_degraded() -> None:
    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        statistics(
            total_runs=1,
            interrupted_runs=1,
            processed=1,
            skipped=1,
            latest_sequence=1,
        )
    )

    assert summary.degraded
    assert summary.headline == "Session degraded with 1 interrupted runs."


def test_summary_is_immutable_snapshot() -> None:
    source = statistics(
        total_runs=2,
        completed_runs=2,
        processed=4,
        rendered=4,
        latest_sequence=2,
    )

    summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
        source
    )

    assert summary.total_runs == 2
    assert summary.processed == 4
    assert summary.latest_sequence == 2
    assert summary.healthy
