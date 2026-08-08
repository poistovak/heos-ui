from heos_ui.binding.brain_status import BrainStatusBinding
from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.events.bus import EventBus
from heos_ui.widgets.brain_status import BrainStatusWidget


def snapshot(
    *,
    cycle: int = 157,
    health: SystemHealth = SystemHealth.HEALTHY,
    accepted: int = 4,
    blocked: int = 0,
    executed: int = 4,
    healthy_targets: int = 5,
    unhealthy_targets: int = 0,
    successful: bool = True,
) -> BrainRuntimeSnapshot:
    return BrainRuntimeSnapshot(
        cycle_sequence=cycle,
        system_health=health,
        accepted=accepted,
        blocked=blocked,
        executed=executed,
        healthy_targets=healthy_targets,
        unhealthy_targets=unhealthy_targets,
        successful=successful,
    )


def widget() -> BrainStatusWidget:
    return BrainStatusWidget(
        id="brain-status",
        title="HEOS Brain",
    )


def test_binding_starts_with_unchanged_widget() -> None:
    brain = widget()

    BrainStatusBinding(
        event_bus=EventBus(),
        widget=brain,
    )

    assert not brain.has_data
    assert brain.status == "UNKNOWN"


def test_snapshot_event_updates_widget() -> None:
    event_bus = EventBus()
    brain = widget()

    BrainStatusBinding(
        event_bus=event_bus,
        widget=brain,
    )

    event_bus.publish(
        "brain.snapshot",
        snapshot(),
    )

    assert brain.has_data
    assert brain.cycle == 157


def test_binding_builds_running_view() -> None:
    event_bus = EventBus()
    brain = widget()

    BrainStatusBinding(
        event_bus=event_bus,
        widget=brain,
    )

    event_bus.publish(
        "brain.snapshot",
        snapshot(),
    )

    assert brain.status == "RUNNING"
    assert brain.health == "HEALTHY"


def test_binding_builds_attention_view() -> None:
    event_bus = EventBus()
    brain = widget()

    BrainStatusBinding(
        event_bus=event_bus,
        widget=brain,
    )

    event_bus.publish(
        "brain.snapshot",
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        ),
    )

    assert brain.status == "ATTENTION"
    assert brain.health == "DEGRADED"


def test_binding_updates_execution_percent() -> None:
    event_bus = EventBus()
    brain = widget()

    BrainStatusBinding(
        event_bus=event_bus,
        widget=brain,
    )

    event_bus.publish(
        "brain.snapshot",
        snapshot(
            accepted=4,
            executed=3,
        ),
    )

    assert brain.execution_percent == 75


def test_binding_updates_target_summary() -> None:
    event_bus = EventBus()
    brain = widget()

    BrainStatusBinding(
        event_bus=event_bus,
        widget=brain,
    )

    event_bus.publish(
        "brain.snapshot",
        snapshot(
            healthy_targets=4,
            unhealthy_targets=1,
        ),
    )

    assert brain.target_summary == "4/5 healthy"


def test_new_snapshot_replaces_widget_state() -> None:
    event_bus = EventBus()
    brain = widget()

    BrainStatusBinding(
        event_bus=event_bus,
        widget=brain,
    )

    event_bus.publish(
        "brain.snapshot",
        snapshot(cycle=1),
    )
    event_bus.publish(
        "brain.snapshot",
        snapshot(cycle=2),
    )

    assert brain.cycle == 2


def test_custom_topic_updates_widget() -> None:
    event_bus = EventBus()
    brain = widget()

    BrainStatusBinding(
        event_bus=event_bus,
        widget=brain,
        topic="heos.brain.snapshot",
    )

    event_bus.publish(
        "brain.snapshot",
        snapshot(cycle=1),
    )

    assert not brain.has_data

    event_bus.publish(
        "heos.brain.snapshot",
        snapshot(cycle=157),
    )

    assert brain.cycle == 157