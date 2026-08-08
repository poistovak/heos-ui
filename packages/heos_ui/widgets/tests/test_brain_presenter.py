from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.decision.brain_view import BrainViewModel
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.brain_presenter import (
    BrainStatusPresenter,
    BrainStatusSeverity,
)
from heos_ui.widgets.brain_status import BrainStatusWidget


def widget() -> BrainStatusWidget:
    return BrainStatusWidget(
        id="brain-status",
        title="HEOS Brain",
    )


def update_widget(
    brain: BrainStatusWidget,
    *,
    cycle: int = 158,
    health: SystemHealth = SystemHealth.HEALTHY,
    accepted: int = 4,
    blocked: int = 0,
    executed: int = 4,
    healthy_targets: int = 5,
    unhealthy_targets: int = 0,
    successful: bool = True,
) -> None:
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

    brain.update(
        BrainViewModel.from_snapshot(snapshot)
    )


def test_empty_widget_has_unknown_presentation() -> None:
    presentation = BrainStatusPresenter().present(
        widget()
    )

    assert presentation.status == "UNKNOWN"
    assert presentation.health == "UNKNOWN"
    assert presentation.severity is BrainStatusSeverity.UNKNOWN


def test_title_is_preserved() -> None:
    brain = widget()
    update_widget(brain)

    presentation = BrainStatusPresenter().present(brain)

    assert presentation.title == "HEOS Brain"


def test_running_brain_has_normal_severity() -> None:
    brain = widget()
    update_widget(brain)

    presentation = BrainStatusPresenter().present(brain)

    assert presentation.status == "RUNNING"
    assert presentation.severity is BrainStatusSeverity.NORMAL


def test_attention_brain_has_warning_severity() -> None:
    brain = widget()
    update_widget(
        brain,
        health=SystemHealth.DEGRADED,
        successful=False,
    )

    presentation = BrainStatusPresenter().present(brain)

    assert presentation.status == "ATTENTION"
    assert presentation.health == "DEGRADED"
    assert presentation.severity is BrainStatusSeverity.WARNING


def test_cycle_is_render_ready() -> None:
    brain = widget()
    update_widget(
        brain,
        cycle=158,
    )

    presentation = BrainStatusPresenter().present(brain)

    assert presentation.cycle == "Cycle 158"


def test_execution_is_render_ready() -> None:
    brain = widget()
    update_widget(
        brain,
        accepted=4,
        executed=3,
    )

    presentation = BrainStatusPresenter().present(brain)

    assert presentation.execution == "Execution 75%"


def test_targets_are_render_ready() -> None:
    brain = widget()
    update_widget(
        brain,
        healthy_targets=4,
        unhealthy_targets=1,
    )

    presentation = BrainStatusPresenter().present(brain)

    assert presentation.targets == "Targets 4/5 healthy"


def test_empty_widget_uses_placeholders() -> None:
    presentation = BrainStatusPresenter().present(
        widget()
    )

    assert presentation.cycle == "Cycle —"
    assert presentation.execution == "Execution —"
    assert presentation.targets == "Targets —"