import pytest
from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.events.bus import EventBus
from heos_ui.widgets.brain_runtime_events import (
    BrainRuntimeEvents,
    BrainRuntimeEventType,
)
from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_runtime_lifecycle import (
    BrainRuntimeLifecycle,
    BrainRuntimeLifecycleState,
)
from heos_ui.widgets.brain_runtime_session import BrainRuntimeSession


def snapshot(
    *,
    cycle: int = 173,
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


def runtime_events(
    *,
    event_bus: EventBus | None = None,
) -> BrainRuntimeEvents:
    runtime = BrainRuntimeLifecycle(
        session=BrainRuntimeSession(
            runtime=BrainRuntimeFactory.create(),
        )
    )

    return BrainRuntimeEvents(
        runtime=runtime,
        event_bus=event_bus or EventBus(),
    )


def test_start_emits_started_event() -> None:
    events = runtime_events()

    event = events.start()

    assert event.event_type is BrainRuntimeEventType.STARTED
    assert event.state is BrainRuntimeLifecycleState.STARTED


def test_started_event_has_no_cycle() -> None:
    events = runtime_events()

    event = events.start()

    assert event.cycle is None


def test_publish_emits_snapshot_event() -> None:
    events = runtime_events()

    events.start()

    event = events.publish(
        snapshot()
    )

    assert (
        event.event_type
        is BrainRuntimeEventType.SNAPSHOT_PUBLISHED
    )
    assert event.state is BrainRuntimeLifecycleState.RUNNING
    assert event.cycle == 173


def test_render_emits_frame_event() -> None:
    events = runtime_events()

    events.start()
    events.publish(snapshot())

    frame, event = events.render()

    assert len(frame) == 7
    assert (
        event.event_type
        is BrainRuntimeEventType.FRAME_RENDERED
    )
    assert event.cycle == 173


def test_stop_emits_stopped_event() -> None:
    events = runtime_events()

    events.start()
    events.publish(snapshot())

    event = events.stop()

    assert event.event_type is BrainRuntimeEventType.STOPPED
    assert event.state is BrainRuntimeLifecycleState.STOPPED
    assert event.cycle == 173


def test_events_are_published_to_event_bus() -> None:
    event_bus = EventBus()
    received = []

    event_bus.subscribe(
        "brain.runtime",
        received.append,
    )

    events = runtime_events(
        event_bus=event_bus,
    )

    events.start()
    events.publish(snapshot())
    events.render()
    events.stop()

    assert len(received) == 4


def test_event_order_matches_runtime_flow() -> None:
    event_bus = EventBus()
    received = []

    event_bus.subscribe(
        "brain.runtime",
        received.append,
    )

    events = runtime_events(
        event_bus=event_bus,
    )

    events.start()
    events.publish(snapshot())
    events.render()
    events.stop()

    assert tuple(
        event.event_type
        for event in received
    ) == (
        BrainRuntimeEventType.STARTED,
        BrainRuntimeEventType.SNAPSHOT_PUBLISHED,
        BrainRuntimeEventType.FRAME_RENDERED,
        BrainRuntimeEventType.STOPPED,
    )


def test_custom_topic_is_supported() -> None:
    event_bus = EventBus()
    received = []

    event_bus.subscribe(
        "heos.runtime",
        received.append,
    )

    events = runtime_events(
        event_bus=event_bus,
    )
    events.topic = "heos.runtime"

    events.start()

    assert len(received) == 1
    assert received[0].event_type is BrainRuntimeEventType.STARTED


def test_publish_tracks_latest_cycle() -> None:
    events = runtime_events()

    events.start()

    first = events.publish(
        snapshot(cycle=1)
    )
    second = events.publish(
        snapshot(cycle=173)
    )

    assert first.cycle == 1
    assert second.cycle == 173


def test_invalid_runtime_transition_emits_no_event() -> None:
    event_bus = EventBus()
    received = []

    event_bus.subscribe(
        "brain.runtime",
        received.append,
    )

    events = runtime_events(
        event_bus=event_bus,
    )

    with pytest.raises(RuntimeError):
        events.publish(snapshot())

    assert received == []


def test_render_event_keeps_runtime_running() -> None:
    events = runtime_events()

    events.start()
    events.publish(snapshot())

    _, event = events.render()

    assert event.state is BrainRuntimeLifecycleState.RUNNING
    assert events.runtime.running
