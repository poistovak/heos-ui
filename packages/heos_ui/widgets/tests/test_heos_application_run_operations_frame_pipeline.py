from heos_ui.widgets.heos_application_run_operations_canvas_renderer import (
    HEOSApplicationRunOperationsCanvasRenderer,
)
from heos_ui.widgets.heos_application_run_operations_frame_pipeline import (
    HEOSApplicationRunOperationsFramePipeline,
    HEOSApplicationRunOperationsFrameResult,
)
from heos_ui.widgets.heos_application_run_operations_health_renderer import (
    HEOSApplicationRunOperationsHealthRenderer,
)
from heos_ui.widgets.heos_application_run_operations_health_widget import (
    HEOSApplicationRunOperationsHealthView,
)
from heos_ui.widgets.heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsSeverity,
)


def view(
    *,
    title: str = "HEOS Operations",
    status: str = "HEALTHY",
    detail: str = "Healthy 213, idle 1.",
    updates: str = "Updates 214",
    frames: str = "Frames 214",
    severity: HEOSApplicationRunOperationsSeverity = (
        HEOSApplicationRunOperationsSeverity.SUCCESS
    ),
) -> HEOSApplicationRunOperationsHealthView:
    return HEOSApplicationRunOperationsHealthView(
        title=title,
        status=status,
        detail=detail,
        updates=updates,
        frames=frames,
        severity=severity,
    )


def test_create_builds_pipeline() -> None:
    pipeline = HEOSApplicationRunOperationsFramePipeline.create()

    assert isinstance(
        pipeline.renderer,
        HEOSApplicationRunOperationsHealthRenderer,
    )
    assert isinstance(
        pipeline.canvas_renderer,
        HEOSApplicationRunOperationsCanvasRenderer,
    )


def test_render_returns_frame_result() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view()
    )

    assert isinstance(
        result,
        HEOSApplicationRunOperationsFrameResult,
    )


def test_pipeline_preserves_scene_title() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view(title="HEOS Operations Health")
    )

    assert result.scene.title == "HEOS Operations Health"


def test_pipeline_preserves_scene_status() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view(status="HEALTHY")
    )

    assert result.scene.status == "HEALTHY"


def test_pipeline_creates_five_canvas_commands() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view()
    )

    assert result.command_count == 5
    assert result.frame.command_count == 5


def test_pipeline_frame_contains_title() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view(title="HEOS Operations")
    )

    assert result.frame.commands[0].kind == "title"
    assert result.frame.commands[0].text == "HEOS Operations"


def test_pipeline_frame_contains_status() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view(status="HEALTHY")
    )

    assert result.frame.commands[1].kind == "status"
    assert result.frame.commands[1].text == "HEALTHY"


def test_pipeline_frame_contains_detail() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view(detail="Healthy 214, idle 0.")
    )

    assert (
        result.frame.commands[2].text
        == "Detail: Healthy 214, idle 0."
    )


def test_pipeline_frame_contains_updates() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view(updates="Updates 214")
    )

    assert (
        result.frame.commands[3].text
        == "Updates: Updates 214"
    )


def test_pipeline_frame_contains_frames() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view(frames="Frames 214")
    )

    assert (
        result.frame.commands[4].text
        == "Frames: Frames 214"
    )


def test_success_severity_flows_through_pipeline() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view(
            severity=HEOSApplicationRunOperationsSeverity.SUCCESS,
        )
    )

    assert (
        result.scene.severity
        is HEOSApplicationRunOperationsSeverity.SUCCESS
    )
    assert (
        result.frame.severity
        is HEOSApplicationRunOperationsSeverity.SUCCESS
    )


def test_warning_severity_flows_through_pipeline() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view(
            status="DEGRADED",
            severity=HEOSApplicationRunOperationsSeverity.WARNING,
        )
    )

    assert (
        result.scene.severity
        is HEOSApplicationRunOperationsSeverity.WARNING
    )
    assert (
        result.frame.severity
        is HEOSApplicationRunOperationsSeverity.WARNING
    )


def test_neutral_severity_flows_through_pipeline() -> None:
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view(
            status="IDLE",
            severity=HEOSApplicationRunOperationsSeverity.NEUTRAL,
        )
    )

    assert (
        result.scene.severity
        is HEOSApplicationRunOperationsSeverity.NEUTRAL
    )
    assert (
        result.frame.severity
        is HEOSApplicationRunOperationsSeverity.NEUTRAL
    )


def test_custom_canvas_geometry_is_supported() -> None:
    pipeline = HEOSApplicationRunOperationsFramePipeline(
        renderer=HEOSApplicationRunOperationsHealthRenderer(),
        canvas_renderer=HEOSApplicationRunOperationsCanvasRenderer(
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
    result = HEOSApplicationRunOperationsFramePipeline.create().render(
        view(
            title="HEOS Operations",
            status="HEALTHY",
        )
    )

    assert result.scene.title == "HEOS Operations"
    assert result.scene.status == "HEALTHY"
    assert result.frame.commands[0].text == "HEOS Operations"
    assert result.frame.commands[1].text == "HEALTHY"
