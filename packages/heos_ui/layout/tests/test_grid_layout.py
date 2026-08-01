import pytest
from heos_ui.layout.arrange import Rect
from heos_ui.layout.constraints import Size
from heos_ui.layout.grid import GridLayout


def test_grid_arranges_children_in_rows() -> None:
    layout = GridLayout(columns=2)

    result = layout.arrange(
        (
            Size(100.0, 40.0),
            Size(120.0, 50.0),
            Size(80.0, 30.0),
            Size(90.0, 60.0),
        )
    )

    assert result == (
        Rect(0.0, 0.0, 100.0, 40.0),
        Rect(100.0, 0.0, 120.0, 50.0),
        Rect(0.0, 50.0, 80.0, 30.0),
        Rect(100.0, 50.0, 90.0, 60.0),
    )


def test_grid_uses_largest_column_width() -> None:
    layout = GridLayout(columns=2)

    result = layout.arrange(
        (
            Size(100.0, 40.0),
            Size(80.0, 40.0),
            Size(150.0, 40.0),
            Size(90.0, 40.0),
        )
    )

    assert result[1].x == 150.0
    assert result[3].x == 150.0


def test_grid_applies_spacing_and_origin() -> None:
    layout = GridLayout(
        columns=2,
        column_spacing=10.0,
        row_spacing=8.0,
    )

    result = layout.arrange(
        (
            Size(100.0, 40.0),
            Size(120.0, 50.0),
            Size(80.0, 30.0),
        ),
        x=20.0,
        y=30.0,
    )

    assert result == (
        Rect(20.0, 30.0, 100.0, 40.0),
        Rect(130.0, 30.0, 120.0, 50.0),
        Rect(20.0, 88.0, 80.0, 30.0),
    )


def test_grid_measurement() -> None:
    layout = GridLayout(
        columns=2,
        column_spacing=10.0,
        row_spacing=8.0,
    )

    assert layout.measure(
        (
            Size(100.0, 40.0),
            Size(120.0, 50.0),
            Size(150.0, 30.0),
            Size(90.0, 60.0),
        )
    ) == Size(
        width=280.0,
        height=118.0,
    )


def test_incomplete_final_row() -> None:
    layout = GridLayout(columns=3)

    result = layout.arrange(
        (
            Size(40.0, 20.0),
            Size(50.0, 30.0),
            Size(60.0, 40.0),
            Size(70.0, 50.0),
        )
    )

    assert result[3] == Rect(
        0.0,
        40.0,
        70.0,
        50.0,
    )


def test_empty_grid() -> None:
    layout = GridLayout(columns=2)

    assert layout.arrange(()) == ()
    assert layout.measure(()) == Size(0.0, 0.0)


def test_invalid_grid_configuration_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Grid columns must be greater than zero.",
    ):
        GridLayout(columns=0)

    with pytest.raises(
        ValueError,
        match="Grid column spacing cannot be negative.",
    ):
        GridLayout(columns=2, column_spacing=-1.0)

    with pytest.raises(
        ValueError,
        match="Grid row spacing cannot be negative.",
    ):
        GridLayout(columns=2, row_spacing=-1.0)
