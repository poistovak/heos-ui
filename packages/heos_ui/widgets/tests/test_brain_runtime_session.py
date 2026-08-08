from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_runtime_session import BrainRuntimeSession


def snapshot(
    *,
    cycle: int = 167,
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


def session() -> BrainRuntimeSession:
    return BrainRuntimeSession(
        runtime=BrainRuntimeFactory.create(),
    )


def test_session_starts_empty() -> None:
    brain = session()

    assert not brain.has_data
    assert brain.status == "UNKNOWN"
    assert brain.cycle is None


def test_publish_updates_session() -> None:
    brain = session()

    brain.publish(
        snapshot()
    )

    assert brain.has_data
    assert brain.status == "RUNNING"
    assert brain.cycle == 167


def test_session_renders_complete_frame() -> None:
    brain = session()

    brain.publish(
        snapshot()
    )

    frame = brain.render()

    assert len(frame) == 7
    assert frame[0].command == "rect"


def test_session_reflects_degraded_state() -> None:
    brain = session()

    brain.publish(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert brain.status == "ATTENTION"
