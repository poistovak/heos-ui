from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FrameClock:
    """Tracks render frames."""

    frame: int = 0

    def tick(self) -> int:
        """Advance to the next frame."""

        self.frame += 1
        return self.frame

    def reset(self) -> None:
        """Reset frame counter."""

        self.frame = 0