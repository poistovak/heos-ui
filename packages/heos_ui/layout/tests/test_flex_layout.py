from heos_ui.layout.arrange import Rect
from heos_ui.layout.constraints import Size
from heos_ui.layout.flex import (
    FlexDirection,
    FlexItem,
    FlexLayout,
)


def test_equal_row_distribution() -> None:
    layout = FlexLayout()

    result = layout.arrange(
        (
            FlexItem(Size(0.0, 0.0)),
            FlexItem(Size(0.0, 0.0)),
        ),
        Size(400.0, 100.0),
    )

    assert result == (
        Rect(0.0, 0.0, 200.0, 100.0),
        Rect(200.0, 0.0, 200.0, 100.0),
    )


def test_weighted_distribution() -> None:
    layout = FlexLayout()

    result = layout.arrange(
        (
            FlexItem(Size(0.0, 0.0), flex=1),
            FlexItem(Size(0.0, 0.0), flex=3),
        ),
        Size(400.0, 80.0),
    )

    assert result[0].width == 100.0
    assert result[1].width == 300.0


def test_column_distribution() -> None:
    layout = FlexLayout(
        direction=FlexDirection.COLUMN,
    )

    result = layout.arrange(
        (
            FlexItem(Size(0.0, 0.0)),
            FlexItem(Size(0.0, 0.0)),
        ),
        Size(120.0, 300.0),
    )

    assert result == (
        Rect(0.0, 0.0, 120.0, 150.0),
        Rect(0.0, 150.0, 120.0, 150.0),
    )


def test_spacing() -> None:
    layout = FlexLayout(spacing=20.0)

    result = layout.arrange(
        (
            FlexItem(Size(0.0, 0.0)),
            FlexItem(Size(0.0, 0.0)),
        ),
        Size(420.0, 100.0),
    )

    assert result[0].width == 200.0
    assert result[1].x == 220.0


def test_empty_layout() -> None:
    assert FlexLayout().arrange(
        (),
        Size(100.0, 100.0),
    ) == ()


def test_three_items() -> None:
    layout = FlexLayout()

    result = layout.arrange(
        (
            FlexItem(Size(0.0, 0.0), 1),
            FlexItem(Size(0.0, 0.0), 1),
            FlexItem(Size(0.0, 0.0), 2),
        ),
        Size(400.0, 100.0),
    )

    assert result[2].width == 200.0