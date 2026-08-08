from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.layout import Rect
from heos_ui.scene.canvas import CanvasBackend
from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_scene_adapter import BrainSceneLayout


def snapshot(
    *,
    cycle: int = 166,
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


def test_factory_creates_empty_runtime() -> None:
    runtime = BrainRuntimeFactory.create()

    assert not runtime.has_data
    assert runtime.status == "UNKNOWN"
    assert runtime.cycle is None


def test_factory_runtime_accepts_snapshot() -> None:
    runtime = BrainRuntimeFactory.create()

    runtime.event_bus.publish(
        "brain.snapshot",
        snapshot(),
    )

    assert runtime.has_data
    assert runtime.status == "RUNNING"
    assert runtime.cycle == 166


def test_factory_runtime_renders_complete_frame() -> None:
    runtime = BrainRuntimeFactory.create()

    runtime.event_bus.publish(
        "brain.snapshot",
        snapshot(),
    )

    frame = runtime.render()

    assert len(frame) == 7


def test_factory_uses_default_layout() -> None:
    runtime = BrainRuntimeFactory.create()

    runtime.event_bus.publish(
        "brain.snapshot",
        snapshot(),
    )

    frame = runtime.render()
    layout = BrainRuntimeFactory.default_layout()

    assert frame[0].rect == layout.bounds
    assert frame[1].rect == layout.title


def test_factory_accepts_custom_canvas() -> None:
    canvas = CanvasBackend()
    runtime = BrainRuntimeFactory.create(
        canvas=canvas,
    )

    runtime.event_bus.publish(
        "brain.snapshot",
        snapshot(),
    )
    runtime.render()

    assert canvas.command_count == 7


def test_factory_accepts_custom_layout() -> None:
    custom_layout = BrainSceneLayout(
        bounds=Rect(10, 20, 500, 300),
        title=Rect(30, 40, 460, 30),
        status=Rect(30, 80, 200, 24),
        health=Rect(250, 80, 240, 24),
        cycle=Rect(30, 120, 460, 20),
        execution=Rect(30, 160, 460, 20),
        targets=Rect(30, 200, 460, 20),
    )

    runtime = BrainRuntimeFactory.create(
        layout=custom_layout,
    )

    runtime.event_bus.publish(
        "brain.snapshot",
        snapshot(),
    )

    frame = runtime.render()

    assert frame[0].rect == custom_layout.bounds
    assert frame[1].rect == custom_layout.title


def test_factory_accepts_custom_widget_identity() -> None:
    runtime = BrainRuntimeFactory.create(
        widget_id="main-brain",
        title="HEOS Central Brain",
    )

    assert runtime.frame_controller.widget.id == "main-brain"
    assert runtime.frame_controller.widget.title == "HEOS Central Brain"


def test_factory_runtime_reflects_new_snapshot() -> None:
    runtime = BrainRuntimeFactory.create()

    runtime.event_bus.publish(
        "brain.snapshot",
        snapshot(cycle=1),
    )

    assert runtime.cycle == 1

    runtime.event_bus.publish(
        "brain.snapshot",
        snapshot(cycle=166),
    )

    assert runtime.cycle == 166


def test_factory_runtime_handles_degraded_state() -> None:
    runtime = BrainRuntimeFactory.create()

    runtime.event_bus.publish(
        "brain.snapshot",
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        ),
    )

    assert runtime.status == "ATTENTION"
