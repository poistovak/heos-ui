from heos_ui.layout import Rect
from heos_ui.scene import CanvasBackend, PaintCommand


def command() -> PaintCommand:
    return PaintCommand(
        "rect",
        Rect(
            0.0,
            0.0,
            100.0,
            50.0,
        ),
    )


def test_canvas_starts_empty() -> None:
    canvas = CanvasBackend()

    assert canvas.command_count == 0


def test_submit_command() -> None:
    canvas = CanvasBackend()

    canvas.submit(command())

    assert canvas.command_count == 1


def test_begin_frame_clears_previous_commands() -> None:
    canvas = CanvasBackend()

    canvas.submit(command())

    canvas.begin_frame()

    assert canvas.command_count == 0


def test_end_frame_returns_commands() -> None:
    canvas = CanvasBackend()

    canvas.submit(command())

    commands = canvas.end_frame()

    assert len(commands) == 1


def test_multiple_commands() -> None:
    canvas = CanvasBackend()

    canvas.submit(command())
    canvas.submit(command())
    canvas.submit(command())

    assert canvas.command_count == 3


def test_end_frame_is_immutable() -> None:
    canvas = CanvasBackend()

    canvas.submit(command())

    assert isinstance(
        canvas.end_frame(),
        tuple,
    )