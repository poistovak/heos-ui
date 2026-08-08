from heos_ui.binding.brain_status import BrainStatusBinding
from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.events.bus import EventBus
from heos_ui.layout import Rect
from heos_ui.scene.canvas import CanvasBackend
from heos_ui.widgets.brain_canvas_renderer import BrainCanvasRenderer
from heos_ui.widgets.brain_frame_controller import BrainFrameController
from heos_ui.widgets.brain_frame_pipeline import BrainFramePipeline
from heos_ui.widgets.brain_live_renderer import BrainLiveRenderer
from heos_ui.widgets.brain_presenter import BrainStatusPresenter
from heos_ui.widgets.brain_renderer import BrainStatusRenderer
from heos_ui.widgets.brain_runtime_controller import BrainRuntimeController
from heos_ui.widgets.brain_scene_adapter import (
    BrainSceneAdapter,
    BrainSceneLayout,
)
from heos_ui.widgets.brain_status import BrainStatusWidget


def snapshot(
    *,
    cycle: int = 165,
    health: SystemHealth = SystemHealth.HEALTHY,
    successful: bool = True,
) -> BrainRuntimeSnapshot:
    return BrainRuntimeSnapshot(
        cycle_sequence=cycle,
        system_health=health,
        accepted=4,
        blocked=0,
        executed=4,
        healthy_targets=5,
        unhealthy_targets=0,
        successful=successful,
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


def runtime(
    canvas: CanvasBackend | None = None,
) -> BrainRuntimeController:
    event_bus = EventBus()
    widget = BrainStatusWidget(
        id="brain-status",
        title="HEOS Brain",
    )

    binding = BrainStatusBinding(
        event_bus=event_bus,
        widget=widget,
    )

    backend = canvas or CanvasBackend()

    live_renderer = BrainLiveRenderer(
        presenter=BrainStatusPresenter(),
        pipeline=BrainFramePipeline(
            renderer=BrainStatusRenderer(),
            adapter=BrainSceneAdapter(),
            canvas_renderer=BrainCanvasRenderer(
                canvas=backend,
            ),
        ),
    )

    frame_controller = BrainFrameController(
        widget=widget,
        renderer=live_renderer,
        layout=layout(),
    )

    return BrainRuntimeController(
        event_bus=event_bus,
        binding=binding,
        frame_controller=frame_controller,
    )


def test_runtime_starts_without_data() -> None:
    brain = runtime()

    assert not brain.has_data
    assert brain.status == "UNKNOWN"
    assert brain.cycle is None


def test_snapshot_event_updates_runtime() -> None:
    brain = runtime()

    brain.event_bus.publish(
        "brain.snapshot",
        snapshot(),
    )

    assert brain.has_data
    assert brain.status == "RUNNING"
    assert brain.cycle == 165


def test_runtime_renders_complete_frame() -> None:
    brain = runtime()

    brain.event_bus.publish(
        "brain.snapshot",
        snapshot(),
    )

    frame = brain.render()

    assert len(frame) == 7


def test_runtime_renders_card_bounds() -> None:
    brain = runtime()

    brain.event_bus.publish(
        "brain.snapshot",
        snapshot(),
    )

    frame = brain.render()

    assert frame[0].command == "rect"
    assert frame[0].rect == layout().bounds


def test_runtime_reflects_new_snapshot() -> None:
    brain = runtime()

    brain.event_bus.publish(
        "brain.snapshot",
        snapshot(cycle=1),
    )

    assert brain.cycle == 1

    brain.event_bus.publish(
        "brain.snapshot",
        snapshot(cycle=2),
    )

    assert brain.cycle == 2


def test_degraded_snapshot_changes_status() -> None:
    brain = runtime()

    brain.event_bus.publish(
        "brain.snapshot",
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        ),
    )

    assert brain.status == "ATTENTION"


def test_runtime_submits_frame_to_canvas() -> None:
    canvas = CanvasBackend()
    brain = runtime(canvas)

    brain.event_bus.publish(
        "brain.snapshot",
        snapshot(),
    )

    brain.render()

    assert canvas.command_count == 7


def test_second_render_replaces_canvas_frame() -> None:
    canvas = CanvasBackend()
    brain = runtime(canvas)

    brain.event_bus.publish(
        "brain.snapshot",
        snapshot(cycle=1),
    )
    brain.render()

    brain.event_bus.publish(
        "brain.snapshot",
        snapshot(cycle=2),
    )
    frame = brain.render()

    assert brain.cycle == 2
    assert len(frame) == 7
    assert canvas.command_count == 7
