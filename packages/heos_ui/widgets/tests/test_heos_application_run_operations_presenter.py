from heos_ui.widgets.heos_application_run_operations_health import (
    HEOSApplicationRunOperationsHealth,
    HEOSApplicationRunOperationsHealthSummary,
)
from heos_ui.widgets.heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsHealthPresenter,
    HEOSApplicationRunOperationsPresentation,
    HEOSApplicationRunOperationsSeverity,
)


def summary(
    *,
    health: HEOSApplicationRunOperationsHealth,
    total_updates: int = 0,
    idle_updates: int = 0,
    healthy_updates: int = 0,
    degraded_updates: int = 0,
    rendered_frames: int = 0,
    latest_sequence: int | None = None,
) -> HEOSApplicationRunOperationsHealthSummary:
    return HEOSApplicationRunOperationsHealthSummary(
        health=health,
        headline="test",
        total_updates=total_updates,
        idle_updates=idle_updates,
        healthy_updates=healthy_updates,
        degraded_updates=degraded_updates,
        rendered_frames=rendered_frames,
        latest_sequence=latest_sequence,
    )


def test_present_returns_presentation() -> None:
    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        summary(
            health=HEOSApplicationRunOperationsHealth.EMPTY,
        )
    )

    assert isinstance(
        presentation,
        HEOSApplicationRunOperationsPresentation,
    )


def test_empty_health_becomes_idle() -> None:
    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        summary(
            health=HEOSApplicationRunOperationsHealth.EMPTY,
        )
    )

    assert presentation.status == "IDLE"
    assert (
        presentation.severity
        is HEOSApplicationRunOperationsSeverity.NEUTRAL
    )


def test_empty_health_has_stable_detail() -> None:
    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        summary(
            health=HEOSApplicationRunOperationsHealth.EMPTY,
        )
    )

    assert presentation.detail == "No operations updates recorded."


def test_empty_health_has_placeholders() -> None:
    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        summary(
            health=HEOSApplicationRunOperationsHealth.EMPTY,
        )
    )

    assert presentation.updates == "Updates —"
    assert presentation.frames == "Frames —"


def test_healthy_health_becomes_success() -> None:
    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        summary(
            health=HEOSApplicationRunOperationsHealth.HEALTHY,
            total_updates=5,
            healthy_updates=4,
            idle_updates=1,
            rendered_frames=5,
            latest_sequence=5,
        )
    )

    assert presentation.status == "HEALTHY"
    assert (
        presentation.severity
        is HEOSApplicationRunOperationsSeverity.SUCCESS
    )


def test_healthy_detail_preserves_counts() -> None:
    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        summary(
            health=HEOSApplicationRunOperationsHealth.HEALTHY,
            total_updates=5,
            healthy_updates=4,
            idle_updates=1,
            rendered_frames=5,
        )
    )

    assert presentation.detail == "Healthy 4, idle 1."


def test_healthy_presentation_preserves_totals() -> None:
    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        summary(
            health=HEOSApplicationRunOperationsHealth.HEALTHY,
            total_updates=210,
            healthy_updates=210,
            rendered_frames=210,
        )
    )

    assert presentation.updates == "Updates 210"
    assert presentation.frames == "Frames 210"


def test_degraded_health_becomes_warning() -> None:
    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        summary(
            health=HEOSApplicationRunOperationsHealth.DEGRADED,
            total_updates=5,
            healthy_updates=3,
            degraded_updates=2,
            rendered_frames=5,
        )
    )

    assert presentation.status == "DEGRADED"
    assert (
        presentation.severity
        is HEOSApplicationRunOperationsSeverity.WARNING
    )


def test_degraded_detail_preserves_counts() -> None:
    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        summary(
            health=HEOSApplicationRunOperationsHealth.DEGRADED,
            total_updates=7,
            healthy_updates=5,
            degraded_updates=2,
            rendered_frames=7,
        )
    )

    assert presentation.detail == "Degraded 2, healthy 5."


def test_degraded_presentation_preserves_totals() -> None:
    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        summary(
            health=HEOSApplicationRunOperationsHealth.DEGRADED,
            total_updates=7,
            healthy_updates=5,
            degraded_updates=2,
            rendered_frames=7,
        )
    )

    assert presentation.updates == "Updates 7"
    assert presentation.frames == "Frames 7"


def test_default_title_is_stable() -> None:
    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        summary(
            health=HEOSApplicationRunOperationsHealth.EMPTY,
        )
    )

    assert presentation.title == "HEOS Operations"


def test_custom_title_is_preserved() -> None:
    presenter = HEOSApplicationRunOperationsHealthPresenter(
        title="HEOS Operations Health",
    )

    presentation = presenter.present(
        summary(
            health=HEOSApplicationRunOperationsHealth.HEALTHY,
            total_updates=1,
            healthy_updates=1,
            rendered_frames=1,
        )
    )

    assert presentation.title == "HEOS Operations Health"


def test_presentation_is_immutable_snapshot() -> None:
    source = summary(
        health=HEOSApplicationRunOperationsHealth.HEALTHY,
        total_updates=3,
        healthy_updates=3,
        rendered_frames=3,
        latest_sequence=3,
    )

    presentation = HEOSApplicationRunOperationsHealthPresenter().present(
        source
    )

    assert presentation.status == "HEALTHY"
    assert presentation.updates == "Updates 3"
    assert presentation.frames == "Frames 3"
