from __future__ import annotations

from dataclasses import dataclass

from .animation import Animation


@dataclass(slots=True)
class Transition:
    """Animated transition between two values."""

    animation: Animation
    progress: float = 0.0

    @property
    def finished(self) -> bool:
        return self.progress >= 1.0

    def value(self) -> float:
        return self.animation.value(self.progress)

    def advance(self, delta: float) -> None:
        self.progress = min(
            1.0,
            max(
                0.0,
                self.progress + delta,
            ),
        )


class TransitionEngine:
    """Runs transitions."""

    def step(
        self,
        transition: Transition,
        delta: float,
    ) -> float:
        transition.advance(delta)
        return transition.value()