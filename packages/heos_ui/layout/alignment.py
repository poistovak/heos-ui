from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .arrange import Rect
from .constraints import Size


class HorizontalAlignment(StrEnum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class VerticalAlignment(StrEnum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


@dataclass(frozen=True, slots=True)
class Alignment:
    horizontal: HorizontalAlignment = HorizontalAlignment.LEFT
    vertical: VerticalAlignment = VerticalAlignment.TOP

    def align(
        self,
        container: Rect,
        child: Size,
    ) -> Rect:
        if self.horizontal is HorizontalAlignment.LEFT:
            x = container.x
        elif self.horizontal is HorizontalAlignment.CENTER:
            x = container.x + (container.width - child.width) / 2
        else:
            x = container.x + container.width - child.width

        if self.vertical is VerticalAlignment.TOP:
            y = container.y
        elif self.vertical is VerticalAlignment.CENTER:
            y = container.y + (container.height - child.height) / 2
        else:
            y = container.y + container.height - child.height

        return Rect(
            x=x,
            y=y,
            width=child.width,
            height=child.height,
        )