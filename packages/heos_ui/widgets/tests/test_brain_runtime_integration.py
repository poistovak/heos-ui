from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.events.bus import EventBus
from heos_ui.widgets.brain_runtime_diagnostics import BrainRuntimeDiagnostics
from heos_ui.widgets.brain_runtime_events import BrainRuntimeEvents
from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_runtime_health import BrainRuntimeHealthAssessor
from heos_ui.widgets.brain_runtime_history import BrainRuntimeHistory
from heos_ui.widgets.brain_runtime_integration import BrainRuntimeIntegration
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
    cycle: int = 177,
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


def integration() -> BrainRuntimeIntegration:
    runtime = BrainRuntimeLifecycle(
        session=BrainRuntimeSession(
            runtime=BrainRuntimeFactory.create(),
        )
    )

    return BrainRuntimeIntegration(
        orchestrator=BrainRuntimeOrchestrator(
            events=BrainRuntimeEvents(
                runtime=runtime,
                event_bus=EventBus(),
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
    )


def test_integration_starts_created() -> None:
    brain = integration()

    assert brain.lifecycle is BrainRuntimeLifecycleState.CREATED
    assert not brain.started
    assert brain.last_result is None


def test_start_exposes_started_runtime() -> None:
    brain = integration()

    brain.start()

    assert brain.started
    assert brain.lifecycle is BrainRuntimeLifecycleState.STARTED


def test_start_records_state_in_history() -> None:
    brain = integration()

    brain.start()

    assert brain.orchestrator.history.count == 1


def test_update_returns_cycle_result() -> None:
    brain = integration()
    brain.start()

    result = brain.update(snapshot())

    assert result.cycle == 177
    assert result.rendered


def test_update_exposes_last_result() -> None:
    brain = integration()
    brain.start()

    result = brain.update(snapshot())

    assert brain.last_result is result


def test_state_exposes_latest_runtime_state() -> None:
    brain = integration()
    brain.start()
    brain.update(snapshot(cycle=177))

    state = brain.state

    assert state.running
    assert state.cycle == 177
    assert state.status == "RUNNING"


def test_diagnostics_exposes_runtime_report() -> None:
    brain = integration()
    brain.start()
    brain.update(snapshot())

    report = brain.diagnostics

    assert report.total_states == 2
    assert report.latest_cycle == 177
    assert report.healthy


def test_multiple_updates_expose_latest_cycle() -> None:
    brain = integration()
    brain.start()

    brain.update(snapshot(cycle=1))
    brain.update(snapshot(cycle=177))

    assert brain.state.cycle == 177
    assert brain.last_result is not None
    assert brain.last_result.cycle == 177


def test_stop_moves_runtime_to_stopped() -> None:
    brain = integration()
    brain.start()
    brain.update(snapshot())

    brain.stop()

    assert brain.stopped
    assert brain.lifecycle is BrainRuntimeLifecycleState.STOPPED


def test_stop_records_stopped_state() -> None:
    brain = integration()
    brain.start()
    brain.update(snapshot())

    brain.stop()

    latest = brain.orchestrator.history.latest

    assert latest is not None
    assert latest.stopped


def test_critical_update_stops_runtime() -> None:
    brain = integration()
    brain.start()

    result = brain.update(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert result.recovery.action is BrainRuntimeRecoveryAction.STOP
    assert brain.stopped
    assert not result.rendered


def test_critical_result_remains_available() -> None:
    brain = integration()
    brain.start()

    result = brain.update(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert brain.last_result is result
    assert result.stopped


def test_integration_hides_orchestrator_cycle_complexity() -> None:
    brain = integration()

    brain.start()
    result = brain.update(snapshot())

    assert result.rendered
    assert brain.running
    assert brain.state.has_data
