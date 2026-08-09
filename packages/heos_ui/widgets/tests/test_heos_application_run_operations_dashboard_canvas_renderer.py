from heos_ui.widgets.heos_application_run_operations_dashboard_canvas_renderer import (
    HEOSApplicationRunOperationsDashboardCanvasFrame,
    HEOSApplicationRunOperationsDashboardCanvasRenderer,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_health_renderer import (
    HEOSApplicationRunOperationsDashboardRenderField,
    HEOSApplicationRunOperationsDashboardRenderScene,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_presenter import (
    HEOSApplicationRunOperationsDashboardSeverity,
)


def scene(
    *,
    title: str = "HEOS Operations Dashboard",
    status: str = "HEALTHY",
    severity: HEOSApplicationRunOperationsDashboardSeverity = (
        HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
    ),
) -> HEOSApplicationRunOperationsDashboardRenderScene:
    return HEOSApplicationRunOperationsDashboardRenderScene(
        title=title,
        status=status,
        severity=severity,
        fields=(
            HEOSApplicationRunOperationsDashboardRenderField(
                label="Detail",
                value="Healthy 222, idle 1.",
            ),
            HEOSApplicationRunOperationsDashboardRenderField(
                label="Refreshes",
                value="Refreshes 223",
            ),
            HEOSApplicationRunOperationsDashboardRenderField(
                label="Frames",
                value="Frames 223",
            ),
            HEOSApplicationRunOperationsDashboardRenderField(
                label="Sequence",
                value="Sequence 223",
            ),
        ),
    )


def test_renderer_returns_canvas_frame() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene()
        )
    )

    assert isinstance(
        frame,
        HEOSApplicationRunOperationsDashboardCanvasFrame,
    )


def test_frame_contains_six_commands() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene()
        )
    )

    assert frame.command_count == 6
    assert len(frame.commands) == 6


def test_first_command_is_title() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene()
        )
    )

    command = frame.commands[0]

    assert command.kind == "title"
    assert command.text == "HEOS Operations Dashboard"


def test_second_command_is_status() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene()
        )
    )

    command = frame.commands[1]

    assert command.kind == "status"
    assert command.text == "HEALTHY"


def test_detail_field_becomes_canvas_command() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene()
        )
    )

    command = frame.commands[2]

    assert command.kind == "field"
    assert command.text == "Detail: Healthy 222, idle 1."


def test_refreshes_field_becomes_canvas_command() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene()
        )
    )

    command = frame.commands[3]

    assert command.kind == "field"
    assert command.text == "Refreshes: Refreshes 223"


def test_frames_field_becomes_canvas_command() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene()
        )
    )

    command = frame.commands[4]

    assert command.kind == "field"
    assert command.text == "Frames: Frames 223"


def test_sequence_field_becomes_canvas_command() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene()
        )
    )

    command = frame.commands[5]

    assert command.kind == "field"
    assert command.text == "Sequence: Sequence 223"


def test_commands_use_vertical_layout() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene()
        )
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
        156,
    )


def test_commands_share_origin_x() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene()
        )
    )

    assert all(
        command.x == 16
        for command in frame.commands
    )


def test_custom_geometry_is_respected() -> None:
    renderer = HEOSApplicationRunOperationsDashboardCanvasRenderer(
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
        (40, 170),
    )


def test_success_severity_flows_to_frame() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene(
                severity=(
                    HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
                ),
            )
        )
    )

    assert (
        frame.severity
        is HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
    )


def test_warning_severity_flows_to_frame() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene(
                status="DEGRADED",
                severity=(
                    HEOSApplicationRunOperationsDashboardSeverity.WARNING
                ),
            )
        )
    )

    assert (
        frame.severity
        is HEOSApplicationRunOperationsDashboardSeverity.WARNING
    )


def test_neutral_severity_flows_to_frame() -> None:
    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            scene(
                status="IDLE",
                severity=(
                    HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
                ),
            )
        )
    )

    assert (
        frame.severity
        is HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
    )


def test_canvas_frame_is_snapshot() -> None:
    source = scene(
        title="HEOS Operations Dashboard",
        status="HEALTHY",
    )

    frame = (
        HEOSApplicationRunOperationsDashboardCanvasRenderer().render(
            source
        )
    )

    assert frame.commands[0].text == "HEOS Operations Dashboard"
    assert frame.commands[1].text == "HEALTHY"
    assert frame.commands[3].text == "Refreshes: Refreshes 223"
    assert frame.commands[5].text == "Sequence: Sequence 223"
    assert frame.command_count == 6
