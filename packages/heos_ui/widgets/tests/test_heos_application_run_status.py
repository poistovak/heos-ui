from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunPresentation,
    HEOSApplicationRunSeverity,
)
from heos_ui.widgets.heos_application_run_status import (
    HEOSApplicationRunStatusView,
    HEOSApplicationRunStatusWidget,
)


def presentation(
    *,
    status: str = "COMPLETED",
    detail: str = "Processed 3, rendered 3.",
    cycles: str = "Cycles 1–3",
    severity: HEOSApplicationRunSeverity = (
        HEOSApplicationRunSeverity.SUCCESS
    ),
) -> HEOSApplicationRunPresentation:
    return HEOSApplicationRunPresentation(
        title="HEOS Application",
        status=status,
        detail=detail,
        cycles=cycles,
        severity=severity,
    )


def test_widget_starts_empty() -> None:
    widget = HEOSApplicationRunStatusWidget()

    assert widget.view is None
    assert not widget.has_data


def test_update_creates_view() -> None:
    widget = HEOSApplicationRunStatusWidget()

    view = widget.update(presentation())

    assert isinstance(view, HEOSApplicationRunStatusView)
    assert widget.has_data


def test_update_stores_latest_view() -> None:
    widget = HEOSApplicationRunStatusWidget()

    view = widget.update(presentation())

    assert widget.view is view


def test_view_preserves_title() -> None:
    view = HEOSApplicationRunStatusWidget().update(
        presentation()
    )

    assert view.title == "HEOS Application"


def test_view_preserves_status() -> None:
    view = HEOSApplicationRunStatusWidget().update(
        presentation(status="COMPLETED")
    )

    assert view.status == "COMPLETED"


def test_view_preserves_detail() -> None:
    view = HEOSApplicationRunStatusWidget().update(
        presentation(
            detail="Processed 3, rendered 3.",
        )
    )

    assert view.detail == "Processed 3, rendered 3."


def test_view_preserves_cycles() -> None:
    view = HEOSApplicationRunStatusWidget().update(
        presentation(
            cycles="Cycles 1–187",
        )
    )

    assert view.cycles == "Cycles 1–187"


def test_success_view_is_successful() -> None:
    view = HEOSApplicationRunStatusWidget().update(
        presentation(
            severity=HEOSApplicationRunSeverity.SUCCESS,
        )
    )

    assert view.successful
    assert not view.warning
    assert not view.neutral


def test_warning_view_is_warning() -> None:
    view = HEOSApplicationRunStatusWidget().update(
        presentation(
            status="INTERRUPTED",
            severity=HEOSApplicationRunSeverity.WARNING,
        )
    )

    assert view.warning
    assert not view.successful
    assert not view.neutral


def test_neutral_view_is_neutral() -> None:
    view = HEOSApplicationRunStatusWidget().update(
        presentation(
            status="IDLE",
            severity=HEOSApplicationRunSeverity.NEUTRAL,
        )
    )

    assert view.neutral
    assert not view.successful
    assert not view.warning


def test_second_update_replaces_view() -> None:
    widget = HEOSApplicationRunStatusWidget()

    first = widget.update(
        presentation(
            status="IDLE",
            severity=HEOSApplicationRunSeverity.NEUTRAL,
        )
    )

    second = widget.update(
        presentation(
            status="COMPLETED",
            severity=HEOSApplicationRunSeverity.SUCCESS,
        )
    )

    assert widget.view is second
    assert widget.view is not first
    assert widget.view.status == "COMPLETED"


def test_previous_view_remains_immutable() -> None:
    widget = HEOSApplicationRunStatusWidget()

    first = widget.update(
        presentation(
            status="IDLE",
            detail="No cycles processed.",
            cycles="Cycles —",
            severity=HEOSApplicationRunSeverity.NEUTRAL,
        )
    )

    widget.update(
        presentation(
            status="COMPLETED",
            severity=HEOSApplicationRunSeverity.SUCCESS,
        )
    )

    assert first.status == "IDLE"
    assert first.detail == "No cycles processed."
    assert first.cycles == "Cycles —"


def test_clear_removes_view() -> None:
    widget = HEOSApplicationRunStatusWidget()

    widget.update(presentation())
    widget.clear()

    assert widget.view is None
    assert not widget.has_data
