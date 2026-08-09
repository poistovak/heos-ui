from heos_ui.widgets.heos_application_run_session_canvas_renderer import (
    HEOSApplicationRunSessionCanvasRenderer,
)
from heos_ui.widgets.heos_application_run_session_frame_pipeline import (
    HEOSApplicationRunSessionFramePipeline,
    HEOSApplicationRunSessionFrameResult,
)
from heos_ui.widgets.heos_application_run_session_health_renderer import (
    HEOSApplicationRunSessionHealthRenderer,
)
from heos_ui.widgets.heos_application_run_session_health_widget import (
    HEOSApplicationRunSessionHealthView,
)
from heos_ui.widgets.heos_application_run_session_presenter import (
    HEOSApplicationRunSessionSeverity,
)


def view(
    *,
    title: str = "HEOS Live Session",
    status: str = "HEALTHY",
    detail: str = "Completed 4, interrupted 0.",
    runs: str = "Runs 4",
    cycles: str = "Processed 8, rendered 8.",
    severity: HEOSApplicationRunSessionSeverity = (
        HEOSApplicationRunSessionSeverity.SUCCESS
    ),
) -> HEOSApplicationRunSessionHealthView:
    return HEOSApplicationRunSessionHealthView(
        title=title,
        status=status,
        detail=detail,
        runs=runs,
        cycles=cycles,
        severity=severity,
    )


def test_create_builds_pipeline() -> None:
    pipeline = HEOSApplicationRunSessionFramePipeline.create()

    assert isinstance(
        pipeline.renderer,
        HEOSApplicationRunSessionHealthRenderer,
    )
    assert isinstance(
        pipeline.canvas_renderer,
        HEOSApplicationRunSessionCanvasRenderer,
    )


def test_render_returns_frame_result() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view()
    )

    assert isinstance(
        result,
        HEOSApplicationRunSessionFrameResult,
    )


def test_pipeline_preserves_scene_title() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view(title="HEOS Operations")
    )

    assert result.scene.title == "HEOS Operations"


def test_pipeline_preserves_scene_status() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view(status="HEALTHY")
    )

    assert result.scene.status == "HEALTHY"


def test_pipeline_creates_five_canvas_commands() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view()
    )

    assert result.command_count == 5
    assert result.frame.command_count == 5


def test_pipeline_frame_contains_title() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view(title="HEOS Operations")
    )

    assert result.frame.commands[0].kind == "title"
    assert result.frame.commands[0].text == "HEOS Operations"


def test_pipeline_frame_contains_status() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view(status="HEALTHY")
    )

    assert result.frame.commands[1].kind == "status"
    assert result.frame.commands[1].text == "HEALTHY"


def test_pipeline_frame_contains_detail() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view(detail="Completed 204, interrupted 0.")
    )

    assert (
        result.frame.commands[2].text
        == "Detail: Completed 204, interrupted 0."
    )


def test_pipeline_frame_contains_runs() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view(runs="Runs 204")
    )

    assert result.frame.commands[3].text == "Runs: Runs 204"


def test_pipeline_frame_contains_cycles() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view(cycles="Processed 204, rendered 204.")
    )

    assert (
        result.frame.commands[4].text
        == "Cycles: Processed 204, rendered 204."
    )


def test_success_severity_flows_through_pipeline() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view(
            severity=HEOSApplicationRunSessionSeverity.SUCCESS,
        )
    )

    assert (
        result.scene.severity
        is HEOSApplicationRunSessionSeverity.SUCCESS
    )
    assert (
        result.frame.severity
        is HEOSApplicationRunSessionSeverity.SUCCESS
    )


def test_warning_severity_flows_through_pipeline() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view(
            status="DEGRADED",
            severity=HEOSApplicationRunSessionSeverity.WARNING,
        )
    )

    assert (
        result.scene.severity
        is HEOSApplicationRunSessionSeverity.WARNING
    )
    assert (
        result.frame.severity
        is HEOSApplicationRunSessionSeverity.WARNING
    )


def test_neutral_severity_flows_through_pipeline() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view(
            status="IDLE",
            severity=HEOSApplicationRunSessionSeverity.NEUTRAL,
        )
    )

    assert (
        result.scene.severity
        is HEOSApplicationRunSessionSeverity.NEUTRAL
    )
    assert (
        result.frame.severity
        is HEOSApplicationRunSessionSeverity.NEUTRAL
    )


def test_custom_canvas_geometry_is_supported() -> None:
    pipeline = HEOSApplicationRunSessionFramePipeline(
        renderer=HEOSApplicationRunSessionHealthRenderer(),
        canvas_renderer=HEOSApplicationRunSessionCanvasRenderer(
            origin_x=40,
            origin_y=20,
            line_height=30,
        ),
    )

    result = pipeline.render(view())

    assert tuple(
        (command.x, command.y)
        for command in result.frame.commands
    ) == (
        (40, 20),
        (40, 50),
        (40, 80),
        (40, 110),
        (40, 140),
    )


def test_result_keeps_scene_and_frame_snapshots() -> None:
    result = HEOSApplicationRunSessionFramePipeline.create().render(
        view(
            title="HEOS Live Session",
            status="HEALTHY",
        )
    )

    assert result.scene.title == "HEOS Live Session"
    assert result.scene.status == "HEALTHY"
    assert result.frame.commands[0].text == "HEOS Live Session"
    assert result.frame.commands[1].text == "HEALTHY"
