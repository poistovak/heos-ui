from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_runtime_lifecycle import (
    BrainRuntimeLifecycle,
    BrainRuntimeLifecycleState,
)
from heos_ui.widgets.brain_runtime_session import BrainRuntimeSession
from heos_ui.widgets.brain_runtime_state import BrainRuntimeState


def snapshot(
    *,
    cycle: int = 169,
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


def lifecycle() -> BrainRuntimeLifecycle:
    return BrainRuntimeLifecycle(
        session=BrainRuntimeSession(
            runtime=BrainRuntimeFactory.create(),
        )
    )


def test_created_state_is_captured() -> None:
    runtime = lifecycle()

    state = BrainRuntimeState.capture(runtime)

    assert state.lifecycle is BrainRuntimeLifecycleState.CREATED
    assert not state.has_data
    assert state.status == "UNKNOWN"
    assert state.cycle is None


def test_created_state_is_not_started() -> None:
    state = BrainRuntimeState.capture(
        lifecycle()
    )

    assert not state.started
    assert not state.running
    assert not state.stopped


def test_started_state_is_captured() -> None:
    runtime = lifecycle()
    runtime.start()

    state = BrainRuntimeState.capture(runtime)

    assert state.lifecycle is BrainRuntimeLifecycleState.STARTED
    assert state.started
    assert not state.running
    assert not state.stopped


def test_running_state_is_captured() -> None:
    runtime = lifecycle()
    runtime.start()
    runtime.publish(snapshot())

    state = BrainRuntimeState.capture(runtime)

    assert state.lifecycle is BrainRuntimeLifecycleState.RUNNING
    assert state.started
    assert state.running
    assert not state.stopped


def test_running_state_contains_runtime_data() -> None:
    runtime = lifecycle()
    runtime.start()
    runtime.publish(
        snapshot(cycle=169)
    )

    state = BrainRuntimeState.capture(runtime)

    assert state.has_data
    assert state.status == "RUNNING"
    assert state.cycle == 169


def test_state_reflects_latest_cycle() -> None:
    runtime = lifecycle()
    runtime.start()

    runtime.publish(
        snapshot(cycle=1)
    )
    first = BrainRuntimeState.capture(runtime)

    runtime.publish(
        snapshot(cycle=169)
    )
    second = BrainRuntimeState.capture(runtime)

    assert first.cycle == 1
    assert second.cycle == 169


def test_state_reflects_degraded_runtime() -> None:
    runtime = lifecycle()
    runtime.start()

    runtime.publish(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    state = BrainRuntimeState.capture(runtime)

    assert state.has_data
    assert state.status == "ATTENTION"


def test_stopped_state_is_captured() -> None:
    runtime = lifecycle()
    runtime.start()
    runtime.publish(snapshot())
    runtime.stop()

    state = BrainRuntimeState.capture(runtime)

    assert state.lifecycle is BrainRuntimeLifecycleState.STOPPED
    assert state.stopped
    assert not state.running


def test_stopped_state_retains_last_runtime_data() -> None:
    runtime = lifecycle()
    runtime.start()
    runtime.publish(
        snapshot(cycle=169)
    )
    runtime.stop()

    state = BrainRuntimeState.capture(runtime)

    assert state.has_data
    assert state.cycle == 169


def test_state_snapshot_is_immutable() -> None:
    runtime = lifecycle()
    runtime.start()
    runtime.publish(
        snapshot(cycle=1)
    )

    state = BrainRuntimeState.capture(runtime)

    runtime.publish(
        snapshot(cycle=2)
    )

    assert state.cycle == 1


def test_multiple_captures_are_independent() -> None:
    runtime = lifecycle()
    runtime.start()
    runtime.publish(
        snapshot(cycle=10)
    )

    first = BrainRuntimeState.capture(runtime)

    runtime.publish(
        snapshot(cycle=20)
    )

    second = BrainRuntimeState.capture(runtime)

    assert first.cycle == 10
    assert second.cycle == 20
