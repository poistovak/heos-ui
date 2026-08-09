from heos_ui.widgets.heos_application_run_operations_dashboard_health_widget import (
    HEOSApplicationRunOperationsDashboardHealthView,
    HEOSApplicationRunOperationsDashboardHealthWidget,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_presenter import (
    HEOSApplicationRunOperationsDashboardPresentation,
    HEOSApplicationRunOperationsDashboardSeverity,
)


def presentation(
    *,
    title: str = "HEOS Operations Dashboard",
    status: str = "HEALTHY",
    detail: str = "Healthy 4, idle 1.",
    refreshes: str = "Refreshes 5",
    frames: str = "Frames 5",
    sequence: str = "Sequence 5",
    severity: HEOSApplicationRunOperationsDashboardSeverity = (
        HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
    ),
) -> HEOSApplicationRunOperationsDashboardPresentation:
    return HEOSApplicationRunOperationsDashboardPresentation(
        title=title,
        status=status,
        detail=detail,
        refreshes=refreshes,
        frames=frames,
        sequence=sequence,
        severity=severity,
    )


def test_widget_starts_empty() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    assert widget.view is None
    assert not widget.has_data


def test_update_returns_dashboard_health_view() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    view = widget.update(presentation())

    assert isinstance(
        view,
        HEOSApplicationRunOperationsDashboardHealthView,
    )


def test_update_stores_latest_view() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    view = widget.update(presentation())

    assert widget.view is view
    assert widget.has_data


def test_view_preserves_title() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    view = widget.update(
        presentation(
            title="HEOS Operations Control",
        )
    )

    assert view.title == "HEOS Operations Control"


def test_view_preserves_status() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    view = widget.update(
        presentation(
            status="DEGRADED",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.WARNING
            ),
        )
    )

    assert view.status == "DEGRADED"


def test_view_preserves_detail() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    view = widget.update(
        presentation(
            detail="Healthy 220, idle 1.",
        )
    )

    assert view.detail == "Healthy 220, idle 1."


def test_view_preserves_refreshes() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    view = widget.update(
        presentation(
            refreshes="Refreshes 221",
        )
    )

    assert view.refreshes == "Refreshes 221"


def test_view_preserves_frames() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    view = widget.update(
        presentation(
            frames="Frames 221",
        )
    )

    assert view.frames == "Frames 221"


def test_view_preserves_sequence() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    view = widget.update(
        presentation(
            sequence="Sequence 221",
        )
    )

    assert view.sequence == "Sequence 221"


def test_success_view_is_healthy() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    view = widget.update(
        presentation(
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
            ),
        )
    )

    assert view.healthy
    assert not view.warning
    assert not view.neutral


def test_warning_view_is_warning() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    view = widget.update(
        presentation(
            status="DEGRADED",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.WARNING
            ),
        )
    )

    assert view.warning
    assert not view.healthy
    assert not view.neutral


def test_neutral_view_is_neutral() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    view = widget.update(
        presentation(
            status="IDLE",
            detail="No dashboard refreshes recorded.",
            refreshes="Refreshes —",
            frames="Frames —",
            sequence="Sequence —",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
            ),
        )
    )

    assert view.neutral
    assert not view.healthy
    assert not view.warning


def test_second_update_replaces_latest_view() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    first = widget.update(
        presentation(
            status="IDLE",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
            ),
        )
    )
    second = widget.update(presentation())

    assert widget.view is second
    assert widget.view is not first


def test_previous_view_remains_snapshot() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    first = widget.update(
        presentation(
            status="IDLE",
            detail="No dashboard refreshes recorded.",
            refreshes="Refreshes —",
            frames="Frames —",
            sequence="Sequence —",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
            ),
        )
    )

    widget.update(
        presentation(
            status="HEALTHY",
            refreshes="Refreshes 221",
            frames="Frames 221",
            sequence="Sequence 221",
        )
    )

    assert first.status == "IDLE"
    assert first.refreshes == "Refreshes —"
    assert first.frames == "Frames —"
    assert first.sequence == "Sequence —"
    assert first.neutral


def test_clear_removes_view() -> None:
    widget = HEOSApplicationRunOperationsDashboardHealthWidget()

    widget.update(presentation())
    widget.clear()

    assert widget.view is None
    assert not widget.has_data
