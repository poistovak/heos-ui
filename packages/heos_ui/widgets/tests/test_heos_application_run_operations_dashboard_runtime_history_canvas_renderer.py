from heos_ui.widgets import (
    heos_application_run_operations_dashboard_runtime_history_canvas_renderer as canvas_renderer,
)
from heos_ui.widgets import (
    heos_application_run_operations_dashboard_runtime_history_health_renderer as history_renderer,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_presenter import (
    HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity,
)

CanvasCommand = (
    canvas_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasCommand
)
CanvasFrame = (
    canvas_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasFrame
)
CanvasRenderer = (
    canvas_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasRenderer
)
RenderField = (
    history_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderField
)
RenderScene = (
    history_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderScene
)


def scene(
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
) -> RenderScene:
    return RenderScene(
        title=title,
        status=status,
        severity=severity,
        fields=(
            RenderField(label="Detail", value=detail),
            RenderField(label="Cycles", value=cycles),
            RenderField(label="Frames", value=frames),
            RenderField(label="Latest", value=latest),
        ),
    )


def test_renderer_returns_canvas_frame() -> None:
    frame = CanvasRenderer().render(scene())

    assert isinstance(frame, CanvasFrame)


def test_frame_contains_six_commands() -> None:
    frame = CanvasRenderer().render(scene())

    assert frame.command_count == 6
    assert len(frame.commands) == 6


def test_first_command_contains_title() -> None:
    frame = CanvasRenderer().render(
        scene(title="HEOS Runtime Observatory")
    )

    assert frame.commands[0].text == "HEOS Runtime Observatory"
    assert frame.commands[0].row == 0


def test_second_command_contains_status() -> None:
    frame = CanvasRenderer().render(
        scene(status="DEGRADED")
    )

    assert frame.commands[1].text == "DEGRADED"
    assert frame.commands[1].row == 1


def test_detail_command_is_rendered() -> None:
    frame = CanvasRenderer().render(
        scene(detail="Healthy 232, idle 2.")
    )

    assert frame.commands[2].text == "Detail: Healthy 232, idle 2."
    assert frame.commands[2].row == 2


def test_cycles_command_is_rendered() -> None:
    frame = CanvasRenderer().render(
        scene(cycles="Cycles 234")
    )

    assert frame.commands[3].text == "Cycles: Cycles 234"
    assert frame.commands[3].row == 3


def test_frames_command_is_rendered() -> None:
    frame = CanvasRenderer().render(
        scene(frames="Frames 234")
    )

    assert frame.commands[4].text == "Frames: Frames 234"
    assert frame.commands[4].row == 4


def test_latest_command_is_rendered() -> None:
    frame = CanvasRenderer().render(
        scene(latest="Latest cycle 234")
    )

    assert frame.commands[5].text == "Latest: Latest cycle 234"
    assert frame.commands[5].row == 5


def test_command_rows_are_sequential() -> None:
    frame = CanvasRenderer().render(scene())

    assert tuple(command.row for command in frame.commands) == (
        0,
        1,
        2,
        3,
        4,
        5,
    )


def test_commands_preserve_scene_field_order() -> None:
    frame = CanvasRenderer().render(scene())

    assert tuple(command.text for command in frame.commands[2:]) == (
        "Detail: Healthy 5, idle 1.",
        "Cycles: Cycles 6",
        "Frames: Frames 6",
        "Latest: Latest cycle 6",
    )


def test_command_is_canvas_command() -> None:
    frame = CanvasRenderer().render(scene())

    assert isinstance(frame.commands[0], CanvasCommand)


def test_degraded_scene_is_rendered() -> None:
    frame = CanvasRenderer().render(
        scene(
            status="DEGRADED",
            detail="Degraded 1, healthy 5, idle 0.",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
            ),
        )
    )

    assert frame.commands[1].text == "DEGRADED"
    assert frame.commands[2].text == "Detail: Degraded 1, healthy 5, idle 0."


def test_empty_scene_is_rendered() -> None:
    frame = CanvasRenderer().render(
        scene(
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

    assert frame.commands[1].text == "EMPTY"
    assert frame.commands[3].text == "Cycles: Cycles 0"
    assert frame.commands[4].text == "Frames: Frames 0"
    assert frame.commands[5].text == "Latest: Latest cycle —"


def test_frame_is_snapshot() -> None:
    source = scene(
        cycles="Cycles 234",
        frames="Frames 234",
        latest="Latest cycle 234",
    )

    frame = CanvasRenderer().render(source)

    assert frame.commands[3].text == "Cycles: Cycles 234"
    assert frame.commands[4].text == "Frames: Frames 234"
    assert frame.commands[5].text == "Latest: Latest cycle 234"


def test_renderer_is_repeatable() -> None:
    renderer = CanvasRenderer()
    source = scene()

    first = renderer.render(source)
    second = renderer.render(source)

    assert first == second
    assert first is not second
