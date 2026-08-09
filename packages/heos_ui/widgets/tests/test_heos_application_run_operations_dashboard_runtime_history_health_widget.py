from heos_ui.widgets import (
    heos_application_run_operations_dashboard_runtime_history_health_widget as history_widget,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_presenter import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryPresentation,
    HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity,
)

HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView = (
    history_widget.HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView
)
HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget = (
    history_widget.HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget
)


def presentation(
    *,
    title: str = "HEOS Operations Dashboard Runtime History",
    status: str = "HEALTHY",
    detail: str = "Healthy 5, idle 1.",
    cycles: str = "Cycles 6",
    frames: str = "Frames 6",
    latest: str = "Latest cycle 6",
    severity: HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity = (
        HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.SUCCESS
    ),
) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryPresentation:
    return HEOSApplicationRunOperationsDashboardRuntimeHistoryPresentation(
        title=title,
        status=status,
        detail=detail,
        cycles=cycles,
        frames=frames,
        latest=latest,
        severity=severity,
    )


def test_widget_starts_empty() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    assert widget.view is None
    assert not widget.has_data


def test_update_returns_health_view() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    view = widget.update(presentation())

    assert isinstance(
        view,
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView,
    )


def test_update_stores_latest_view() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    view = widget.update(presentation())

    assert widget.view is view
    assert widget.has_data


def test_view_preserves_title() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    view = widget.update(
        presentation(
            title="HEOS Runtime Observatory",
        )
    )

    assert view.title == "HEOS Runtime Observatory"


def test_view_preserves_status() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    view = widget.update(
        presentation(
            status="DEGRADED",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
            ),
        )
    )

    assert view.status == "DEGRADED"


def test_view_preserves_detail() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    view = widget.update(
        presentation(
            detail="Healthy 230, idle 2.",
        )
    )

    assert view.detail == "Healthy 230, idle 2."


def test_view_preserves_cycles() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    view = widget.update(
        presentation(
            cycles="Cycles 232",
        )
    )

    assert view.cycles == "Cycles 232"


def test_view_preserves_frames() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    view = widget.update(
        presentation(
            frames="Frames 232",
        )
    )

    assert view.frames == "Frames 232"


def test_view_preserves_latest_cycle() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    view = widget.update(
        presentation(
            latest="Latest cycle 232",
        )
    )

    assert view.latest == "Latest cycle 232"


def test_success_view_is_healthy() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    view = widget.update(
        presentation(
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.SUCCESS
            ),
        )
    )

    assert view.healthy
    assert not view.warning
    assert not view.neutral


def test_warning_view_is_warning() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    view = widget.update(
        presentation(
            status="DEGRADED",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
            ),
        )
    )

    assert view.warning
    assert not view.healthy
    assert not view.neutral


def test_neutral_view_is_neutral() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    view = widget.update(
        presentation(
            status="EMPTY",
            detail="No runtime history recorded.",
            cycles="Cycles 0",
            frames="Frames 0",
            latest="Latest cycle —",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.NEUTRAL
            ),
        )
    )

    assert view.neutral
    assert not view.healthy
    assert not view.warning


def test_second_update_replaces_latest_view() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    first = widget.update(
        presentation(
            status="EMPTY",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.NEUTRAL
            ),
        )
    )
    second = widget.update(presentation())

    assert widget.view is second
    assert widget.view is not first


def test_previous_view_remains_snapshot() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    first = widget.update(
        presentation(
            status="EMPTY",
            detail="No runtime history recorded.",
            cycles="Cycles 0",
            frames="Frames 0",
            latest="Latest cycle —",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.NEUTRAL
            ),
        )
    )

    widget.update(
        presentation(
            status="HEALTHY",
            cycles="Cycles 232",
            frames="Frames 232",
            latest="Latest cycle 232",
        )
    )

    assert first.status == "EMPTY"
    assert first.cycles == "Cycles 0"
    assert first.frames == "Frames 0"
    assert first.latest == "Latest cycle —"
    assert first.neutral


def test_clear_removes_view() -> None:
    widget = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget()
    )

    widget.update(presentation())
    widget.clear()

    assert widget.view is None
    assert not widget.has_data
