from heos_ui.input.gesture import (
    Gesture,
    GestureEngine,
    GestureType,
)


def test_recognize() -> None:
    engine = GestureEngine()

    gesture = Gesture(
        GestureType.TAP,
        "battery",
    )

    assert engine.recognize(gesture) == gesture


def test_touch_gesture() -> None:
    engine = GestureEngine()

    assert engine.is_touch(
        Gesture(
            GestureType.TAP,
            "card",
        )
    )


def test_motion_gesture() -> None:
    engine = GestureEngine()

    assert engine.is_motion(
        Gesture(
            GestureType.DRAG,
            "card",
        )
    )


def test_swipe_is_motion() -> None:
    engine = GestureEngine()

    assert engine.is_motion(
        Gesture(
            GestureType.SWIPE,
            "card",
        )
    )


def test_long_press_is_touch() -> None:
    engine = GestureEngine()

    assert engine.is_touch(
        Gesture(
            GestureType.LONG_PRESS,
            "card",
        )
    )


def test_drag_is_not_touch() -> None:
    engine = GestureEngine()

    assert not engine.is_touch(
        Gesture(
            GestureType.DRAG,
            "card",
        )
    )


def test_tap_is_not_motion() -> None:
    engine = GestureEngine()

    assert not engine.is_motion(
        Gesture(
            GestureType.TAP,
            "card",
        )
    )