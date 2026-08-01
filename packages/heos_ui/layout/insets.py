from __future__ import annotations

from dataclasses import dataclass

from .arrange import Rect


@dataclass(frozen=True, slots=True)
class EdgeInsets:
    """Immutable padding or margin definition."""

    left: float = 0.0
    top: float = 0.0
    right: float = 0.0
    bottom: float = 0.0

    @classmethod
    def all(cls, value: float) -> "EdgeInsets":
        return cls(value, value, value, value)

    @classmethod
    def symmetric(
        cls,
        *,
        horizontal: float = 0.0,
        vertical: float = 0.0,
    ) -> "EdgeInsets":
        return cls(
            left=horizontal,
            right=horizontal,
            top=vertical,
            bottom=vertical,
        )

    @property
    def horizontal(self) -> float:
        return self.left + self.right

    @property
    def vertical(self) -> float:
        return self.top + self.bottom

    def deflate(self, rect: Rect) -> Rect:
        """Return the inner rectangle."""

        return Rect(
            x=rect.x + self.left,
            y=rect.y + self.top,
            width=max(0.0, rect.width - self.horizontal),
            height=max(0.0, rect.height - self.vertical),
        )

    def inflate(self, rect: Rect) -> Rect:
        """Return the outer rectangle."""

        return Rect(
            x=rect.x - self.left,
            y=rect.y - self.top,
            width=rect.width + self.horizontal,
            height=rect.height + self.vertical,
        )