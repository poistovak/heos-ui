from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Breakpoints:
    mobile: float = 640.0
    tablet: float = 1024.0


@dataclass(frozen=True, slots=True)
class ResponsiveLayout:
    """Determines layout properties from available width."""

    breakpoints: Breakpoints = Breakpoints()

    def columns(self, width: float) -> int:
        if width < self.breakpoints.mobile:
            return 1

        if width < self.breakpoints.tablet:
            return 2

        return 3

    def spacing(self, width: float) -> float:
        if width < self.breakpoints.mobile:
            return 8.0

        if width < self.breakpoints.tablet:
            return 12.0

        return 16.0