import pytest
from heos_ui.layout.arrange import Rect
from heos_ui.layout.constraints import Size
from heos_ui.layout.stack import StackDirection, StackLayout


def test_vertical_stack_arranges_children() -> None:
    layout = StackLayout()

    result = layout.arrange(
        (
            Size(100.0, 40.0),
            Size(120.0, 50.0),
            Size(80.0, 30.0),
        )
    )

    assert result == (
        Rect(0.0, 0.0, 100.0, 40.0),
        Rect(0.0, 40.0, 120.0, 50.0),
        Rect(0.0, 90.0, 80.0, 30.0),
    )


def test_vertical_stack_applies_spacing() -> None:
    layout = StackLayout(spacing=10.0)

    result = layout.arrange(
        (
            Size(100.0, 40.0),
            Size(100.0, 50.0),
        )
    )

    assert result == (
        Rect(0.0, 0.0, 100.0, 40.0),
        Rect(0.0, 50.0, 100.0, 50.0),
    )


def test_horizontal_stack_arranges_children() -> None:
    layout = StackLayout(
        direction=StackDirection.HORIZONTAL,
        spacing=8.0,
    )

    result = layout.arrange(
        (
            Size(100.0, 40.0),
            Size(120.0, 60.0),
        ),
        x=20.0,
        y=30.0,
    )

    assert result == (
        Rect(20.0, 30.0, 100.0, 40.0),
        Rect(128.0, 30.0, 120.0, 60.0),
    )


def test_vertical_stack_measurement() -> None:
    layout = StackLayout(spacing=5.0)

    assert layout.measure(
        (
            Size(100.0, 40.0),
            Size(120.0, 50.0),
            Size(80.0, 30.0),
        )
    ) == Size(
        width=120.0,
        height=130.0,
    )


def test_horizontal_stack_measurement() -> None:
    layout = StackLayout(
        direction=StackDirection.HORIZONTAL,
        spacing=5.0,
    )

    assert layout.measure(
        (
            Size(100.0, 40.0),
            Size(120.0, 60.0),
        )
    ) == Size(
        width=225.0,
        height=60.0,
    )


def test_empty_stack_has_zero_size() -> None:
    layout = StackLayout()

    assert layout.arrange(()) == ()
    assert layout.measure(()) == Size(0.0, 0.0)


def test_negative_spacing_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Stack spacing cannot be negative.",
    ):
        StackLayout(spacing=-1.0)
