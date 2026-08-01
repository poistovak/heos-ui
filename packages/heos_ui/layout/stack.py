from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .arrange import ArrangeEngine, Rect
from .constraints import Size


class StackDirection(StrEnum):
    """Direction in which children are arranged."""

    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclass(frozen=True, slots=True)
class StackLayout:
    """Arranges child sizes sequentially with optional spacing."""

    direction: StackDirection = StackDirection.VERTICAL
    spacing: float = 0.0

    def __post_init__(self) -> None:
        if self.spacing < 0.0:
            raise ValueError("Stack spacing cannot be negative.")

    def arrange(
        self,
        sizes: tuple[Size, ...],
        *,
        x: float = 0.0,
        y: float = 0.0,
    ) -> tuple[Rect, ...]:
        engine = ArrangeEngine()
        rectangles: list[Rect] = []
        current_x = x
        current_y = y

        for size in sizes:
            rectangles.append(
                engine.arrange(
                    current_x,
                    current_y,
                    size,
                )
            )

            if self.direction is StackDirection.HORIZONTAL:
                current_x += size.width + self.spacing
            else:
                current_y += size.height + self.spacing

        return tuple(rectangles)

    def measure(self, sizes: tuple[Size, ...]) -> Size:
        """Return the total size required by all children."""

        if not sizes:
            return Size(0.0, 0.0)

        gaps = self.spacing * (len(sizes) - 1)

        if self.direction is StackDirection.HORIZONTAL:
            return Size(
                width=sum(size.width for size in sizes) + gaps,
                height=max(size.height for size in sizes),
            )

        return Size(
            width=max(size.width for size in sizes),
            height=sum(size.height for size in sizes) + gaps,
        )
