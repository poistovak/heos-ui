from heos_ui.widgets.heos_application_run_session_canvas_renderer import (
    HEOSApplicationRunSessionCanvasFrame,
    HEOSApplicationRunSessionCanvasRenderer,
)
from heos_ui.widgets.heos_application_run_session_health_renderer import (
    HEOSApplicationRunSessionRenderField,
    HEOSApplicationRunSessionRenderScene,
)
from heos_ui.widgets.heos_application_run_session_presenter import (
    HEOSApplicationRunSessionSeverity,
)


def scene(
    *,
    title: str = "HEOS Live Session",
    status: str = "HEALTHY",
    severity: HEOSApplicationRunSessionSeverity = (
        HEOSApplicationRunSessionSeverity.SUCCESS
    ),
) -> HEOSApplicationRunSessionRenderScene:
    return HEOSApplicationRunSessionRenderScene(
        title=title,
        status=status,
        severity=severity,
        fields=(
            HEOSApplicationRunSessionRenderField(
                label="Detail",
                value="Completed 3, interrupted 0.",
            ),
            HEOSApplicationRunSessionRenderField(
                label="Runs",
                value="Runs 203",
            ),
            HEOSApplicationRunSessionRenderField(
                label="Cycles",
                value="Processed 203, rendered 203.",
            ),
        ),
    )


def test_renderer_returns_canvas_frame() -> None:
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        scene()
    )

    assert isinstance(
        frame,
        HEOSApplicationRunSessionCanvasFrame,
    )


def test_frame_contains_five_commands() -> None:
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        scene()
    )

    assert frame.command_count == 5


def test_first_command_is_title() -> None:
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        scene()
    )

    command = frame.commands[0]

    assert command.kind == "title"
    assert command.text == "HEOS Live Session"


def test_second_command_is_status() -> None:
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        scene()
    )

    command = frame.commands[1]

    assert command.kind == "status"
    assert command.text == "HEALTHY"


def test_detail_field_becomes_canvas_command() -> None:
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        scene()
    )

    command = frame.commands[2]

    assert command.kind == "field"
    assert (
        command.text
        == "Detail: Completed 3, interrupted 0."
    )


def test_runs_field_becomes_canvas_command() -> None:
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        scene()
    )

    command = frame.commands[3]

    assert command.kind == "field"
    assert command.text == "Runs: Runs 203"


def test_cycles_field_becomes_canvas_command() -> None:
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        scene()
    )

    command = frame.commands[4]

    assert command.kind == "field"
    assert (
        command.text
        == "Cycles: Processed 203, rendered 203."
    )


def test_commands_use_vertical_layout() -> None:
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
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
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        scene()
    )

    assert all(
        command.x == 16
        for command in frame.commands
    )


def test_custom_geometry_is_respected() -> None:
    renderer = HEOSApplicationRunSessionCanvasRenderer(
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
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        scene(
            severity=HEOSApplicationRunSessionSeverity.SUCCESS,
        )
    )

    assert (
        frame.severity
        is HEOSApplicationRunSessionSeverity.SUCCESS
    )


def test_warning_severity_flows_to_frame() -> None:
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        scene(
            status="DEGRADED",
            severity=HEOSApplicationRunSessionSeverity.WARNING,
        )
    )

    assert (
        frame.severity
        is HEOSApplicationRunSessionSeverity.WARNING
    )


def test_neutral_severity_flows_to_frame() -> None:
    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        scene(
            status="IDLE",
            severity=HEOSApplicationRunSessionSeverity.NEUTRAL,
        )
    )

    assert (
        frame.severity
        is HEOSApplicationRunSessionSeverity.NEUTRAL
    )


def test_canvas_frame_is_snapshot() -> None:
    source = scene()

    frame = HEOSApplicationRunSessionCanvasRenderer().render(
        source
    )

    assert frame.commands[0].text == "HEOS Live Session"
    assert frame.commands[1].text == "HEALTHY"
    assert frame.command_count == 5
