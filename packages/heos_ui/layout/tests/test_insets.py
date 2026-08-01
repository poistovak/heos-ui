from heos_ui.layout.arrange import Rect
from heos_ui.layout.insets import EdgeInsets


def test_all() -> None:
    padding = EdgeInsets.all(10.0)

    assert padding.left == 10.0
    assert padding.right == 10.0
    assert padding.top == 10.0
    assert padding.bottom == 10.0


def test_symmetric() -> None:
    padding = EdgeInsets.symmetric(
        horizontal=12.0,
        vertical=8.0,
    )

    assert padding.horizontal == 24.0
    assert padding.vertical == 16.0


def test_deflate() -> None:
    rect = Rect(0.0, 0.0, 300.0, 200.0)

    result = EdgeInsets.all(10.0).deflate(rect)

    assert result == Rect(
        10.0,
        10.0,
        280.0,
        180.0,
    )


def test_inflate() -> None:
    rect = Rect(10.0, 10.0, 280.0, 180.0)

    result = EdgeInsets.all(10.0).inflate(rect)

    assert result == Rect(
        0.0,
        0.0,
        300.0,
        200.0,
    )


def test_zero_padding() -> None:
    rect = Rect(5.0, 5.0, 100.0, 50.0)

    assert EdgeInsets().deflate(rect) == rect
    assert EdgeInsets().inflate(rect) == rect


def test_large_padding_never_negative() -> None:
    rect = Rect(0.0, 0.0, 20.0, 20.0)

    result = EdgeInsets.all(50.0).deflate(rect)

    assert result.width == 0.0
    assert result.height == 0.0