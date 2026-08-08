from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.decision.brain_view import BrainViewModel
from heos_ui.diagnostics import SystemHealth
from heos_ui.layout import Rect
from heos_ui.scene.canvas import CanvasBackend
from heos_ui.widgets.brain_canvas_renderer import BrainCanvasRenderer
from heos_ui.widgets.brain_frame_controller import BrainFrameController
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
    backend = canvas or CanvasBackend()

    return BrainLiveRenderer(
        presenter=BrainStatusPresenter(),
        pipeline=BrainFramePipeline(
            renderer=BrainStatusRenderer(),
            adapter=BrainSceneAdapter(),
            canvas_renderer=BrainCanvasRenderer(
                canvas=backend,
            ),
        ),
    )


def controller(
    *,
    brain: BrainStatusWidget | None = None,
    canvas: CanvasBackend | None = None,
) -> BrainFrameController:
    return BrainFrameController(
        widget=brain or widget(),
        renderer=live_renderer(canvas),
        layout=layout(),
    )


def update_widget(
    brain: BrainStatusWidget,
    *,
    cycle: int = 164,
    health: SystemHealth = SystemHealth.HEALTHY,
    successful: bool = True,
) -> None:
    snapshot = BrainRuntimeSnapshot(
        cycle_sequence=cycle,
        system_health=health,
        accepted=4,
        blocked=0,
        executed=4,
        healthy_targets=5,
        unhealthy_targets=0,
        successful=successful,
    )

    brain.update(
        BrainViewModel.from_snapshot(snapshot)
    )


def test_controller_starts_without_data() -> None:
    brain_controller = controller()

    assert not brain_controller.has_data
    assert brain_controller.status == "UNKNOWN"


def test_controller_renders_empty_widget() -> None:
    frame = controller().render()

    assert len(frame) == 7


def test_controller_exposes_live_status() -> None:
    brain = widget()
    update_widget(brain)

    brain_controller = controller(brain=brain)

    assert brain_controller.has_data
    assert brain_controller.status == "RUNNING"


def test_controller_exposes_cycle() -> None:
    brain = widget()
    update_widget(
        brain,
        cycle=164,
    )

    brain_controller = controller(brain=brain)

    assert brain_controller.cycle == 164


def test_controller_renders_live_widget() -> None:
    brain = widget()
    update_widget(brain)

    frame = controller(brain=brain).render()

    assert len(frame) == 7
    assert frame[0].command == "rect"


def test_controller_uses_configured_layout() -> None:
    brain = widget()
    update_widget(brain)

    brain_controller = controller(brain=brain)
    frame = brain_controller.render()

    assert frame[0].rect == layout().bounds
    assert frame[1].rect == layout().title


def test_controller_submits_complete_frame() -> None:
    canvas = CanvasBackend()
    brain = widget()
    update_widget(brain)

    brain_controller = controller(
        brain=brain,
        canvas=canvas,
    )

    brain_controller.render()

    assert canvas.command_count == 7


def test_controller_reflects_updated_widget() -> None:
    brain = widget()
    brain_controller = controller(brain=brain)

    update_widget(
        brain,
        cycle=1,
    )
    brain_controller.render()

    update_widget(
        brain,
        cycle=2,
    )
    frame = brain_controller.render()

    assert brain_controller.cycle == 2
    assert len(frame) == 7
