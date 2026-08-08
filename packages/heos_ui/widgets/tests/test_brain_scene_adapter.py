from heos_ui.layout import Rect
from heos_ui.widgets.brain_presenter import BrainStatusSeverity
from heos_ui.widgets.brain_renderer import (
    BrainRenderField,
    BrainRenderScene,
)
from heos_ui.widgets.brain_scene_adapter import (
    BrainSceneAdapter,
    BrainSceneLayout,
)


def scene() -> BrainRenderScene:
    return BrainRenderScene(
        title="HEOS Brain",
        status="RUNNING",
        health="HEALTHY",
        severity=BrainStatusSeverity.NORMAL,
        fields=(
            BrainRenderField(
                label="Cycle",
                value="Cycle 160",
            ),
            BrainRenderField(
                label="Execution",
                value="Execution 100%",
            ),
            BrainRenderField(
                label="Targets",
                value="Targets 5/5 healthy",
            ),
        ),
    )


def layout() -> BrainSceneLayout:
    return BrainSceneLayout(
        bounds=Rect(0, 0, 300, 200),
        title=Rect(16, 16, 268, 24),
        status=Rect(16, 48, 120, 24),
        health=Rect(148, 48, 136, 24),
        cycle=Rect(16, 88, 268, 20),
        execution=Rect(16, 120, 268, 20),
        targets=Rect(16, 152, 268, 20),
    )


def test_adapter_returns_seven_commands() -> None:
    paint = BrainSceneAdapter().adapt(
        scene(),
        layout(),
    )

    assert paint.count == 7


def test_first_command_draws_card_rect() -> None:
    paint = BrainSceneAdapter().adapt(
        scene(),
        layout(),
    )

    first = paint.commands[0]

    assert first.command == "rect"
    assert first.rect == layout().bounds


def test_title_is_text_command() -> None:
    paint = BrainSceneAdapter().adapt(
        scene(),
        layout(),
    )

    command = paint.commands[1]

    assert command.command == "text"
    assert command.rect == layout().title


def test_status_is_text_command() -> None:
    paint = BrainSceneAdapter().adapt(
        scene(),
        layout(),
    )

    command = paint.commands[2]

    assert command.command == "text"
    assert command.rect == layout().status


def test_health_is_text_command() -> None:
    paint = BrainSceneAdapter().adapt(
        scene(),
        layout(),
    )

    command = paint.commands[3]

    assert command.command == "text"
    assert command.rect == layout().health


def test_cycle_is_text_command() -> None:
    paint = BrainSceneAdapter().adapt(
        scene(),
        layout(),
    )

    assert paint.commands[4].rect == layout().cycle


def test_execution_is_text_command() -> None:
    paint = BrainSceneAdapter().adapt(
        scene(),
        layout(),
    )

    assert paint.commands[5].rect == layout().execution


def test_targets_are_text_command() -> None:
    paint = BrainSceneAdapter().adapt(
        scene(),
        layout(),
    )

    assert paint.commands[6].rect == layout().targets