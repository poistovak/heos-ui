from heos_ui.layout.alignment import (
    Alignment,
    HorizontalAlignment,
    VerticalAlignment,
)
from heos_ui.layout.arrange import Rect
from heos_ui.layout.constraints import Size

CONTAINER = Rect(
    x=0.0,
    y=0.0,
    width=300.0,
    height=200.0,
)


def test_top_left() -> None:
    rect = Alignment().align(
        CONTAINER,
        Size(100.0, 50.0),
    )

    assert rect == Rect(
        0.0,
        0.0,
        100.0,
        50.0,
    )


def test_center() -> None:
    rect = Alignment(
        HorizontalAlignment.CENTER,
        VerticalAlignment.CENTER,
    ).align(
        CONTAINER,
        Size(100.0, 50.0),
    )

    assert rect == Rect(
        100.0,
        75.0,
        100.0,
        50.0,
    )


def test_bottom_right() -> None:
    rect = Alignment(
        HorizontalAlignment.RIGHT,
        VerticalAlignment.BOTTOM,
    ).align(
        CONTAINER,
        Size(100.0, 50.0),
    )

    assert rect == Rect(
        200.0,
        150.0,
        100.0,
        50.0,
    )


def test_left_center() -> None:
    rect = Alignment(
        HorizontalAlignment.LEFT,
        VerticalAlignment.CENTER,
    ).align(
        CONTAINER,
        Size(100.0, 50.0),
    )

    assert rect.y == 75.0


def test_top_right() -> None:
    rect = Alignment(
        HorizontalAlignment.RIGHT,
        VerticalAlignment.TOP,
    ).align(
        CONTAINER,
        Size(100.0, 50.0),
    )

    assert rect.x == 200.0
    assert rect.y == 0.0


def test_bottom_left() -> None:
    rect = Alignment(
        HorizontalAlignment.LEFT,
        VerticalAlignment.BOTTOM,
    ).align(
        CONTAINER,
        Size(100.0, 50.0),
    )

    assert rect.x == 0.0
    assert rect.y == 150.0