from heos_ui.decision.brain import BrainCycleReport
from heos_ui.decision.brain_publisher import BrainSnapshotPublisher
from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.decision.runtime_cycle import RuntimeCycleResult
from heos_ui.decision.runtime_report import RuntimeExecutionReport
from heos_ui.diagnostics import SystemHealth
from heos_ui.events.bus import EventBus


def report(
    *,
    sequence: int = 1,
    accepted: int = 1,
    blocked: int = 0,
    executed: int = 1,
    system_health: SystemHealth = SystemHealth.HEALTHY,
) -> BrainCycleReport:
    return BrainCycleReport(
        sequence=sequence,
        cycle=RuntimeCycleResult(
            report=RuntimeExecutionReport(
                accepted=accepted,
                blocked=blocked,
                executed=executed,
            )
        ),
        system_health=system_health,
        healthy_targets=1,
        unhealthy_targets=0,
    )


def test_publish_returns_snapshot() -> None:
    publisher = BrainSnapshotPublisher(
        event_bus=EventBus(),
    )

    snapshot = publisher.publish(report())

    assert isinstance(snapshot, BrainRuntimeSnapshot)


def test_publish_preserves_sequence() -> None:
    publisher = BrainSnapshotPublisher(
        event_bus=EventBus(),
    )

    snapshot = publisher.publish(
        report(sequence=7)
    )

    assert snapshot.cycle_sequence == 7


def test_publish_emits_snapshot_event() -> None:
    event_bus = EventBus()
    received = []

    event_bus.subscribe(
        "brain.snapshot",
        received.append,
    )

    publisher = BrainSnapshotPublisher(
        event_bus=event_bus,
    )

    snapshot = publisher.publish(report())

    assert received == [snapshot]


def test_custom_topic() -> None:
    event_bus = EventBus()
    received = []

    event_bus.subscribe(
        "heos.brain",
        received.append,
    )

    publisher = BrainSnapshotPublisher(
        event_bus=event_bus,
        topic="heos.brain",
    )

    snapshot = publisher.publish(report())

    assert received == [snapshot]


def test_runtime_values_are_preserved() -> None:
    publisher = BrainSnapshotPublisher(
        event_bus=EventBus(),
    )

    snapshot = publisher.publish(
        report(
            accepted=3,
            blocked=1,
            executed=2,
        )
    )

    assert snapshot.accepted == 3
    assert snapshot.blocked == 1
    assert snapshot.executed == 2


def test_system_health_is_preserved() -> None:
    publisher = BrainSnapshotPublisher(
        event_bus=EventBus(),
    )

    snapshot = publisher.publish(
        report(
            system_health=SystemHealth.DEGRADED,
        )
    )

    assert snapshot.system_health is SystemHealth.DEGRADED
    assert not snapshot.successful


def test_multiple_publishes_emit_multiple_snapshots() -> None:
    event_bus = EventBus()
    received = []

    event_bus.subscribe(
        "brain.snapshot",
        received.append,
    )

    publisher = BrainSnapshotPublisher(
        event_bus=event_bus,
    )

    publisher.publish(
        report(sequence=1)
    )
    publisher.publish(
        report(sequence=2)
    )

    assert len(received) == 2
    assert received[0].cycle_sequence == 1
    assert received[1].cycle_sequence == 2