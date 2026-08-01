from heos_ui.layout import Rect
from heos_ui.scene.paint import (
    PaintCommand,
    PaintList,
)


def rect() -> Rect:
    return Rect(
        0.0,
        0.0,
        100.0,
        50.0,
    )


def test_empty_list() -> None:
    commands = PaintList()

    assert commands.count == 0


def test_add_command() -> None:
    commands = PaintList()

    commands.add(
        PaintCommand(
            "rect",
            rect(),
        )
    )

    assert commands.count == 1


def test_clear() -> None:
    commands = PaintList()

    commands.add(
        PaintCommand(
            "rect",
            rect(),
        )
    )

    commands.clear()

    assert commands.count == 0


def test_iteration() -> None:
    commands = PaintList()

    commands.add(
        PaintCommand(
            "rect",
            rect(),
        )
    )

    assert len(
        list(commands)
    ) == 1


def test_commands_are_immutable() -> None:
    commands = PaintList()

    commands.add(
        PaintCommand(
            "text",
            rect(),
        )
    )

    assert isinstance(
        commands.commands,
        tuple,
    )


def test_multiple_commands() -> None:
    commands = PaintList()

    commands.add(
        PaintCommand(
            "rect",
            rect(),
        )
    )

    commands.add(
        PaintCommand(
            "text",
            rect(),
        )
    )

    commands.add(
        PaintCommand(
            "image",
            rect(),
        )
    )

    assert commands.count == 3