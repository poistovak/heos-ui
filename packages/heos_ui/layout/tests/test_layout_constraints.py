import pytest
from heos_ui.layout.constraints import LayoutConstraints, Size


def test_unbounded_constraints_preserve_size() -> None:
    constraints = LayoutConstraints()

    assert constraints.constrain(Size(320.0, 180.0)) == Size(
        width=320.0,
        height=180.0,
    )


def test_size_is_clamped_to_minimums() -> None:
    constraints = LayoutConstraints(
        min_width=100.0,
        min_height=80.0,
    )

    assert constraints.constrain(Size(20.0, 30.0)) == Size(
        width=100.0,
        height=80.0,
    )


def test_size_is_clamped_to_maximums() -> None:
    constraints = LayoutConstraints(
        max_width=500.0,
        max_height=300.0,
    )

    assert constraints.constrain(Size(800.0, 600.0)) == Size(
        width=500.0,
        height=300.0,
    )


def test_loosen_removes_minimums() -> None:
    constraints = LayoutConstraints(
        min_width=100.0,
        max_width=500.0,
        min_height=80.0,
        max_height=300.0,
    )

    assert constraints.loosen() == LayoutConstraints(
        max_width=500.0,
        max_height=300.0,
    )


def test_tighten_creates_fixed_dimensions() -> None:
    constraints = LayoutConstraints(
        max_width=500.0,
        max_height=300.0,
    )

    assert constraints.tighten(
        width=240.0,
        height=120.0,
    ) == LayoutConstraints(
        min_width=240.0,
        max_width=240.0,
        min_height=120.0,
        max_height=120.0,
    )


def test_invalid_constraints_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Maximum width cannot be smaller than minimum width.",
    ):
        LayoutConstraints(
            min_width=200.0,
            max_width=100.0,
        )
