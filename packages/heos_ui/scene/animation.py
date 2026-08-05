from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Animation:
    """Linear animation."""

    start: float
    end: float
    duration: float

    def value(self, progress: float) -> float:
        """Return interpolated value."""

        progress = max(0.0, min(1.0, progress))

        return self.start + (
            self.end - self.start
        ) * progress


class AnimationEngine:
    """Runs animations."""

    def animate(
        self,
        animation: Animation,
        progress: float,
    ) -> float:
        return animation.value(progress)