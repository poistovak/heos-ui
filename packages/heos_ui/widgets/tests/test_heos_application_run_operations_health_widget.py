from heos_ui.widgets.heos_application_run_operations_health_widget import (
    HEOSApplicationRunOperationsHealthView,
    HEOSApplicationRunOperationsHealthWidget,
)
from heos_ui.widgets.heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsPresentation,
    HEOSApplicationRunOperationsSeverity,
)


def presentation(
    *,
    title: str = "HEOS Operations",
    status: str = "HEALTHY",
    detail: str = "Healthy 4, idle 1.",
    updates: str = "Updates 5",
    frames: str = "Frames 5",
    severity: HEOSApplicationRunOperationsSeverity = (
        HEOSApplicationRunOperationsSeverity.SUCCESS
    ),
) -> HEOSApplicationRunOperationsPresentation:
    return HEOSApplicationRunOperationsPresentation(
        title=title,
        status=status,
        detail=detail,
        updates=updates,
        frames=frames,
        severity=severity,
    )


def test_widget_starts_empty() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    assert widget.view is None
    assert not widget.has_data


def test_update_returns_health_view() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    view = widget.update(presentation())

    assert isinstance(
        view,
        HEOSApplicationRunOperationsHealthView,
    )


def test_update_stores_latest_view() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    view = widget.update(presentation())

    assert widget.view is view
    assert widget.has_data


def test_view_preserves_title() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    view = widget.update(
        presentation(title="HEOS Operations Health")
    )

    assert view.title == "HEOS Operations Health"


def test_view_preserves_status() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    view = widget.update(
        presentation(status="DEGRADED")
    )

    assert view.status == "DEGRADED"


def test_view_preserves_detail() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    view = widget.update(
        presentation(
            detail="Healthy 210, idle 1.",
        )
    )

    assert view.detail == "Healthy 210, idle 1."


def test_view_preserves_updates() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    view = widget.update(
        presentation(updates="Updates 211")
    )

    assert view.updates == "Updates 211"


def test_view_preserves_frames() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    view = widget.update(
        presentation(frames="Frames 211")
    )

    assert view.frames == "Frames 211"


def test_success_view_is_healthy() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    view = widget.update(
        presentation(
            severity=HEOSApplicationRunOperationsSeverity.SUCCESS,
        )
    )

    assert view.healthy
    assert not view.warning
    assert not view.neutral


def test_warning_view_is_warning() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    view = widget.update(
        presentation(
            status="DEGRADED",
            severity=HEOSApplicationRunOperationsSeverity.WARNING,
        )
    )

    assert view.warning
    assert not view.healthy
    assert not view.neutral


def test_neutral_view_is_neutral() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    view = widget.update(
        presentation(
            status="IDLE",
            updates="Updates —",
            frames="Frames —",
            severity=HEOSApplicationRunOperationsSeverity.NEUTRAL,
        )
    )

    assert view.neutral
    assert not view.healthy
    assert not view.warning


def test_second_update_replaces_latest_view() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    first = widget.update(
        presentation(
            status="IDLE",
            severity=HEOSApplicationRunOperationsSeverity.NEUTRAL,
        )
    )
    second = widget.update(presentation())

    assert widget.view is second
    assert widget.view is not first


def test_previous_view_remains_snapshot() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    first = widget.update(
        presentation(
            status="IDLE",
            detail="No operations updates recorded.",
            updates="Updates —",
            frames="Frames —",
            severity=HEOSApplicationRunOperationsSeverity.NEUTRAL,
        )
    )

    widget.update(
        presentation(
            status="HEALTHY",
            updates="Updates 211",
            frames="Frames 211",
        )
    )

    assert first.status == "IDLE"
    assert first.updates == "Updates —"
    assert first.frames == "Frames —"
    assert first.neutral


def test_clear_removes_view() -> None:
    widget = HEOSApplicationRunOperationsHealthWidget()

    widget.update(presentation())
    widget.clear()

    assert widget.view is None
    assert not widget.has_data
