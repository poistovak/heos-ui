from heos_ui.scene.animation import (
    Animation,
    AnimationEngine,
)


def test_start_value() -> None:
    animation = Animation(
        0.0,
        100.0,
        1.0,
    )

    assert animation.value(0.0) == 0.0


def test_end_value() -> None:
    animation = Animation(
        0.0,
        100.0,
        1.0,
    )

    assert animation.value(1.0) == 100.0


def test_halfway() -> None:
    animation = Animation(
        0.0,
        100.0,
        1.0,
    )

    assert animation.value(0.5) == 50.0


def test_clamp_low() -> None:
    animation = Animation(
        0.0,
        100.0,
        1.0,
    )

    assert animation.value(-1.0) == 0.0


def test_clamp_high() -> None:
    animation = Animation(
        0.0,
        100.0,
        1.0,
    )

    assert animation.value(2.0) == 100.0


def test_engine() -> None:
    engine = AnimationEngine()

    animation = Animation(
        10.0,
        30.0,
        1.0,
    )

    assert engine.animate(
        animation,
        0.5,
    ) == 20.0