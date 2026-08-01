from heos_ui.layout import Rect
from heos_ui.scene.dirty import DirtyRegionEngine


def rect(
    x: float = 0.0,
    y: float = 0.0,
    w: float = 100.0,
    h: float = 100.0,
) -> Rect:
    return Rect(
        x=x,
        y=y,
        width=w,
        height=h,
    )


def test_starts_empty() -> None:
    engine = DirtyRegionEngine()

    assert engine.empty
    assert engine.count == 0


def test_mark_region() -> None:
    engine = DirtyRegionEngine()

    engine.mark(rect())

    assert engine.count == 1


def test_clear_regions() -> None:
    engine = DirtyRegionEngine()

    engine.mark(rect())
    engine.clear()

    assert engine.empty


def test_union_single() -> None:
    engine = DirtyRegionEngine()

    engine.mark(rect())

    assert engine.union() == rect()


def test_union_multiple() -> None:
    engine = DirtyRegionEngine()

    engine.mark(rect(0, 0, 100, 100))
    engine.mark(rect(100, 50, 50, 50))

    assert engine.union() == Rect(
        0.0,
        0.0,
        150.0,
        100.0,
    )


def test_regions_are_immutable() -> None:
    engine = DirtyRegionEngine()

    engine.mark(rect())

    assert isinstance(
        engine.regions,
        tuple,
    )