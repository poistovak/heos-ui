from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.decision.brain_view import BrainViewModel
from heos_ui.diagnostics import SystemHealth
from heos_ui.layout import Rect
from heos_ui.scene.canvas import CanvasBackend
from heos_ui.widgets.brain_canvas_renderer import BrainCanvasRenderer
from heos_ui.widgets.brain_frame_pipeline import BrainFramePipeline
from heos_ui.widgets.brain_live_renderer import BrainLiveRenderer
from heos_ui.widgets.brain_presenter import BrainStatusPresenter
from heos_ui.widgets.brain_renderer import BrainStatusRenderer
from heos_ui.widgets.brain_scene_adapter import (
    BrainSceneAdapter,
    BrainSceneLayout,
)
from heos_ui.widgets.brain_status import BrainStatusWidget


def widget() -> BrainStatusWidget:
    return BrainStatusWidget(
        id="brain-status",
        title="HEOS Brain",
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


def live_renderer(
    canvas: CanvasBackend | None = None,
) -> BrainLiveRenderer:
    canvas_backend = canvas or CanvasBackend()

    return BrainLiveRenderer(
        presenter=BrainStatusPresenter(),
        pipeline=BrainFramePipeline(
            renderer=BrainStatusRenderer(),
            adapter=BrainSceneAdapter(),
            canvas_renderer=BrainCanvasRenderer(
                canvas=canvas_backend,
            ),
        ),
    )


def update_widget(
    brain: BrainStatusWidget,
    *,
    cycle: int = 163,
    health: SystemHealth = SystemHealth.HEALTHY,
    accepted: int = 4,
    blocked: int = 0,
    executed: int = 4,
    healthy_targets: int = 5,
    unhealthy_targets: int = 0,
    successful: bool = True,
) -> None:
    snapshot = BrainRuntimeSnapshot(
        cycle_sequence=cycle,
        system_health=health,
        accepted=accepted,
        blocked=blocked,
        executed=executed,
        healthy_targets=healthy_targets,
        unhealthy_targets=unhealthy_targets,
        successful=successful,
    )

    brain.update(
        BrainViewModel.from_snapshot(snapshot)
    )


def test_empty_widget_renders_frame() -> None:
    frame = live_renderer().render(
        widget(),
        layout(),
    )

    assert len(frame) == 7


def test_live_widget_renders_complete_frame() -> None:
    brain = widget()
    update_widget(brain)

    frame = live_renderer().render(
        brain,
        layout(),
    )

    assert len(frame) == 7


def test_frame_starts_with_bounds_rect() -> None:
    brain = widget()
    update_widget(brain)

    frame = live_renderer().render(
        brain,
        layout(),
    )

    assert frame[0].command == "rect"
    assert frame[0].rect == layout().bounds


def test_widget_cycle_is_rendered() -> None:
    brain = widget()
    update_widget(
        brain,
        cycle=163,
    )

    frame = live_renderer().render(
        brain,
        layout(),
    )

    assert frame[4].rect == layout().cycle


def test_degraded_widget_still_renders() -> None:
    brain = widget()

    update_widget(
        brain,
        health=SystemHealth.DEGRADED,
        successful=False,
    )

    frame = live_renderer().render(
        brain,
        layout(),
    )

    assert len(frame) == 7


def test_render_submits_commands_to_canvas() -> None:
    canvas = CanvasBackend()
    renderer = live_renderer(canvas)
    brain = widget()

    update_widget(brain)

    renderer.render(
        brain,
        layout(),
    )

    assert canvas.command_count == 7


def test_second_render_replaces_frame() -> None:
    canvas = CanvasBackend()
    renderer = live_renderer(canvas)
    brain = widget()

    update_widget(brain, cycle=1)
    renderer.render(
        brain,
        layout(),
    )

    update_widget(brain, cycle=2)
    frame = renderer.render(
        brain,
        layout(),
    )

    assert len(frame) == 7
    assert canvas.command_count == 7


def test_live_renderer_uses_widget_title() -> None:
    brain = BrainStatusWidget(
        id="brain-status",
        title="HEOS Energy Brain",
    )

    update_widget(brain)

    frame = live_renderer().render(
        brain,
        layout(),
    )

    assert frame[1].rect == layout().title
