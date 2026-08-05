from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class FlowAnimation:
    source: str
    destination: str
    progress: float


class AnimationEngine:
    def advance(
        self,
        animation: FlowAnimation,
        delta: float,
    ) -> FlowAnimation:
        progress = min(
            1.0,
            max(
                0.0,
                animation.progress + delta,
            ),
        )

        return FlowAnimation(
            source=animation.source,
            destination=animation.destination,
            progress=progress,
        )