from heos_ui.layout import Rect
from heos_ui.scene.canvas import CanvasBackend
from heos_ui.widgets.brain_canvas_renderer import BrainCanvasRenderer
from heos_ui.widgets.brain_frame_pipeline import BrainFramePipeline
from heos_ui.widgets.brain_presenter import (
    BrainStatusPresentation,
    BrainStatusSeverity,
)
from heos_ui.widgets.brain_renderer import BrainStatusRenderer
from heos_ui.widgets.brain_scene_adapter import (
    BrainSceneAdapter,
    BrainSceneLayout,
)


def presentation() -> BrainStatusPresentation:
    return BrainStatusPresentation(
        title="HEOS Brain",
        status="RUNNING",
        health="HEALTHY",
        cycle="Cycle 162",
        execution="Execution 100%",
        targets="Targets 5/5 healthy",
        severity=BrainStatusSeverity.NORMAL,
    )


def layout() -> BrainSceneLayout:
    return BrainSceneLayout(
        bounds=Rect(0, 0, 300, 200),
        title=Rect(16, 16, 268, 24),
        status=Rect(16, 48, 120, 24),
        health=Rect(148, 48, 136, 24),
        cycle=Rect(16, 88, 268, 20),
        execution=Rect(16, 120, 268, 20),
        targets=Rect(16, 152, 268, 20),
    )


def pipeline(
    canvas: CanvasBackend | None = None,
) -> BrainFramePipeline:
    return BrainFramePipeline(
        renderer=BrainStatusRenderer(),
        adapter=BrainSceneAdapter(),
        canvas_renderer=BrainCanvasRenderer(
            canvas=canvas or CanvasBackend(),
        ),
    )


def test_pipeline_returns_complete_frame() -> None:
    frame = pipeline().render(
        presentation(),
        layout(),
    )

    assert len(frame) == 7


def test_frame_starts_with_card_rect() -> None:
    frame = pipeline().render(
        presentation(),
        layout(),
    )

    assert frame[0].command == "rect"
    assert frame[0].rect == layout().bounds


def test_frame_contains_title_command() -> None:
    frame = pipeline().render(
        presentation(),
        layout(),
    )

    assert frame[1].command == "text"
    assert frame[1].rect == layout().title


def test_frame_contains_status_command() -> None:
    frame = pipeline().render(
        presentation(),
        layout(),
    )

    assert frame[2].rect == layout().status


def test_frame_contains_health_command() -> None:
    frame = pipeline().render(
        presentation(),
        layout(),
    )

    assert frame[3].rect == layout().health


def test_frame_contains_runtime_fields() -> None:
    frame = pipeline().render(
        presentation(),
        layout(),
    )

    assert frame[4].rect == layout().cycle
    assert frame[5].rect == layout().execution
    assert frame[6].rect == layout().targets


def test_pipeline_submits_commands_to_canvas() -> None:
    canvas = CanvasBackend()
    brain_pipeline = pipeline(canvas)

    brain_pipeline.render(
        presentation(),
        layout(),
    )

    assert canvas.command_count == 7


def test_second_render_replaces_previous_frame() -> None:
    canvas = CanvasBackend()
    brain_pipeline = pipeline(canvas)

    first = brain_pipeline.render(
        presentation(),
        layout(),
    )
    second = brain_pipeline.render(
        presentation(),
        layout(),
    )

    assert len(first) == 7
    assert len(second) == 7
    assert canvas.command_count == 7
