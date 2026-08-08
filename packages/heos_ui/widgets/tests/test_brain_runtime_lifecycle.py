import pytest
from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_runtime_lifecycle import (
    BrainRuntimeLifecycle,
    BrainRuntimeLifecycleState,
)
from heos_ui.widgets.brain_runtime_session import BrainRuntimeSession


def snapshot(
    *,
    cycle: int = 168,
) -> BrainRuntimeSnapshot:
    return BrainRuntimeSnapshot(
        cycle_sequence=cycle,
        system_health=SystemHealth.HEALTHY,
        accepted=4,
        blocked=0,
        executed=4,
        healthy_targets=5,
        unhealthy_targets=0,
        successful=True,
    )


def lifecycle() -> BrainRuntimeLifecycle:
    return BrainRuntimeLifecycle(
        session=BrainRuntimeSession(
            runtime=BrainRuntimeFactory.create(),
        )
    )


def test_lifecycle_starts_created() -> None:
    runtime = lifecycle()

    assert runtime.state is BrainRuntimeLifecycleState.CREATED
    assert not runtime.started
    assert not runtime.running
    assert not runtime.stopped


def test_start_moves_to_started() -> None:
    runtime = lifecycle()

    runtime.start()

    assert runtime.state is BrainRuntimeLifecycleState.STARTED
    assert runtime.started
    assert not runtime.running


def test_publish_moves_started_runtime_to_running() -> None:
    runtime = lifecycle()

    runtime.start()
    runtime.publish(snapshot())

    assert runtime.state is BrainRuntimeLifecycleState.RUNNING
    assert runtime.running
    assert runtime.session.cycle == 168


def test_running_runtime_renders_frame() -> None:
    runtime = lifecycle()

    runtime.start()
    runtime.publish(snapshot())

    frame = runtime.render()

    assert len(frame) == 7
    assert frame[0].command == "rect"


def test_stop_moves_running_runtime_to_stopped() -> None:
    runtime = lifecycle()

    runtime.start()
    runtime.publish(snapshot())
    runtime.stop()

    assert runtime.state is BrainRuntimeLifecycleState.STOPPED
    assert runtime.stopped
    assert not runtime.running


def test_started_runtime_can_stop_without_snapshot() -> None:
    runtime = lifecycle()

    runtime.start()
    runtime.stop()

    assert runtime.state is BrainRuntimeLifecycleState.STOPPED


def test_created_runtime_cannot_publish() -> None:
    runtime = lifecycle()

    with pytest.raises(
        RuntimeError,
        match="Cannot publish runtime snapshot in state created",
    ):
        runtime.publish(snapshot())


def test_created_runtime_cannot_render() -> None:
    runtime = lifecycle()

    with pytest.raises(
        RuntimeError,
        match="Cannot render runtime in state created",
    ):
        runtime.render()


def test_started_runtime_cannot_render_before_snapshot() -> None:
    runtime = lifecycle()

    runtime.start()

    with pytest.raises(
        RuntimeError,
        match="Cannot render runtime in state started",
    ):
        runtime.render()


def test_stopped_runtime_rejects_publish() -> None:
    runtime = lifecycle()

    runtime.start()
    runtime.stop()

    with pytest.raises(
        RuntimeError,
        match="Cannot publish runtime snapshot in state stopped",
    ):
        runtime.publish(snapshot())


def test_stopped_runtime_rejects_render() -> None:
    runtime = lifecycle()

    runtime.start()
    runtime.publish(snapshot())
    runtime.stop()

    with pytest.raises(
        RuntimeError,
        match="Cannot render runtime in state stopped",
    ):
        runtime.render()


def test_runtime_cannot_start_twice() -> None:
    runtime = lifecycle()

    runtime.start()

    with pytest.raises(
        RuntimeError,
        match="Cannot start runtime from state started",
    ):
        runtime.start()
