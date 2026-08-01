from heos_ui.layout.constraints import LayoutConstraints, Size
from heos_ui.layout.measure import MeasureEngine


def test_measure_unbounded() -> None:
    engine = MeasureEngine(LayoutConstraints())

    assert engine.measure(Size(320, 180)) == Size(320, 180)


def test_measure_respects_minimums() -> None:
    engine = MeasureEngine(
        LayoutConstraints(
            min_width=200,
            min_height=100,
        )
    )

    assert engine.measure(Size(50, 20)) == Size(200, 100)


def test_measure_respects_maximums() -> None:
    engine = MeasureEngine(
        LayoutConstraints(
            max_width=400,
            max_height=300,
        )
    )

    assert engine.measure(Size(800, 600)) == Size(400, 300)


def test_measure_inside_constraints() -> None:
    engine = MeasureEngine(
        LayoutConstraints(
            min_width=100,
            max_width=500,
            min_height=50,
            max_height=300,
        )
    )

    assert engine.measure(Size(250, 120)) == Size(250, 120)


def test_measure_fixed_constraints() -> None:
    constraints = LayoutConstraints().tighten(
        width=300,
        height=120,
    )

    engine = MeasureEngine(constraints)

    assert engine.measure(Size(50, 900)) == Size(300, 120)


def test_measure_zero_size() -> None:
    engine = MeasureEngine(LayoutConstraints())

    assert engine.measure(Size(0, 0)) == Size(0, 0)