from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .arrange import Rect
from .constraints import Size


class FlexDirection(StrEnum):
    ROW = "row"
    COLUMN = "column"


@dataclass(frozen=True, slots=True)
class FlexItem:
    size: Size
    flex: int = 1


@dataclass(slots=True)
class FlexLayout:
    """Distributes free space between flex items."""

    direction: FlexDirection = FlexDirection.ROW
    spacing: float = 0.0

    def arrange(
        self,
        items: tuple[FlexItem, ...],
        available: Size,
    ) -> tuple[Rect, ...]:
        if not items:
            return ()

        total_flex = sum(item.flex for item in items)

        if self.direction is FlexDirection.ROW:
            available_main = (
                available.width
                - self.spacing * (len(items) - 1)
            )
        else:
            available_main = (
                available.height
                - self.spacing * (len(items) - 1)
            )

        unit = available_main / total_flex

        rects: list[Rect] = []

        x = 0.0
        y = 0.0

        for item in items:
            main = unit * item.flex

            if self.direction is FlexDirection.ROW:
                rects.append(
                    Rect(
                        x=x,
                        y=0.0,
                        width=main,
                        height=available.height,
                    )
                )

                x += main + self.spacing

            else:
                rects.append(
                    Rect(
                        x=0.0,
                        y=y,
                        width=available.width,
                        height=main,
                    )
                )

                y += main + self.spacing

        return tuple(rects)