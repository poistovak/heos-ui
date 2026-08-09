import importlib

canvas_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_canvas_renderer"
)
presenter_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_presenter"
)
renderer_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_renderer"
)
widget_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_widget"
)

CanvasCommand = (
    canvas_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasCommand
)
CanvasFrame = (
    canvas_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasFrame
)
CanvasRenderer = (
    canvas_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasRenderer
)
Renderer = (
    renderer_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderer
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


def render_frame(
    source: View | None = None,
) -> CanvasFrame:
    source = source or view()
    scene = Renderer().render(source)
    return CanvasRenderer().render(scene)


def test_canvas_renderer_returns_frame() -> None:
    frame = render_frame()

    assert isinstance(frame, CanvasFrame)


def test_frame_contains_seven_commands() -> None:
    frame = render_frame()

    assert frame.command_count == 7
    assert len(frame.commands) == 7


def test_first_command_contains_title() -> None:
    frame = render_frame(
        view(title="HEOS History Observatory")
    )

    assert frame.commands[0].text == "HEOS History Observatory"
    assert frame.commands[0].row == 0


def test_second_command_contains_status() -> None:
    frame = render_frame(
        view(status="RUNNING")
    )

    assert frame.commands[1].text == "RUNNING"
    assert frame.commands[1].row == 1


def test_detail_command_is_rendered() -> None:
    frame = render_frame()

    assert frame.commands[2].text == (
        "Detail: Runtime history orchestration is active."
    )
    assert frame.commands[2].row == 2


def test_cycles_command_is_rendered() -> None:
    frame = render_frame(
        view(cycles="Cycles 245")
    )

    assert frame.commands[3].text == "Cycles: Cycles 245"
    assert frame.commands[3].row == 3


def test_runs_command_is_rendered() -> None:
    frame = render_frame(
        view(runs="Runs 245")
    )

    assert frame.commands[4].text == "Runs: Runs 245"
    assert frame.commands[4].row == 4


def test_refreshes_command_is_rendered() -> None:
    frame = render_frame(
        view(refreshes="Refreshes 245")
    )

    assert frame.commands[5].text == "Refreshes: Refreshes 245"
    assert frame.commands[5].row == 5


def test_latest_command_is_rendered() -> None:
    frame = render_frame(
        view(latest="Latest sequence 245")
    )

    assert frame.commands[6].text == "Latest: Latest sequence 245"
    assert frame.commands[6].row == 6


def test_commands_have_sequential_rows() -> None:
    frame = render_frame()

    assert tuple(command.row for command in frame.commands) == (
        0,
        1,
        2,
        3,
        4,
        5,
        6,
    )


def test_commands_are_canvas_commands() -> None:
    frame = render_frame()

    assert all(
        isinstance(command, CanvasCommand)
        for command in frame.commands
    )


def test_idle_scene_is_rendered() -> None:
    frame = render_frame(
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

    assert frame.commands[1].text == "IDLE"
    assert frame.commands[3].text == "Cycles: Cycles 0"
    assert frame.commands[6].text == "Latest: Latest sequence —"


def test_stopped_scene_is_rendered() -> None:
    frame = render_frame(
        view(
            status="STOPPED",
            detail="Runtime history orchestration is stopped.",
            severity=Severity.STOPPED,
        )
    )

    assert frame.commands[1].text == "STOPPED"
    assert frame.commands[2].text == (
        "Detail: Runtime history orchestration is stopped."
    )


def test_canvas_rendering_is_repeatable() -> None:
    renderer = CanvasRenderer()
    scene = Renderer().render(view())

    first = renderer.render(scene)
    second = renderer.render(scene)

    assert first == second
    assert first is not second
