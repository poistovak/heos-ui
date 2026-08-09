from heos_ui.widgets.heos_application_run_operations_dashboard_health import (
    HEOSApplicationRunOperationsDashboardHealth,
    HEOSApplicationRunOperationsDashboardHealthSummary,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_presenter import (
    HEOSApplicationRunOperationsDashboardHealthPresenter,
    HEOSApplicationRunOperationsDashboardPresentation,
    HEOSApplicationRunOperationsDashboardSeverity,
)


def summary(
    *,
    health: HEOSApplicationRunOperationsDashboardHealth,
    total_refreshes: int = 0,
    idle_refreshes: int = 0,
    healthy_refreshes: int = 0,
    degraded_refreshes: int = 0,
    rendered_frames: int = 0,
    latest_sequence: int | None = None,
) -> HEOSApplicationRunOperationsDashboardHealthSummary:
    return HEOSApplicationRunOperationsDashboardHealthSummary(
        health=health,
        headline="test",
        total_refreshes=total_refreshes,
        idle_refreshes=idle_refreshes,
        healthy_refreshes=healthy_refreshes,
        degraded_refreshes=degraded_refreshes,
        rendered_frames=rendered_frames,
        latest_sequence=latest_sequence,
    )


def test_present_returns_dashboard_presentation() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.EMPTY,
            )
        )
    )

    assert isinstance(
        presentation,
        HEOSApplicationRunOperationsDashboardPresentation,
    )


def test_empty_health_becomes_idle() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.EMPTY,
            )
        )
    )

    assert presentation.status == "IDLE"
    assert (
        presentation.severity
        is HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
    )


def test_empty_health_has_stable_detail() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.EMPTY,
            )
        )
    )

    assert presentation.detail == "No dashboard refreshes recorded."


def test_empty_health_has_placeholders() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.EMPTY,
            )
        )
    )

    assert presentation.refreshes == "Refreshes —"
    assert presentation.frames == "Frames —"
    assert presentation.sequence == "Sequence —"


def test_healthy_health_becomes_success() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.HEALTHY,
                total_refreshes=5,
                healthy_refreshes=4,
                idle_refreshes=1,
                rendered_frames=5,
                latest_sequence=5,
            )
        )
    )

    assert presentation.status == "HEALTHY"
    assert (
        presentation.severity
        is HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
    )


def test_healthy_detail_preserves_counts() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.HEALTHY,
                total_refreshes=5,
                healthy_refreshes=4,
                idle_refreshes=1,
                rendered_frames=5,
                latest_sequence=5,
            )
        )
    )

    assert presentation.detail == "Healthy 4, idle 1."


def test_healthy_presentation_preserves_refreshes() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.HEALTHY,
                total_refreshes=220,
                healthy_refreshes=220,
                rendered_frames=220,
                latest_sequence=220,
            )
        )
    )

    assert presentation.refreshes == "Refreshes 220"


def test_healthy_presentation_preserves_frames() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.HEALTHY,
                total_refreshes=220,
                healthy_refreshes=220,
                rendered_frames=219,
                latest_sequence=220,
            )
        )
    )

    assert presentation.frames == "Frames 219"


def test_healthy_presentation_preserves_sequence() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.HEALTHY,
                total_refreshes=220,
                healthy_refreshes=220,
                rendered_frames=220,
                latest_sequence=220,
            )
        )
    )

    assert presentation.sequence == "Sequence 220"


def test_degraded_health_becomes_warning() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.DEGRADED,
                total_refreshes=7,
                healthy_refreshes=5,
                degraded_refreshes=2,
                rendered_frames=7,
                latest_sequence=7,
            )
        )
    )

    assert presentation.status == "DEGRADED"
    assert (
        presentation.severity
        is HEOSApplicationRunOperationsDashboardSeverity.WARNING
    )


def test_degraded_detail_preserves_counts() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.DEGRADED,
                total_refreshes=7,
                healthy_refreshes=5,
                degraded_refreshes=2,
                rendered_frames=7,
                latest_sequence=7,
            )
        )
    )

    assert presentation.detail == "Degraded 2, healthy 5."


def test_degraded_presentation_preserves_totals() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.DEGRADED,
                total_refreshes=9,
                healthy_refreshes=6,
                degraded_refreshes=3,
                rendered_frames=9,
                latest_sequence=9,
            )
        )
    )

    assert presentation.refreshes == "Refreshes 9"
    assert presentation.frames == "Frames 9"
    assert presentation.sequence == "Sequence 9"


def test_default_title_is_stable() -> None:
    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            summary(
                health=HEOSApplicationRunOperationsDashboardHealth.EMPTY,
            )
        )
    )

    assert presentation.title == "HEOS Operations Dashboard"


def test_custom_title_is_preserved() -> None:
    presenter = HEOSApplicationRunOperationsDashboardHealthPresenter(
        title="HEOS Operations Control",
    )

    presentation = presenter.present(
        summary(
            health=HEOSApplicationRunOperationsDashboardHealth.HEALTHY,
            total_refreshes=1,
            healthy_refreshes=1,
            rendered_frames=1,
            latest_sequence=1,
        )
    )

    assert presentation.title == "HEOS Operations Control"


def test_presentation_is_immutable_snapshot() -> None:
    source = summary(
        health=HEOSApplicationRunOperationsDashboardHealth.HEALTHY,
        total_refreshes=3,
        healthy_refreshes=3,
        rendered_frames=3,
        latest_sequence=3,
    )

    presentation = (
        HEOSApplicationRunOperationsDashboardHealthPresenter().present(
            source
        )
    )

    assert presentation.status == "HEALTHY"
    assert presentation.refreshes == "Refreshes 3"
    assert presentation.frames == "Frames 3"
    assert presentation.sequence == "Sequence 3"
