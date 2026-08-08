from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.events.bus import EventBus
from heos_ui.widgets.brain_runtime_diagnostics import BrainRuntimeDiagnostics
from heos_ui.widgets.brain_runtime_events import BrainRuntimeEvents
from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_runtime_health import (
    BrainRuntimeHealthAssessor,
    BrainRuntimeHealthLevel,
)
from heos_ui.widgets.brain_runtime_history import BrainRuntimeHistory
from heos_ui.widgets.brain_runtime_lifecycle import (
    BrainRuntimeLifecycle,
    BrainRuntimeLifecycleState,
)
from heos_ui.widgets.brain_runtime_metrics import BrainRuntimeMetrics
from heos_ui.widgets.brain_runtime_orchestrator import BrainRuntimeOrchestrator
from heos_ui.widgets.brain_runtime_recovery import (
    BrainRuntimeRecovery,
    BrainRuntimeRecoveryAction,
    BrainRuntimeRecoveryPolicy,
)
from heos_ui.widgets.brain_runtime_session import BrainRuntimeSession


def snapshot(
    *,
    cycle: int = 176,
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


def orchestrator() -> BrainRuntimeOrchestrator:
    runtime = BrainRuntimeLifecycle(
        session=BrainRuntimeSession(
            runtime=BrainRuntimeFactory.create(),
        )
    )

    event_bus = EventBus()

    return BrainRuntimeOrchestrator(
        events=BrainRuntimeEvents(
            runtime=runtime,
            event_bus=event_bus,
        ),
        history=BrainRuntimeHistory(),
        diagnostics=BrainRuntimeDiagnostics(),
        recovery=BrainRuntimeRecovery(
            runtime=runtime,
            policy=BrainRuntimeRecoveryPolicy(),
        ),
        metrics=BrainRuntimeMetrics(),
        health_assessor=BrainRuntimeHealthAssessor(),
    )


def test_start_moves_runtime_to_started() -> None:
    brain = orchestrator()

    brain.start()

    assert (
        brain.events.runtime.state
        is BrainRuntimeLifecycleState.STARTED
    )


def test_start_records_initial_runtime_state() -> None:
    brain = orchestrator()

    brain.start()

    assert brain.history.count == 1
    assert (
        brain.history.latest is not None
        and brain.history.latest.lifecycle
        is BrainRuntimeLifecycleState.STARTED
    )


def test_healthy_cycle_runs_to_completion() -> None:
    brain = orchestrator()
    brain.start()

    result = brain.run(snapshot())

    assert result.cycle == 176
    assert result.recovery.action is BrainRuntimeRecoveryAction.CONTINUE
    assert result.rendered


def test_healthy_cycle_returns_complete_frame() -> None:
    brain = orchestrator()
    brain.start()

    result = brain.run(snapshot())

    assert result.frame is not None
    assert len(result.frame) == 7


def test_cycle_records_running_state() -> None:
    brain = orchestrator()
    brain.start()

    brain.run(snapshot())

    assert brain.history.count == 2
    assert brain.history.latest is not None
    assert (
        brain.history.latest.lifecycle
        is BrainRuntimeLifecycleState.RUNNING
    )


def test_healthy_cycle_produces_healthy_diagnostic() -> None:
    brain = orchestrator()
    brain.start()

    result = brain.run(snapshot())

    assert result.diagnostic.health is BrainRuntimeHealthLevel.HEALTHY
    assert result.diagnostic.healthy


def test_orchestrator_health_uses_runtime_history() -> None:
    brain = orchestrator()
    brain.start()
    brain.run(snapshot())

    health = brain.health()

    assert health.level is BrainRuntimeHealthLevel.HEALTHY
    assert health.total_states == 2


def test_latest_cycle_is_visible_after_run() -> None:
    brain = orchestrator()
    brain.start()

    result = brain.run(
        snapshot(cycle=176)
    )

    assert result.cycle == 176
    assert brain.events.runtime.session.cycle == 176


def test_multiple_healthy_cycles_remain_running() -> None:
    brain = orchestrator()
    brain.start()

    first = brain.run(snapshot(cycle=1))
    second = brain.run(snapshot(cycle=176))

    assert first.rendered
    assert second.rendered
    assert brain.events.runtime.running
    assert brain.history.count == 3


def test_degraded_cycle_can_continue_with_caution() -> None:
    brain = orchestrator()
    brain.start()

    brain.run(snapshot(cycle=1))
    brain.run(snapshot(cycle=2))

    result = brain.run(
        snapshot(
            cycle=3,
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert (
        result.recovery.action
        is BrainRuntimeRecoveryAction.CONTINUE_WITH_CAUTION
    )
    assert result.rendered


def test_critical_runtime_stops_without_rendering() -> None:
    brain = orchestrator()
    brain.start()

    result = brain.run(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert result.recovery.action is BrainRuntimeRecoveryAction.STOP
    assert result.stopped
    assert not result.rendered
    assert result.frame is None
    assert brain.events.runtime.stopped


def test_critical_cycle_stops_lifecycle() -> None:
    brain = orchestrator()
    brain.start()

    brain.run(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert (
        brain.events.runtime.state
        is BrainRuntimeLifecycleState.STOPPED
    )


def test_cycle_result_is_snapshot_of_decision() -> None:
    brain = orchestrator()
    brain.start()

    result = brain.run(snapshot(cycle=1))

    assert result.cycle == 1
    assert result.diagnostic.latest_cycle == 1
    assert result.recovery.can_continue
