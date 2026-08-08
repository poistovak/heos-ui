import pytest
from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.events.bus import EventBus
from heos_ui.widgets.brain_runtime_diagnostics import BrainRuntimeDiagnostics
from heos_ui.widgets.brain_runtime_events import BrainRuntimeEvents
from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_runtime_health import BrainRuntimeHealthAssessor
from heos_ui.widgets.brain_runtime_history import BrainRuntimeHistory
from heos_ui.widgets.brain_runtime_integration import BrainRuntimeIntegration
from heos_ui.widgets.brain_runtime_lifecycle import BrainRuntimeLifecycle
from heos_ui.widgets.brain_runtime_metrics import BrainRuntimeMetrics
from heos_ui.widgets.brain_runtime_orchestrator import BrainRuntimeOrchestrator
from heos_ui.widgets.brain_runtime_recovery import (
    BrainRuntimeRecovery,
    BrainRuntimeRecoveryPolicy,
)
from heos_ui.widgets.brain_runtime_service import (
    BrainRuntimeService,
    BrainRuntimeServiceState,
)
from heos_ui.widgets.brain_runtime_session import BrainRuntimeSession


def snapshot(
    *,
    cycle: int = 178,
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


def service() -> BrainRuntimeService:
    runtime = BrainRuntimeLifecycle(
        session=BrainRuntimeSession(
            runtime=BrainRuntimeFactory.create(),
        )
    )

    orchestrator = BrainRuntimeOrchestrator(
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

    return BrainRuntimeService(
        integration=BrainRuntimeIntegration(
            orchestrator=orchestrator,
        )
    )


def test_service_starts_created() -> None:
    brain = service()

    assert brain.state is BrainRuntimeServiceState.CREATED
    assert not brain.active
    assert not brain.stopped
    assert brain.processed_cycles == 0


def test_start_activates_service() -> None:
    brain = service()

    brain.start()

    assert brain.state is BrainRuntimeServiceState.ACTIVE
    assert brain.active


def test_start_starts_runtime_integration() -> None:
    brain = service()

    brain.start()

    assert brain.integration.started


def test_process_returns_runtime_result() -> None:
    brain = service()
    brain.start()

    result = brain.process(snapshot())

    assert result.cycle == 178
    assert result.rendered


def test_process_counts_cycles() -> None:
    brain = service()
    brain.start()

    brain.process(snapshot(cycle=1))
    brain.process(snapshot(cycle=2))

    assert brain.processed_cycles == 2


def test_last_result_is_exposed() -> None:
    brain = service()
    brain.start()

    result = brain.process(snapshot())

    assert brain.last_result is result


def test_runtime_state_is_exposed() -> None:
    brain = service()
    brain.start()
    brain.process(snapshot(cycle=178))

    state = brain.runtime_state

    assert state.running
    assert state.cycle == 178


def test_diagnostics_are_exposed() -> None:
    brain = service()
    brain.start()
    brain.process(snapshot())

    report = brain.diagnostics

    assert report.latest_cycle == 178
    assert report.healthy


def test_process_before_start_is_rejected() -> None:
    brain = service()

    with pytest.raises(
        RuntimeError,
        match="Cannot process snapshot in service state created",
    ):
        brain.process(snapshot())


def test_service_cannot_start_twice() -> None:
    brain = service()
    brain.start()

    with pytest.raises(
        RuntimeError,
        match="Cannot start runtime service from state active",
    ):
        brain.start()


def test_stop_stops_service_and_runtime() -> None:
    brain = service()
    brain.start()
    brain.process(snapshot())

    brain.stop()

    assert brain.stopped
    assert brain.integration.stopped


def test_process_after_stop_is_rejected() -> None:
    brain = service()
    brain.start()
    brain.stop()

    with pytest.raises(
        RuntimeError,
        match="Cannot process snapshot in service state stopped",
    ):
        brain.process(snapshot())


def test_critical_runtime_stops_service_automatically() -> None:
    brain = service()
    brain.start()

    result = brain.process(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert result.stopped
    assert brain.stopped
    assert brain.processed_cycles == 1


def test_manual_stop_preserves_processed_cycle_count() -> None:
    brain = service()
    brain.start()

    brain.process(snapshot(cycle=1))
    brain.process(snapshot(cycle=2))
    brain.stop()

    assert brain.processed_cycles == 2


def test_stopped_service_cannot_be_stopped_twice() -> None:
    brain = service()
    brain.start()
    brain.stop()

    with pytest.raises(
        RuntimeError,
        match="Cannot stop runtime service from state stopped",
    ):
        brain.stop()
