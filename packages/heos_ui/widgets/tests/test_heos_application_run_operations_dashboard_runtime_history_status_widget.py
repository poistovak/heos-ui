import importlib

presenter_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_presenter"
)
widget_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_widget"
)

Presentation = (
    presenter_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusPresentation
)
Severity = (
    presenter_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSeverity
)
Widget = (
    widget_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusWidget
)
View = (
    widget_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView
)


def presentation(
    *,
    title: str = "HEOS Runtime History",
    status: str = "RUNNING",
    detail: str = "Runtime history orchestration is active.",
    cycles: str = "Cycles 3",
    runs: str = "Runs 3",
    refreshes: str = "Refreshes 3",
    latest: str = "Latest sequence 3",
    severity: Severity = Severity.ACTIVE,
) -> Presentation:
    return Presentation(
        title=title,
        status=status,
        detail=detail,
        cycles=cycles,
        runs=runs,
        refreshes=refreshes,
        latest=latest,
        severity=severity,
    )


def test_widget_starts_empty() -> None:
    widget = Widget()

    assert widget.view is None
    assert not widget.has_view


def test_update_returns_view() -> None:
    widget = Widget()

    view = widget.update(
        presentation()
    )

    assert isinstance(view, View)


def test_update_stores_view() -> None:
    widget = Widget()

    view = widget.update(
        presentation()
    )

    assert widget.view is view
    assert widget.has_view


def test_update_copies_title() -> None:
    widget = Widget()

    view = widget.update(
        presentation(
            title="HEOS History Observatory"
        )
    )

    assert view.title == "HEOS History Observatory"


def test_update_copies_status() -> None:
    widget = Widget()

    view = widget.update(
        presentation(
            status="RUNNING"
        )
    )

    assert view.status == "RUNNING"


def test_update_copies_detail() -> None:
    widget = Widget()

    view = widget.update(
        presentation(
            detail="Runtime history orchestration is active."
        )
    )

    assert view.detail == "Runtime history orchestration is active."


def test_update_copies_counts() -> None:
    widget = Widget()

    view = widget.update(
        presentation(
            cycles="Cycles 7",
            runs="Runs 6",
            refreshes="Refreshes 5",
        )
    )

    assert view.cycles == "Cycles 7"
    assert view.runs == "Runs 6"
    assert view.refreshes == "Refreshes 5"


def test_update_copies_latest() -> None:
    widget = Widget()

    view = widget.update(
        presentation(
            latest="Latest sequence 42"
        )
    )

    assert view.latest == "Latest sequence 42"


def test_update_copies_severity() -> None:
    widget = Widget()

    view = widget.update(
        presentation(
            severity=Severity.STOPPED
        )
    )

    assert view.severity is Severity.STOPPED


def test_second_update_replaces_view() -> None:
    widget = Widget()

    first = widget.update(
        presentation(
            cycles="Cycles 1",
            latest="Latest sequence 1",
        )
    )
    second = widget.update(
        presentation(
            cycles="Cycles 2",
            latest="Latest sequence 2",
        )
    )

    assert widget.view is second
    assert widget.view is not first


def test_previous_view_remains_snapshot() -> None:
    widget = Widget()

    first = widget.update(
        presentation(
            cycles="Cycles 1",
            latest="Latest sequence 1",
        )
    )

    widget.update(
        presentation(
            cycles="Cycles 2",
            latest="Latest sequence 2",
        )
    )

    assert first.cycles == "Cycles 1"
    assert first.latest == "Latest sequence 1"


def test_clear_removes_view() -> None:
    widget = Widget()

    widget.update(
        presentation()
    )
    widget.clear()

    assert widget.view is None
    assert not widget.has_view


def test_clear_is_idempotent() -> None:
    widget = Widget()

    widget.clear()
    widget.clear()

    assert widget.view is None
    assert not widget.has_view


def test_widget_can_update_after_clear() -> None:
    widget = Widget()

    widget.update(
        presentation()
    )
    widget.clear()

    view = widget.update(
        presentation(
            status="STOPPED",
            severity=Severity.STOPPED,
        )
    )

    assert widget.view is view
    assert view.status == "STOPPED"
    assert view.severity is Severity.STOPPED


def test_idle_presentation_can_be_rendered_as_view() -> None:
    widget = Widget()

    view = widget.update(
        presentation(
            status="IDLE",
            detail="Runtime history has not produced an update.",
            cycles="Cycles 0",
            runs="Runs 0",
            refreshes="Refreshes 0",
            latest="Latest sequence —",
            severity=Severity.NEUTRAL,
        )
    )

    assert view.status == "IDLE"
    assert view.cycles == "Cycles 0"
    assert view.runs == "Runs 0"
    assert view.refreshes == "Refreshes 0"
    assert view.latest == "Latest sequence —"
    assert view.severity is Severity.NEUTRAL
