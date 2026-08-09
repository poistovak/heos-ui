from heos_ui.widgets.heos_application_run_operations_canvas_renderer import (
    HEOSApplicationRunOperationsCanvasFrame,
    HEOSApplicationRunOperationsCanvasRenderer,
)
from heos_ui.widgets.heos_application_run_operations_health_renderer import (
    HEOSApplicationRunOperationsRenderField,
    HEOSApplicationRunOperationsRenderScene,
)
from heos_ui.widgets.heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsSeverity,
)


def scene(
    *,
    title: str = "HEOS Operations",
    status: str = "HEALTHY",
    severity: HEOSApplicationRunOperationsSeverity = (
        HEOSApplicationRunOperationsSeverity.SUCCESS
    ),
) -> HEOSApplicationRunOperationsRenderScene:
    return HEOSApplicationRunOperationsRenderScene(
        title=title,
        status=status,
        severity=severity,
        fields=(
            HEOSApplicationRunOperationsRenderField(
                label="Detail",
                value="Healthy 212, idle 1.",
            ),
            HEOSApplicationRunOperationsRenderField(
                label="Updates",
                value="Updates 213",
            ),
            HEOSApplicationRunOperationsRenderField(
                label="Frames",
                value="Frames 213",
            ),
        ),
    )


def test_renderer_returns_canvas_frame() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene()
    )

    assert isinstance(
        frame,
        HEOSApplicationRunOperationsCanvasFrame,
    )


def test_frame_contains_five_commands() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene()
    )

    assert frame.command_count == 5


def test_first_command_is_title() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene()
    )

    command = frame.commands[0]

    assert command.kind == "title"
    assert command.text == "HEOS Operations"


def test_second_command_is_status() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene()
    )

    command = frame.commands[1]

    assert command.kind == "status"
    assert command.text == "HEALTHY"


def test_detail_field_becomes_canvas_command() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene()
    )

    command = frame.commands[2]

    assert command.kind == "field"
    assert command.text == "Detail: Healthy 212, idle 1."


def test_updates_field_becomes_canvas_command() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene()
    )

    command = frame.commands[3]

    assert command.kind == "field"
    assert command.text == "Updates: Updates 213"


def test_frames_field_becomes_canvas_command() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene()
    )

    command = frame.commands[4]

    assert command.kind == "field"
    assert command.text == "Frames: Frames 213"


def test_commands_use_vertical_layout() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene()
    )

    assert tuple(
        command.y
        for command in frame.commands
    ) == (
        16,
        44,
        72,
        100,
        128,
    )


def test_commands_share_origin_x() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene()
    )

    assert all(
        command.x == 16
        for command in frame.commands
    )


def test_custom_geometry_is_respected() -> None:
    renderer = HEOSApplicationRunOperationsCanvasRenderer(
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
        (40, 140),
    )


def test_success_severity_flows_to_frame() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene(
            severity=HEOSApplicationRunOperationsSeverity.SUCCESS,
        )
    )

    assert (
        frame.severity
        is HEOSApplicationRunOperationsSeverity.SUCCESS
    )


def test_warning_severity_flows_to_frame() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene(
            status="DEGRADED",
            severity=HEOSApplicationRunOperationsSeverity.WARNING,
        )
    )

    assert (
        frame.severity
        is HEOSApplicationRunOperationsSeverity.WARNING
    )


def test_neutral_severity_flows_to_frame() -> None:
    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        scene(
            status="IDLE",
            severity=HEOSApplicationRunOperationsSeverity.NEUTRAL,
        )
    )

    assert (
        frame.severity
        is HEOSApplicationRunOperationsSeverity.NEUTRAL
    )


def test_canvas_frame_is_snapshot() -> None:
    source = scene(
        title="HEOS Operations",
        status="HEALTHY",
    )

    frame = HEOSApplicationRunOperationsCanvasRenderer().render(
        source
    )

    assert frame.commands[0].text == "HEOS Operations"
    assert frame.commands[1].text == "HEALTHY"
    assert frame.command_count == 5
