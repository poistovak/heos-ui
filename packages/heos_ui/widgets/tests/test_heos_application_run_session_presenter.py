from heos_ui.widgets.heos_application_run_session_health import (
    HEOSApplicationRunSessionHealth,
    HEOSApplicationRunSessionHealthSummary,
)
from heos_ui.widgets.heos_application_run_session_presenter import (
    HEOSApplicationRunSessionHealthPresenter,
    HEOSApplicationRunSessionSeverity,
)


def summary(
    *,
    health: HEOSApplicationRunSessionHealth,
    total_runs: int = 0,
    completed_runs: int = 0,
    interrupted_runs: int = 0,
    idle_runs: int = 0,
    processed: int = 0,
    rendered: int = 0,
    skipped: int = 0,
    latest_sequence: int | None = None,
) -> HEOSApplicationRunSessionHealthSummary:
    return HEOSApplicationRunSessionHealthSummary(
        health=health,
        headline="test",
        total_runs=total_runs,
        completed_runs=completed_runs,
        interrupted_runs=interrupted_runs,
        idle_runs=idle_runs,
        processed=processed,
        rendered=rendered,
        skipped=skipped,
        latest_sequence=latest_sequence,
    )


def test_empty_summary_is_idle() -> None:
    presentation = HEOSApplicationRunSessionHealthPresenter().present(
        summary(
            health=HEOSApplicationRunSessionHealth.EMPTY,
        )
    )

    assert presentation.status == "IDLE"
    assert (
        presentation.severity
        is HEOSApplicationRunSessionSeverity.NEUTRAL
    )


def test_empty_summary_has_placeholders() -> None:
    presentation = HEOSApplicationRunSessionHealthPresenter().present(
        summary(
            health=HEOSApplicationRunSessionHealth.EMPTY,
        )
    )

    assert presentation.runs == "Runs —"
    assert presentation.cycles == "Cycles —"


def test_empty_summary_has_stable_detail() -> None:
    presentation = HEOSApplicationRunSessionHealthPresenter().present(
        summary(
            health=HEOSApplicationRunSessionHealth.EMPTY,
        )
    )

    assert presentation.detail == "No application runs recorded."


def test_healthy_summary_is_success() -> None:
    presentation = HEOSApplicationRunSessionHealthPresenter().present(
        summary(
            health=HEOSApplicationRunSessionHealth.HEALTHY,
            total_runs=3,
            completed_runs=3,
            processed=6,
            rendered=6,
            latest_sequence=3,
        )
    )

    assert presentation.status == "HEALTHY"
    assert (
        presentation.severity
        is HEOSApplicationRunSessionSeverity.SUCCESS
    )


def test_healthy_summary_preserves_run_count() -> None:
    presentation = HEOSApplicationRunSessionHealthPresenter().present(
        summary(
            health=HEOSApplicationRunSessionHealth.HEALTHY,
            total_runs=3,
            completed_runs=3,
        )
    )

    assert presentation.runs == "Runs 3"


def test_healthy_summary_preserves_cycle_counts() -> None:
    presentation = HEOSApplicationRunSessionHealthPresenter().present(
        summary(
            health=HEOSApplicationRunSessionHealth.HEALTHY,
            total_runs=3,
            completed_runs=3,
            processed=8,
            rendered=8,
        )
    )

    assert presentation.cycles == "Processed 8, rendered 8."


def test_healthy_detail_contains_run_outcome() -> None:
    presentation = HEOSApplicationRunSessionHealthPresenter().present(
        summary(
            health=HEOSApplicationRunSessionHealth.HEALTHY,
            total_runs=4,
            completed_runs=3,
            interrupted_runs=0,
        )
    )

    assert presentation.detail == "Completed 3, interrupted 0."


def test_degraded_summary_is_warning() -> None:
    presentation = HEOSApplicationRunSessionHealthPresenter().present(
        summary(
            health=HEOSApplicationRunSessionHealth.DEGRADED,
            total_runs=3,
            completed_runs=2,
            interrupted_runs=1,
            processed=5,
            rendered=4,
            skipped=2,
        )
    )

    assert presentation.status == "DEGRADED"
    assert (
        presentation.severity
        is HEOSApplicationRunSessionSeverity.WARNING
    )


def test_degraded_detail_contains_interruptions_and_skips() -> None:
    presentation = HEOSApplicationRunSessionHealthPresenter().present(
        summary(
            health=HEOSApplicationRunSessionHealth.DEGRADED,
            total_runs=3,
            interrupted_runs=1,
            skipped=2,
        )
    )

    assert presentation.detail == "Interrupted 1, skipped 2."


def test_degraded_summary_preserves_counts() -> None:
    presentation = HEOSApplicationRunSessionHealthPresenter().present(
        summary(
            health=HEOSApplicationRunSessionHealth.DEGRADED,
            total_runs=5,
            interrupted_runs=2,
            processed=10,
            rendered=8,
            skipped=3,
        )
    )

    assert presentation.runs == "Runs 5"
    assert presentation.cycles == "Processed 10, rendered 8."


def test_default_title_is_stable() -> None:
    presentation = HEOSApplicationRunSessionHealthPresenter().present(
        summary(
            health=HEOSApplicationRunSessionHealth.EMPTY,
        )
    )

    assert presentation.title == "HEOS Live Session"


def test_custom_title_is_preserved() -> None:
    presenter = HEOSApplicationRunSessionHealthPresenter(
        title="HEOS Session Health",
    )

    presentation = presenter.present(
        summary(
            health=HEOSApplicationRunSessionHealth.HEALTHY,
            total_runs=1,
            completed_runs=1,
        )
    )

    assert presentation.title == "HEOS Session Health"
