from __future__ import annotations

from dataclasses import dataclass

from .constraints import Size


@dataclass(frozen=True, slots=True)
class Rect:
    """Immutable layout rectangle."""

    x: float
    y: float
    width: float
    height: float


@dataclass(slots=True)
class ArrangeEngine:
    """Computes widget placement."""

    def arrange(
        self,
        x: float,
        y: float,
        size: Size,
    ) -> Rect:
        return Rect(
            x=x,
            y=y,
            width=size.width,
            height=size.height,
        )