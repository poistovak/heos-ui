from heos_ui.widgets.heos_application_run_session_health_widget import (
    HEOSApplicationRunSessionHealthView,
    HEOSApplicationRunSessionHealthWidget,
)
from heos_ui.widgets.heos_application_run_session_presenter import (
    HEOSApplicationRunSessionPresentation,
    HEOSApplicationRunSessionSeverity,
)


def presentation(
    *,
    title: str = "HEOS Live Session",
    status: str = "HEALTHY",
    detail: str = "Completed 3, interrupted 0.",
    runs: str = "Runs 3",
    cycles: str = "Processed 6, rendered 6.",
    severity: HEOSApplicationRunSessionSeverity = (
        HEOSApplicationRunSessionSeverity.SUCCESS
    ),
) -> HEOSApplicationRunSessionPresentation:
    return HEOSApplicationRunSessionPresentation(
        title=title,
        status=status,
        detail=detail,
        runs=runs,
        cycles=cycles,
        severity=severity,
    )


def test_widget_starts_empty() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    assert widget.view is None
    assert not widget.has_data


def test_update_returns_health_view() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    view = widget.update(presentation())

    assert isinstance(view, HEOSApplicationRunSessionHealthView)


def test_update_stores_view() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    view = widget.update(presentation())

    assert widget.view is view
    assert widget.has_data


def test_view_preserves_title() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    view = widget.update(
        presentation(title="HEOS Operations")
    )

    assert view.title == "HEOS Operations"


def test_view_preserves_status() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    view = widget.update(
        presentation(status="HEALTHY")
    )

    assert view.status == "HEALTHY"


def test_view_preserves_detail() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    view = widget.update(
        presentation(
            detail="Completed 5, interrupted 0.",
        )
    )

    assert view.detail == "Completed 5, interrupted 0."


def test_view_preserves_runs() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    view = widget.update(
        presentation(runs="Runs 201")
    )

    assert view.runs == "Runs 201"


def test_view_preserves_cycles() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    view = widget.update(
        presentation(
            cycles="Processed 201, rendered 201.",
        )
    )

    assert view.cycles == "Processed 201, rendered 201."


def test_success_view_is_healthy() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    view = widget.update(
        presentation(
            severity=HEOSApplicationRunSessionSeverity.SUCCESS,
        )
    )

    assert view.healthy
    assert not view.warning
    assert not view.neutral


def test_warning_view_is_warning() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    view = widget.update(
        presentation(
            status="DEGRADED",
            severity=HEOSApplicationRunSessionSeverity.WARNING,
        )
    )

    assert view.warning
    assert not view.healthy
    assert not view.neutral


def test_neutral_view_is_neutral() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    view = widget.update(
        presentation(
            status="IDLE",
            severity=HEOSApplicationRunSessionSeverity.NEUTRAL,
        )
    )

    assert view.neutral
    assert not view.healthy
    assert not view.warning


def test_second_update_replaces_view() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    first = widget.update(
        presentation(status="IDLE")
    )
    second = widget.update(
        presentation(status="HEALTHY")
    )

    assert widget.view is second
    assert widget.view is not first


def test_previous_view_remains_snapshot() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    first = widget.update(
        presentation(
            status="IDLE",
            runs="Runs —",
            severity=HEOSApplicationRunSessionSeverity.NEUTRAL,
        )
    )

    widget.update(
        presentation(
            status="HEALTHY",
            runs="Runs 201",
        )
    )

    assert first.status == "IDLE"
    assert first.runs == "Runs —"
    assert first.neutral


def test_clear_removes_view() -> None:
    widget = HEOSApplicationRunSessionHealthWidget()

    widget.update(presentation())
    widget.clear()

    assert widget.view is None
    assert not widget.has_data
