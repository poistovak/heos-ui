from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.decision.brain_view import BrainViewModel
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.brain_status import BrainStatusWidget


def view(
    *,
    cycle: int = 155,
    health: SystemHealth = SystemHealth.HEALTHY,
    accepted: int = 4,
    blocked: int = 0,
    executed: int = 4,
    healthy_targets: int = 5,
    unhealthy_targets: int = 0,
    successful: bool = True,
) -> BrainViewModel:
    snapshot = BrainRuntimeSnapshot(
        cycle_sequence=cycle,
        system_health=health,
        accepted=accepted,
        blocked=blocked,
        executed=executed,
        healthy_targets=healthy_targets,
        unhealthy_targets=unhealthy_targets,
        successful=successful,
    )

    return BrainViewModel.from_snapshot(snapshot)


def widget() -> BrainStatusWidget:
    return BrainStatusWidget(
        id="brain-status",
        title="HEOS Brain",
    )


def test_widget_starts_without_data() -> None:
    brain = widget()

    assert not brain.has_data
    assert brain.status == "UNKNOWN"
    assert brain.health == "UNKNOWN"


def test_widget_accepts_view_model() -> None:
    brain = widget()

    brain.update(view())

    assert brain.has_data
    assert brain.view is not None


def test_widget_exposes_running_status() -> None:
    brain = widget()

    brain.update(view())

    assert brain.status == "RUNNING"
    assert brain.health == "HEALTHY"


def test_widget_exposes_attention_status() -> None:
    brain = widget()

    brain.update(
        view(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert brain.status == "ATTENTION"
    assert brain.health == "DEGRADED"


def test_widget_exposes_cycle() -> None:
    brain = widget()

    brain.update(
        view(cycle=156)
    )

    assert brain.cycle == 156


def test_widget_exposes_execution_percent() -> None:
    brain = widget()

    brain.update(
        view(
            accepted=4,
            executed=3,
        )
    )

    assert brain.execution_percent == 75


def test_widget_exposes_target_summary() -> None:
    brain = widget()

    brain.update(
        view(
            healthy_targets=4,
            unhealthy_targets=1,
        )
    )

    assert brain.target_summary == "4/5 healthy"


def test_widget_replaces_previous_view() -> None:
    brain = widget()

    brain.update(
        view(cycle=1)
    )
    brain.update(
        view(cycle=2)
    )

    assert brain.cycle == 2