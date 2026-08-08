from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.brain_runtime_bootstrap import BrainRuntimeBootstrap
from heos_ui.widgets.brain_runtime_lifecycle import BrainRuntimeLifecycleState
from heos_ui.widgets.brain_runtime_service import (
    BrainRuntimeService,
    BrainRuntimeServiceState,
)


def snapshot(
    *,
    cycle: int = 179,
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


def test_bootstrap_creates_service() -> None:
    service = BrainRuntimeBootstrap.create()

    assert isinstance(service, BrainRuntimeService)


def test_bootstrap_service_starts_created() -> None:
    service = BrainRuntimeBootstrap.create()

    assert service.state is BrainRuntimeServiceState.CREATED
    assert service.processed_cycles == 0


def test_bootstrap_service_can_start() -> None:
    service = BrainRuntimeBootstrap.create()

    service.start()

    assert service.active


def test_bootstrap_starts_inner_runtime() -> None:
    service = BrainRuntimeBootstrap.create()

    service.start()

    assert (
        service.integration.lifecycle
        is BrainRuntimeLifecycleState.STARTED
    )


def test_bootstrap_service_processes_snapshot() -> None:
    service = BrainRuntimeBootstrap.create()
    service.start()

    result = service.process(snapshot())

    assert result.cycle == 179
    assert result.rendered


def test_bootstrap_service_tracks_cycle_count() -> None:
    service = BrainRuntimeBootstrap.create()
    service.start()

    service.process(snapshot(cycle=1))
    service.process(snapshot(cycle=2))

    assert service.processed_cycles == 2


def test_bootstrap_exposes_runtime_state() -> None:
    service = BrainRuntimeBootstrap.create()
    service.start()
    service.process(snapshot(cycle=179))

    state = service.runtime_state

    assert state.running
    assert state.cycle == 179


def test_bootstrap_exposes_diagnostics() -> None:
    service = BrainRuntimeBootstrap.create()
    service.start()
    service.process(snapshot())

    report = service.diagnostics

    assert report.healthy
    assert report.latest_cycle == 179


def test_bootstrap_service_can_stop() -> None:
    service = BrainRuntimeBootstrap.create()
    service.start()
    service.process(snapshot())

    service.stop()

    assert service.stopped
    assert service.integration.stopped


def test_bootstrap_critical_snapshot_stops_service() -> None:
    service = BrainRuntimeBootstrap.create()
    service.start()

    result = service.process(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert result.stopped
    assert service.stopped


def test_bootstrap_creates_independent_services() -> None:
    first = BrainRuntimeBootstrap.create()
    second = BrainRuntimeBootstrap.create()

    first.start()
    first.process(snapshot(cycle=1))

    assert first.processed_cycles == 1
    assert second.processed_cycles == 0
    assert second.state is BrainRuntimeServiceState.CREATED
