import importlib

live_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_live_renderer"
)
presenter_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_presenter"
)
widget_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_widget"
)

LiveRenderer = (
    live_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusLiveRenderer
)
View = (
    widget_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView
)
Severity = (
    presenter_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSeverity
)


def view(
    *,
    title: str = "HEOS Runtime History",
    status: str = "RUNNING",
    detail: str = "Runtime history orchestration is active.",
    cycles: str = "Cycles 3",
    runs: str = "Runs 3",
    refreshes: str = "Refreshes 3",
    latest: str = "Latest sequence 3",
    severity: Severity = Severity.ACTIVE,
) -> View:
    return View(
        title=title,
        status=status,
        detail=detail,
        cycles=cycles,
        runs=runs,
        refreshes=refreshes,
        latest=latest,
        severity=severity,
    )


def test_live_renderer_starts_empty() -> None:
    renderer = LiveRenderer.create()

    assert renderer.latest_result is None
    assert renderer.latest_frame is None
    assert renderer.render_count == 0
    assert not renderer.has_frame


def test_create_builds_pipeline() -> None:
    renderer = LiveRenderer.create()

    assert renderer.pipeline is not None


def test_render_returns_frame_result() -> None:
    renderer = LiveRenderer.create()

    result = renderer.render(view())

    assert result.scene.status == "RUNNING"
    assert result.frame.command_count == 7


def test_render_stores_latest_result() -> None:
    renderer = LiveRenderer.create()

    result = renderer.render(view())

    assert renderer.latest_result is result


def test_render_stores_latest_frame() -> None:
    renderer = LiveRenderer.create()

    result = renderer.render(view())

    assert renderer.latest_frame is result.frame
    assert renderer.has_frame


def test_first_render_increments_count() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())

    assert renderer.render_count == 1


def test_multiple_renders_increment_count() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())
    renderer.render(view())
    renderer.render(view())

    assert renderer.render_count == 3


def test_latest_result_tracks_last_render() -> None:
    renderer = LiveRenderer.create()

    renderer.render(
        view(
            cycles="Cycles 1",
            latest="Latest sequence 1",
        )
    )
    second = renderer.render(
        view(
            cycles="Cycles 247",
            latest="Latest sequence 247",
        )
    )

    assert renderer.latest_result is second
    assert renderer.latest_frame is second.frame


def test_latest_frame_tracks_status() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view(status="RUNNING"))
    renderer.render(
        view(
            status="STOPPED",
            severity=Severity.STOPPED,
        )
    )

    assert renderer.latest_frame is not None
    assert renderer.latest_frame.commands[1].text == "STOPPED"


def test_previous_result_remains_snapshot() -> None:
    renderer = LiveRenderer.create()

    first = renderer.render(
        view(
            cycles="Cycles 1",
            runs="Runs 1",
            refreshes="Refreshes 1",
            latest="Latest sequence 1",
        )
    )

    renderer.render(
        view(
            cycles="Cycles 247",
            runs="Runs 247",
            refreshes="Refreshes 247",
            latest="Latest sequence 247",
        )
    )

    assert first.frame.commands[3].text == "Cycles: Cycles 1"
    assert first.frame.commands[4].text == "Runs: Runs 1"
    assert first.frame.commands[5].text == "Refreshes: Refreshes 1"
    assert first.frame.commands[6].text == "Latest: Latest sequence 1"


def test_clear_removes_latest_result() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())
    renderer.clear()

    assert renderer.latest_result is None


def test_clear_removes_latest_frame() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())
    renderer.clear()

    assert renderer.latest_frame is None
    assert not renderer.has_frame


def test_clear_preserves_render_count() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())
    renderer.render(view())
    renderer.clear()

    assert renderer.render_count == 2


def test_renderer_can_render_after_clear() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())
    renderer.clear()

    result = renderer.render(
        view(
            cycles="Cycles 247",
            latest="Latest sequence 247",
        )
    )

    assert renderer.latest_result is result
    assert renderer.latest_frame is result.frame
    assert renderer.render_count == 2
    assert renderer.has_frame


def test_idle_view_can_be_rendered() -> None:
    renderer = LiveRenderer.create()

    result = renderer.render(
        view(
            status="IDLE",
            detail="Runtime history has not produced an update.",
            cycles="Cycles 0",
            runs="Runs 0",
            refreshes="Refreshes 0",
            latest="Latest sequence —",
            severity=Severity.NEUTRAL,
        )
    )

    assert result.scene.status == "IDLE"
    assert result.frame.commands[1].text == "IDLE"
    assert result.frame.commands[6].text == "Latest: Latest sequence —"
