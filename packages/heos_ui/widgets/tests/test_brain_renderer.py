from heos_ui.widgets.brain_presenter import (
    BrainStatusPresentation,
    BrainStatusSeverity,
)
from heos_ui.widgets.brain_renderer import (
    BrainRenderScene,
    BrainStatusRenderer,
)


def presentation(
    *,
    title: str = "HEOS Brain",
    status: str = "RUNNING",
    health: str = "HEALTHY",
    cycle: str = "Cycle 158",
    execution: str = "Execution 100%",
    targets: str = "Targets 5/5 healthy",
    severity: BrainStatusSeverity = BrainStatusSeverity.NORMAL,
) -> BrainStatusPresentation:
    return BrainStatusPresentation(
        title=title,
        status=status,
        health=health,
        cycle=cycle,
        execution=execution,
        targets=targets,
        severity=severity,
    )


def test_renderer_returns_scene() -> None:
    scene = BrainStatusRenderer().render(
        presentation()
    )

    assert isinstance(scene, BrainRenderScene)


def test_renderer_preserves_title() -> None:
    scene = BrainStatusRenderer().render(
        presentation(
            title="HEOS Brain",
        )
    )

    assert scene.title == "HEOS Brain"


def test_renderer_preserves_status_and_health() -> None:
    scene = BrainStatusRenderer().render(
        presentation()
    )

    assert scene.status == "RUNNING"
    assert scene.health == "HEALTHY"


def test_renderer_preserves_severity() -> None:
    scene = BrainStatusRenderer().render(
        presentation(
            status="ATTENTION",
            health="DEGRADED",
            severity=BrainStatusSeverity.WARNING,
        )
    )

    assert scene.severity is BrainStatusSeverity.WARNING


def test_renderer_creates_cycle_field() -> None:
    scene = BrainStatusRenderer().render(
        presentation(
            cycle="Cycle 159",
        )
    )

    assert scene.fields[0].label == "Cycle"
    assert scene.fields[0].value == "Cycle 159"


def test_renderer_creates_execution_field() -> None:
    scene = BrainStatusRenderer().render(
        presentation(
            execution="Execution 75%",
        )
    )

    assert scene.fields[1].label == "Execution"
    assert scene.fields[1].value == "Execution 75%"


def test_renderer_creates_targets_field() -> None:
    scene = BrainStatusRenderer().render(
        presentation(
            targets="Targets 4/5 healthy",
        )
    )

    assert scene.fields[2].label == "Targets"
    assert scene.fields[2].value == "Targets 4/5 healthy"


def test_renderer_creates_three_fields() -> None:
    scene = BrainStatusRenderer().render(
        presentation()
    )

    assert len(scene.fields) == 3