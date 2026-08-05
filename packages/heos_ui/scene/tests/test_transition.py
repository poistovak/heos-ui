from heos_ui.scene.animation import Animation
from heos_ui.scene.transition import (
    Transition,
    TransitionEngine,
)


def animation() -> Animation:
    return Animation(
        0.0,
        100.0,
        1.0,
    )


def test_initial_value() -> None:
    transition = Transition(animation())

    assert transition.value() == 0.0


def test_advance() -> None:
    transition = Transition(animation())

    transition.advance(0.5)

    assert transition.value() == 50.0


def test_finish() -> None:
    transition = Transition(animation())

    transition.advance(1.5)

    assert transition.finished
    assert transition.value() == 100.0


def test_engine_step() -> None:
    engine = TransitionEngine()

    transition = Transition(animation())

    value = engine.step(
        transition,
        0.25,
    )

    assert value == 25.0


def test_engine_repeatable() -> None:
    engine = TransitionEngine()

    transition = Transition(animation())

    engine.step(transition, 0.25)
    engine.step(transition, 0.25)

    assert transition.value() == 50.0


def test_progress_never_negative() -> None:
    transition = Transition(animation())

    transition.advance(-1.0)

    assert transition.progress == 0.0