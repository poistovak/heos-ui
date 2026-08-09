from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_health import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth,
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_presenter import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter,
    HEOSApplicationRunOperationsDashboardRuntimeHistoryPresentation,
    HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity,
)


def summary(
    *,
    health: HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.HEALTHY
    ),
    total_cycles: int = 5,
    healthy_cycles: int = 4,
    degraded_cycles: int = 0,
    idle_cycles: int = 1,
    rendered_frames: int = 5,
    latest_cycle: int | None = 5,
) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary:
    return HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary(
        health=health,
        total_cycles=total_cycles,
        healthy_cycles=healthy_cycles,
        degraded_cycles=degraded_cycles,
        idle_cycles=idle_cycles,
        rendered_frames=rendered_frames,
        latest_cycle=latest_cycle,
    )


def test_present_returns_presentation() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(summary())
    )

    assert isinstance(
        presentation,
        HEOSApplicationRunOperationsDashboardRuntimeHistoryPresentation,
    )


def test_present_uses_default_title() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(summary())
    )

    assert (
        presentation.title
        == "HEOS Operations Dashboard Runtime History"
    )


def test_present_supports_custom_title() -> None:
    presenter = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter(
            title="HEOS Runtime Observatory"
        )
    )

    presentation = presenter.present(summary())

    assert presentation.title == "HEOS Runtime Observatory"


def test_healthy_summary_has_healthy_status() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(summary())
    )

    assert presentation.status == "HEALTHY"


def test_healthy_summary_has_success_severity() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(summary())
    )

    assert (
        presentation.severity
        is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.SUCCESS
    )


def test_healthy_summary_builds_detail() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(
            summary(
                healthy_cycles=7,
                idle_cycles=2,
            )
        )
    )

    assert presentation.detail == "Healthy 7, idle 2."


def test_degraded_summary_has_degraded_status() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(
            summary(
                health=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.DEGRADED
                ),
                healthy_cycles=6,
                degraded_cycles=2,
                idle_cycles=1,
            )
        )
    )

    assert presentation.status == "DEGRADED"


def test_degraded_summary_has_warning_severity() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(
            summary(
                health=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.DEGRADED
                ),
                degraded_cycles=1,
            )
        )
    )

    assert (
        presentation.severity
        is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
    )


def test_degraded_summary_builds_detail() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(
            summary(
                health=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.DEGRADED
                ),
                healthy_cycles=8,
                degraded_cycles=2,
                idle_cycles=3,
            )
        )
    )

    assert (
        presentation.detail
        == "Degraded 2, healthy 8, idle 3."
    )


def test_empty_summary_has_empty_status() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(
            summary(
                health=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.EMPTY
                ),
                total_cycles=0,
                healthy_cycles=0,
                idle_cycles=0,
                rendered_frames=0,
                latest_cycle=None,
            )
        )
    )

    assert presentation.status == "EMPTY"


def test_empty_summary_has_neutral_severity() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(
            summary(
                health=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.EMPTY
                ),
                total_cycles=0,
                healthy_cycles=0,
                idle_cycles=0,
                rendered_frames=0,
                latest_cycle=None,
            )
        )
    )

    assert (
        presentation.severity
        is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.NEUTRAL
    )


def test_empty_summary_builds_detail() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(
            summary(
                health=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.EMPTY
                ),
                total_cycles=0,
                healthy_cycles=0,
                idle_cycles=0,
                rendered_frames=0,
                latest_cycle=None,
            )
        )
    )

    assert presentation.detail == "No runtime history recorded."


def test_cycles_are_formatted() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(summary(total_cycles=231))
    )

    assert presentation.cycles == "Cycles 231"


def test_frames_are_formatted() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(summary(rendered_frames=230))
    )

    assert presentation.frames == "Frames 230"


def test_latest_cycle_is_formatted() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(summary(latest_cycle=231))
    )

    assert presentation.latest == "Latest cycle 231"


def test_missing_latest_cycle_uses_placeholder() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter()
        .present(
            summary(
                health=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.EMPTY
                ),
                total_cycles=0,
                healthy_cycles=0,
                idle_cycles=0,
                rendered_frames=0,
                latest_cycle=None,
            )
        )
    )

    assert presentation.latest == "Latest cycle —"
