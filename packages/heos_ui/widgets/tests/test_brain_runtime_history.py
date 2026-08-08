from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_runtime_history import BrainRuntimeHistory
from heos_ui.widgets.brain_runtime_lifecycle import (
    BrainRuntimeLifecycle,
    BrainRuntimeLifecycleState,
)
from heos_ui.widgets.brain_runtime_session import BrainRuntimeSession


def snapshot(
    *,
    cycle: int = 170,
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


def test_history_starts_empty() -> None:
    history = BrainRuntimeHistory()

    assert history.empty
    assert history.count == 0
    assert history.states == ()
    assert history.latest is None


def test_record_captures_created_state() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    state = history.record(runtime)

    assert state.lifecycle is BrainRuntimeLifecycleState.CREATED
    assert history.count == 1
    assert not history.empty


def test_record_returns_captured_state() -> None:
    runtime = lifecycle()
    runtime.start()

    history = BrainRuntimeHistory()

    state = history.record(runtime)

    assert state is history.latest
    assert state.lifecycle is BrainRuntimeLifecycleState.STARTED


def test_history_preserves_record_order() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    history.record(runtime)

    runtime.start()
    history.record(runtime)

    runtime.publish(
        snapshot(cycle=170)
    )
    history.record(runtime)

    assert history.states[0].lifecycle is BrainRuntimeLifecycleState.CREATED
    assert history.states[1].lifecycle is BrainRuntimeLifecycleState.STARTED
    assert history.states[2].lifecycle is BrainRuntimeLifecycleState.RUNNING


def test_latest_returns_last_record() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()
    history.record(runtime)

    runtime.publish(
        snapshot(cycle=170)
    )
    latest = history.record(runtime)

    assert history.latest is latest
    assert history.latest is not None
    assert history.latest.cycle == 170


def test_history_keeps_previous_cycle_snapshot() -> None:
    runtime = lifecycle()
    runtime.start()
    history = BrainRuntimeHistory()

    runtime.publish(
        snapshot(cycle=1)
    )
    first = history.record(runtime)

    runtime.publish(
        snapshot(cycle=2)
    )
    second = history.record(runtime)

    assert first.cycle == 1
    assert second.cycle == 2
    assert history.states[0].cycle == 1
    assert history.states[1].cycle == 2


def test_history_records_degraded_state() -> None:
    runtime = lifecycle()
    runtime.start()
    history = BrainRuntimeHistory()

    runtime.publish(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    state = history.record(runtime)

    assert state.status == "ATTENTION"


def test_history_records_stopped_state() -> None:
    runtime = lifecycle()
    runtime.start()
    runtime.publish(snapshot())
    runtime.stop()

    history = BrainRuntimeHistory()
    state = history.record(runtime)

    assert state.lifecycle is BrainRuntimeLifecycleState.STOPPED
    assert state.stopped


def test_states_property_is_immutable_view() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    history.record(runtime)

    states = history.states

    assert isinstance(states, tuple)
    assert len(states) == 1


def test_clear_removes_all_history() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    history.record(runtime)
    runtime.start()
    history.record(runtime)

    history.clear()

    assert history.empty
    assert history.count == 0
    assert history.states == ()
    assert history.latest is None


def test_history_can_record_after_clear() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    history.record(runtime)
    history.clear()

    runtime.start()
    state = history.record(runtime)

    assert history.count == 1
    assert history.latest is state
    assert state.lifecycle is BrainRuntimeLifecycleState.STARTED
