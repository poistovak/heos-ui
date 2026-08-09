from heos_ui.widgets.heos_application_run_operations_dashboard_canvas_renderer import (
    HEOSApplicationRunOperationsDashboardCanvasRenderer,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_frame_pipeline import (
    HEOSApplicationRunOperationsDashboardFramePipeline,
    HEOSApplicationRunOperationsDashboardFrameResult,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_health_renderer import (
    HEOSApplicationRunOperationsDashboardHealthRenderer,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_health_widget import (
    HEOSApplicationRunOperationsDashboardHealthView,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_presenter import (
    HEOSApplicationRunOperationsDashboardSeverity,
)


def view(
    *,
    title: str = "HEOS Operations Dashboard",
    status: str = "HEALTHY",
    detail: str = "Healthy 223, idle 1.",
    refreshes: str = "Refreshes 224",
    frames: str = "Frames 224",
    sequence: str = "Sequence 224",
    severity: HEOSApplicationRunOperationsDashboardSeverity = (
        HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
    ),
) -> HEOSApplicationRunOperationsDashboardHealthView:
    return HEOSApplicationRunOperationsDashboardHealthView(
        title=title,
        status=status,
        detail=detail,
        refreshes=refreshes,
        frames=frames,
        sequence=sequence,
        severity=severity,
    )


def test_create_builds_pipeline() -> None:
    pipeline = HEOSApplicationRunOperationsDashboardFramePipeline.create()

    assert isinstance(
        pipeline.renderer,
        HEOSApplicationRunOperationsDashboardHealthRenderer,
    )
    assert isinstance(
        pipeline.canvas_renderer,
        HEOSApplicationRunOperationsDashboardCanvasRenderer,
    )


def test_render_returns_frame_result() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view()
        )
    )

    assert isinstance(
        result,
        HEOSApplicationRunOperationsDashboardFrameResult,
    )


def test_pipeline_preserves_scene_title() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(title="HEOS Operations Control")
        )
    )

    assert result.scene.title == "HEOS Operations Control"


def test_pipeline_preserves_scene_status() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(status="HEALTHY")
        )
    )

    assert result.scene.status == "HEALTHY"


def test_pipeline_creates_six_canvas_commands() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view()
        )
    )

    assert result.command_count == 6
    assert result.frame.command_count == 6


def test_pipeline_frame_contains_title() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(title="HEOS Operations Dashboard")
        )
    )

    assert result.frame.commands[0].kind == "title"
    assert (
        result.frame.commands[0].text
        == "HEOS Operations Dashboard"
    )


def test_pipeline_frame_contains_status() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(status="HEALTHY")
        )
    )

    assert result.frame.commands[1].kind == "status"
    assert result.frame.commands[1].text == "HEALTHY"


def test_pipeline_frame_contains_detail() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(detail="Healthy 224, idle 0.")
        )
    )

    assert (
        result.frame.commands[2].text
        == "Detail: Healthy 224, idle 0."
    )


def test_pipeline_frame_contains_refreshes() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(refreshes="Refreshes 224")
        )
    )

    assert (
        result.frame.commands[3].text
        == "Refreshes: Refreshes 224"
    )


def test_pipeline_frame_contains_frames() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(frames="Frames 224")
        )
    )

    assert (
        result.frame.commands[4].text
        == "Frames: Frames 224"
    )


def test_pipeline_frame_contains_sequence() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(sequence="Sequence 224")
        )
    )

    assert (
        result.frame.commands[5].text
        == "Sequence: Sequence 224"
    )


def test_success_severity_flows_through_pipeline() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(
                severity=(
                    HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
                )
            )
        )
    )

    assert (
        result.scene.severity
        is HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
    )
    assert (
        result.frame.severity
        is HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
    )


def test_warning_severity_flows_through_pipeline() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(
                status="DEGRADED",
                severity=(
                    HEOSApplicationRunOperationsDashboardSeverity.WARNING
                ),
            )
        )
    )

    assert (
        result.scene.severity
        is HEOSApplicationRunOperationsDashboardSeverity.WARNING
    )
    assert (
        result.frame.severity
        is HEOSApplicationRunOperationsDashboardSeverity.WARNING
    )


def test_neutral_severity_flows_through_pipeline() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(
                status="IDLE",
                detail="No dashboard refreshes recorded.",
                refreshes="Refreshes —",
                frames="Frames —",
                sequence="Sequence —",
                severity=(
                    HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
                ),
            )
        )
    )

    assert (
        result.scene.severity
        is HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
    )
    assert (
        result.frame.severity
        is HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
    )


def test_custom_canvas_geometry_is_supported() -> None:
    pipeline = HEOSApplicationRunOperationsDashboardFramePipeline(
        renderer=HEOSApplicationRunOperationsDashboardHealthRenderer(),
        canvas_renderer=(
            HEOSApplicationRunOperationsDashboardCanvasRenderer(
                origin_x=40,
                origin_y=20,
                line_height=30,
            )
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
        (40, 170),
    )


def test_result_keeps_scene_and_frame_snapshots() -> None:
    result = (
        HEOSApplicationRunOperationsDashboardFramePipeline.create().render(
            view(
                title="HEOS Operations Dashboard",
                status="HEALTHY",
                sequence="Sequence 224",
            )
        )
    )

    assert result.scene.title == "HEOS Operations Dashboard"
    assert result.scene.status == "HEALTHY"
    assert (
        result.frame.commands[0].text
        == "HEOS Operations Dashboard"
    )
    assert result.frame.commands[1].text == "HEALTHY"
    assert (
        result.frame.commands[5].text
        == "Sequence: Sequence 224"
    )
