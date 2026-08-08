from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.decision.brain_store import BrainSnapshotStore
from heos_ui.diagnostics import SystemHealth
from heos_ui.events.bus import EventBus


def snapshot(
    sequence: int = 1,
) -> BrainRuntimeSnapshot:
    return BrainRuntimeSnapshot(
        cycle_sequence=sequence,
        system_health=SystemHealth.HEALTHY,
        accepted=1,
        blocked=0,
        executed=1,
        healthy_targets=2,
        unhealthy_targets=0,
        successful=True,
    )


def test_store_starts_empty() -> None:
    store = BrainSnapshotStore(
        event_bus=EventBus(),
    )

    assert not store.has_snapshot
    assert store.latest() is None


def test_update_stores_snapshot() -> None:
    store = BrainSnapshotStore(
        event_bus=EventBus(),
    )

    item = snapshot()

    store.update(item)

    assert store.has_snapshot
    assert store.latest() == item


def test_event_updates_store() -> None:
    event_bus = EventBus()
    store = BrainSnapshotStore(
        event_bus=event_bus,
    )

    item = snapshot()

    event_bus.publish(
        "brain.snapshot",
        item,
    )

    assert store.latest() == item


def test_new_snapshot_replaces_previous() -> None:
    event_bus = EventBus()
    store = BrainSnapshotStore(
        event_bus=event_bus,
    )

    event_bus.publish(
        "brain.snapshot",
        snapshot(sequence=1),
    )
    event_bus.publish(
        "brain.snapshot",
        snapshot(sequence=2),
    )

    assert store.latest() is not None
    assert store.latest().cycle_sequence == 2


def test_custom_topic() -> None:
    event_bus = EventBus()

    store = BrainSnapshotStore(
        event_bus=event_bus,
        topic="heos.brain.snapshot",
    )

    item = snapshot(sequence=7)

    event_bus.publish(
        "heos.brain.snapshot",
        item,
    )

    assert store.latest() == item


def test_clear_removes_latest_snapshot() -> None:
    store = BrainSnapshotStore(
        event_bus=EventBus(),
    )

    store.update(snapshot())

    assert store.has_snapshot

    store.clear()

    assert not store.has_snapshot
    assert store.latest() is None