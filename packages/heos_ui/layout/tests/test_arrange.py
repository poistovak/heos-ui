from heos_ui.layout.arrange import ArrangeEngine, Rect
from heos_ui.layout.constraints import Size


def test_origin() -> None:
    engine = ArrangeEngine()

    assert engine.arrange(
        0,
        0,
        Size(100, 50),
    ) == Rect(
        0,
        0,
        100,
        50,
    )


def test_offset() -> None:
    engine = ArrangeEngine()

    assert engine.arrange(
        250,
        120,
        Size(320, 180),
    ) == Rect(
        250,
        120,
        320,
        180,
    )


def test_zero_size() -> None:
    engine = ArrangeEngine()

    assert engine.arrange(
        10,
        20,
        Size(0, 0),
    ) == Rect(
        10,
        20,
        0,
        0,
    )


def test_large_size() -> None:
    engine = ArrangeEngine()

    rect = engine.arrange(
        0,
        0,
        Size(1920, 1080),
    )

    assert rect.width == 1920
    assert rect.height == 1080


def test_negative_position() -> None:
    engine = ArrangeEngine()

    assert engine.arrange(
        -20,
        -10,
        Size(100, 100),
    ) == Rect(
        -20,
        -10,
        100,
        100,
    )


def test_rect_properties() -> None:
    rect = ArrangeEngine().arrange(
        15,
        30,
        Size(200, 80),
    )

    assert rect.x == 15
    assert rect.y == 30
    assert rect.width == 200
    assert rect.height == 80