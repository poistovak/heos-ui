from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FrameBudget:
    """Frame timing budget."""

    target_ms: float

    def within_budget(self, frame_ms: float) -> bool:
        """Return True when frame fits inside the budget."""

        return frame_ms <= self.target_ms

    def exceeded_by(self, frame_ms: float) -> float:
        """Return exceeded milliseconds."""

        return round(max(0.0, frame_ms - self.target_ms), 2)

    def remaining(self, frame_ms: float) -> float:
        """Return remaining milliseconds."""

        return round(max(0.0, self.target_ms - frame_ms), 2)