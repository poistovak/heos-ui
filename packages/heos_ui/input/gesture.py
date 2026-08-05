from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GestureType(Enum):
    TAP = "tap"
    DOUBLE_TAP = "double_tap"
    LONG_PRESS = "long_press"
    DRAG = "drag"
    SWIPE = "swipe"


@dataclass(slots=True, frozen=True)
class Gesture:
    gesture_type: GestureType
    target: str


class GestureEngine:
    """Recognizes and dispatches gestures."""

    def recognize(
        self,
        gesture: Gesture,
    ) -> Gesture:
        return gesture

    def is_touch(
        self,
        gesture: Gesture,
    ) -> bool:
        return gesture.gesture_type in {
            GestureType.TAP,
            GestureType.DOUBLE_TAP,
            GestureType.LONG_PRESS,
        }

    def is_motion(
        self,
        gesture: Gesture,
    ) -> bool:
        return gesture.gesture_type in {
            GestureType.DRAG,
            GestureType.SWIPE,
        }