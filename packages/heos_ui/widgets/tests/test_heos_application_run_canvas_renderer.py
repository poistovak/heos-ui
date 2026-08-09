from heos_ui.widgets.heos_application_run_canvas_renderer import (
    HEOSApplicationRunCanvasFrame,
    HEOSApplicationRunCanvasRenderer,
)
from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunSeverity,
)
from heos_ui.widgets.heos_application_run_status_renderer import (
    HEOSApplicationRunRenderField,
    HEOSApplicationRunRenderScene,
)


def scene(
    *,
    title: str = "HEOS Application",
    status: str = "COMPLETED",
    severity: HEOSApplicationRunSeverity = (
        HEOSApplicationRunSeverity.SUCCESS
    ),
) -> HEOSApplicationRunRenderScene:
    return HEOSApplicationRunRenderScene(
        title=title,
        status=status,
        severity=severity,
        fields=(
            HEOSApplicationRunRenderField(
                label="Detail",
                value="Processed 3, rendered 3.",
            ),
            HEOSApplicationRunRenderField(
                label="Cycles",
                value="Cycles 1–191",
            ),
        ),
    )


def test_renderer_returns_canvas_frame() -> None:
    frame = HEOSApplicationRunCanvasRenderer().render(scene())

    assert isinstance(frame, HEOSApplicationRunCanvasFrame)


def test_frame_contains_four_commands() -> None:
    frame = HEOSApplicationRunCanvasRenderer().render(scene())

    assert frame.command_count == 4


def test_first_command_is_title() -> None:
    frame = HEOSApplicationRunCanvasRenderer().render(scene())

    command = frame.commands[0]

    assert command.kind == "title"
    assert command.text == "HEOS Application"


def test_second_command_is_status() -> None:
    frame = HEOSApplicationRunCanvasRenderer().render(scene())

    command = frame.commands[1]

    assert command.kind == "status"
    assert command.text == "COMPLETED"


def test_detail_field_becomes_canvas_command() -> None:
    frame = HEOSApplicationRunCanvasRenderer().render(scene())

    command = frame.commands[2]

    assert command.kind == "field"
    assert command.text == "Detail: Processed 3, rendered 3."


def test_cycles_field_becomes_canvas_command() -> None:
    frame = HEOSApplicationRunCanvasRenderer().render(scene())

    command = frame.commands[3]

    assert command.kind == "field"
    assert command.text == "Cycles: Cycles 1–191"


def test_commands_use_vertical_layout() -> None:
    frame = HEOSApplicationRunCanvasRenderer().render(scene())

    assert tuple(command.y for command in frame.commands) == (
        16,
        44,
        72,
        100,
    )


def test_commands_share_origin_x() -> None:
    frame = HEOSApplicationRunCanvasRenderer().render(scene())

    assert all(
        command.x == 16
        for command in frame.commands
    )


def test_custom_layout_is_respected() -> None:
    renderer = HEOSApplicationRunCanvasRenderer(
        origin_x=40,
        origin_y=20,
        line_height=30,
    )

    frame = renderer.render(scene())

    assert tuple(
        (command.x, command.y)
        for command in frame.commands
    ) == (
        (40, 20),
        (40, 50),
        (40, 80),
        (40, 110),
    )


def test_success_severity_flows_to_frame() -> None:
    frame = HEOSApplicationRunCanvasRenderer().render(
        scene(
            severity=HEOSApplicationRunSeverity.SUCCESS,
        )
    )

    assert frame.severity is HEOSApplicationRunSeverity.SUCCESS


def test_warning_severity_flows_to_frame() -> None:
    frame = HEOSApplicationRunCanvasRenderer().render(
        scene(
            status="INTERRUPTED",
            severity=HEOSApplicationRunSeverity.WARNING,
        )
    )

    assert frame.severity is HEOSApplicationRunSeverity.WARNING


def test_neutral_severity_flows_to_frame() -> None:
    frame = HEOSApplicationRunCanvasRenderer().render(
        scene(
            status="IDLE",
            severity=HEOSApplicationRunSeverity.NEUTRAL,
        )
    )

    assert frame.severity is HEOSApplicationRunSeverity.NEUTRAL


def test_canvas_frame_is_snapshot() -> None:
    source = scene()

    frame = HEOSApplicationRunCanvasRenderer().render(source)

    assert frame.commands[0].text == "HEOS Application"
    assert frame.commands[1].text == "COMPLETED"
    assert frame.command_count == 4
