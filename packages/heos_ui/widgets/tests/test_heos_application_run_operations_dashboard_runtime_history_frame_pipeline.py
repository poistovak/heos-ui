from heos_ui.widgets import (
    heos_application_run_operations_dashboard_runtime_history_frame_pipeline as frame_pipeline,
)
from heos_ui.widgets import (
    heos_application_run_operations_dashboard_runtime_history_health_widget as health_widget,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_presenter import (
    HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity,
)

FramePipeline = (
    frame_pipeline.HEOSApplicationRunOperationsDashboardRuntimeHistoryFramePipeline
)
FrameResult = (
    frame_pipeline.HEOSApplicationRunOperationsDashboardRuntimeHistoryFrameResult
)
HealthView = (
    health_widget.HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView
)


def view(
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
) -> HealthView:
    return HealthView(
        title=title,
        status=status,
        detail=detail,
        cycles=cycles,
        frames=frames,
        latest=latest,
        severity=severity,
    )


def test_create_builds_pipeline() -> None:
    pipeline = FramePipeline.create()

    assert pipeline.health_renderer is not None
    assert pipeline.canvas_renderer is not None


def test_render_returns_frame_result() -> None:
    result = FramePipeline.create().render(view())

    assert isinstance(result, FrameResult)


def test_render_builds_scene() -> None:
    result = FramePipeline.create().render(view())

    assert result.scene.title == "HEOS Operations Dashboard Runtime History"
    assert result.scene.status == "HEALTHY"


def test_render_builds_canvas_frame() -> None:
    result = FramePipeline.create().render(view())

    assert result.frame.command_count == 6


def test_frame_contains_title() -> None:
    result = FramePipeline.create().render(
        view(title="HEOS Runtime Observatory")
    )

    assert result.frame.commands[0].text == "HEOS Runtime Observatory"


def test_frame_contains_status() -> None:
    result = FramePipeline.create().render(
        view(status="HEALTHY")
    )

    assert result.frame.commands[1].text == "HEALTHY"


def test_scene_contains_four_fields() -> None:
    result = FramePipeline.create().render(view())

    assert result.scene.field_count == 4


def test_detail_flows_through_pipeline() -> None:
    result = FramePipeline.create().render(
        view(detail="Healthy 233, idle 2.")
    )

    assert result.scene.fields[0].value == "Healthy 233, idle 2."
    assert result.frame.commands[2].text == "Detail: Healthy 233, idle 2."


def test_cycles_flow_through_pipeline() -> None:
    result = FramePipeline.create().render(
        view(cycles="Cycles 235")
    )

    assert result.scene.fields[1].value == "Cycles 235"
    assert result.frame.commands[3].text == "Cycles: Cycles 235"


def test_frames_flow_through_pipeline() -> None:
    result = FramePipeline.create().render(
        view(frames="Frames 235")
    )

    assert result.scene.fields[2].value == "Frames 235"
    assert result.frame.commands[4].text == "Frames: Frames 235"


def test_latest_cycle_flows_through_pipeline() -> None:
    result = FramePipeline.create().render(
        view(latest="Latest cycle 235")
    )

    assert result.scene.fields[3].value == "Latest cycle 235"
    assert result.frame.commands[5].text == "Latest: Latest cycle 235"


def test_degraded_status_flows_through_pipeline() -> None:
    result = FramePipeline.create().render(
        view(
            status="DEGRADED",
            detail="Degraded 1, healthy 5, idle 0.",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
            ),
        )
    )

    assert result.scene.status == "DEGRADED"
    assert result.frame.commands[1].text == "DEGRADED"


def test_empty_status_flows_through_pipeline() -> None:
    result = FramePipeline.create().render(
        view(
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

    assert result.scene.status == "EMPTY"
    assert result.frame.commands[1].text == "EMPTY"
    assert result.frame.commands[5].text == "Latest: Latest cycle —"


def test_render_is_repeatable() -> None:
    pipeline = FramePipeline.create()
    source = view()

    first = pipeline.render(source)
    second = pipeline.render(source)

    assert first == second
    assert first is not second


def test_previous_result_remains_snapshot() -> None:
    pipeline = FramePipeline.create()

    first = pipeline.render(
        view(
            cycles="Cycles 1",
            frames="Frames 1",
            latest="Latest cycle 1",
        )
    )

    pipeline.render(
        view(
            cycles="Cycles 235",
            frames="Frames 235",
            latest="Latest cycle 235",
        )
    )

    assert first.scene.fields[1].value == "Cycles 1"
    assert first.frame.commands[3].text == "Cycles: Cycles 1"
    assert first.frame.commands[5].text == "Latest: Latest cycle 1"
