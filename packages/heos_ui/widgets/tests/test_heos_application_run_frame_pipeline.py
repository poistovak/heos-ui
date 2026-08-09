from heos_ui.widgets.heos_application_run_canvas_renderer import (
    HEOSApplicationRunCanvasRenderer,
)
from heos_ui.widgets.heos_application_run_frame_pipeline import (
    HEOSApplicationRunFramePipeline,
    HEOSApplicationRunFrameResult,
)
from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunSeverity,
)
from heos_ui.widgets.heos_application_run_status import (
    HEOSApplicationRunStatusView,
)
from heos_ui.widgets.heos_application_run_status_renderer import (
    HEOSApplicationRunStatusRenderer,
)


def view(
    *,
    title: str = "HEOS Application",
    status: str = "COMPLETED",
    detail: str = "Processed 3, rendered 3.",
    cycles: str = "Cycles 1–192",
    severity: HEOSApplicationRunSeverity = (
        HEOSApplicationRunSeverity.SUCCESS
    ),
) -> HEOSApplicationRunStatusView:
    return HEOSApplicationRunStatusView(
        title=title,
        status=status,
        detail=detail,
        cycles=cycles,
        severity=severity,
    )


def test_create_builds_pipeline() -> None:
    pipeline = HEOSApplicationRunFramePipeline.create()

    assert isinstance(
        pipeline.renderer,
        HEOSApplicationRunStatusRenderer,
    )
    assert isinstance(
        pipeline.canvas_renderer,
        HEOSApplicationRunCanvasRenderer,
    )


def test_pipeline_returns_frame_result() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view()
    )

    assert isinstance(result, HEOSApplicationRunFrameResult)


def test_pipeline_preserves_scene_title() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view(title="HEOS Runtime")
    )

    assert result.scene.title == "HEOS Runtime"


def test_pipeline_preserves_scene_status() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view(status="COMPLETED")
    )

    assert result.scene.status == "COMPLETED"


def test_pipeline_creates_canvas_commands() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view()
    )

    assert result.command_count == 4
    assert result.frame.command_count == 4


def test_pipeline_frame_contains_title() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view(title="HEOS Runtime")
    )

    assert result.frame.commands[0].kind == "title"
    assert result.frame.commands[0].text == "HEOS Runtime"


def test_pipeline_frame_contains_status() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view(status="COMPLETED")
    )

    assert result.frame.commands[1].kind == "status"
    assert result.frame.commands[1].text == "COMPLETED"


def test_pipeline_frame_contains_detail() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view(
            detail="Processed 7, rendered 7.",
        )
    )

    assert (
        result.frame.commands[2].text
        == "Detail: Processed 7, rendered 7."
    )


def test_pipeline_frame_contains_cycle_range() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view(
            cycles="Cycles 10–192",
        )
    )

    assert result.frame.commands[3].text == "Cycles: Cycles 10–192"


def test_success_severity_flows_through_pipeline() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view(
            severity=HEOSApplicationRunSeverity.SUCCESS,
        )
    )

    assert result.scene.severity is HEOSApplicationRunSeverity.SUCCESS
    assert result.frame.severity is HEOSApplicationRunSeverity.SUCCESS


def test_warning_severity_flows_through_pipeline() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view(
            status="INTERRUPTED",
            severity=HEOSApplicationRunSeverity.WARNING,
        )
    )

    assert result.scene.severity is HEOSApplicationRunSeverity.WARNING
    assert result.frame.severity is HEOSApplicationRunSeverity.WARNING


def test_neutral_severity_flows_through_pipeline() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view(
            status="IDLE",
            severity=HEOSApplicationRunSeverity.NEUTRAL,
        )
    )

    assert result.scene.severity is HEOSApplicationRunSeverity.NEUTRAL
    assert result.frame.severity is HEOSApplicationRunSeverity.NEUTRAL


def test_custom_canvas_geometry_is_supported() -> None:
    pipeline = HEOSApplicationRunFramePipeline(
        renderer=HEOSApplicationRunStatusRenderer(),
        canvas_renderer=HEOSApplicationRunCanvasRenderer(
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
    )


def test_result_keeps_scene_and_frame_snapshots() -> None:
    result = HEOSApplicationRunFramePipeline.create().render(
        view(
            title="HEOS Application",
            status="COMPLETED",
        )
    )

    assert result.scene.title == "HEOS Application"
    assert result.scene.status == "COMPLETED"
    assert result.frame.commands[0].text == "HEOS Application"
    assert result.frame.commands[1].text == "COMPLETED"
