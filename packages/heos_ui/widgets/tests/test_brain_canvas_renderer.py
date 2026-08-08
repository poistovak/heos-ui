from heos_ui.layout import Rect
from heos_ui.scene.canvas import CanvasBackend
from heos_ui.scene.paint import PaintCommand, PaintList
from heos_ui.widgets.brain_canvas_renderer import BrainCanvasRenderer


def command(
    kind: str = "text",
    *,
    x: int = 0,
) -> PaintCommand:
    return PaintCommand(
        command=kind,
        rect=Rect(x, 0, 100, 20),
    )


def test_empty_paint_list_renders_empty_frame() -> None:
    renderer = BrainCanvasRenderer(
        canvas=CanvasBackend(),
    )

    result = renderer.render(PaintList())

    assert result == ()


def test_single_command_is_submitted() -> None:
    canvas = CanvasBackend()
    renderer = BrainCanvasRenderer(canvas=canvas)

    paint = PaintList()
    item = command()

    paint.add(item)

    result = renderer.render(paint)

    assert result == (item,)


def test_multiple_commands_preserve_order() -> None:
    renderer = BrainCanvasRenderer(
        canvas=CanvasBackend(),
    )

    paint = PaintList()

    first = command("rect", x=0)
    second = command("text", x=10)
    third = command("text", x=20)

    paint.add(first)
    paint.add(second)
    paint.add(third)

    result = renderer.render(paint)

    assert result == (
        first,
        second,
        third,
    )


def test_canvas_contains_rendered_commands() -> None:
    canvas = CanvasBackend()
    renderer = BrainCanvasRenderer(canvas=canvas)

    paint = PaintList()
    paint.add(command())
    paint.add(command(x=10))

    renderer.render(paint)

    assert canvas.command_count == 2


def test_new_frame_clears_previous_commands() -> None:
    canvas = CanvasBackend()
    renderer = BrainCanvasRenderer(canvas=canvas)

    first_paint = PaintList()
    first_paint.add(command())
    first_paint.add(command(x=10))

    renderer.render(first_paint)

    second_paint = PaintList()
    latest = command(x=20)
    second_paint.add(latest)

    result = renderer.render(second_paint)

    assert result == (latest,)
    assert canvas.command_count == 1


def test_render_returns_tuple() -> None:
    renderer = BrainCanvasRenderer(
        canvas=CanvasBackend(),
    )

    paint = PaintList()
    paint.add(command())

    result = renderer.render(paint)

    assert isinstance(result, tuple)


def test_rect_and_text_commands_are_supported() -> None:
    renderer = BrainCanvasRenderer(
        canvas=CanvasBackend(),
    )

    paint = PaintList()
    rect = command("rect")
    text = command("text", x=10)

    paint.add(rect)
    paint.add(text)

    result = renderer.render(paint)

    assert result[0].command == "rect"
    assert result[1].command == "text"
