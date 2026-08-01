from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Size:
    """Two-dimensional layout size."""

    width: float
    height: float


@dataclass(frozen=True, slots=True)
class LayoutConstraints:
    """Minimum and maximum layout dimensions."""

    min_width: float = 0.0
    max_width: float = float("inf")
    min_height: float = 0.0
    max_height: float = float("inf")

    def __post_init__(self) -> None:
        if self.min_width < 0.0 or self.min_height < 0.0:
            raise ValueError("Minimum dimensions cannot be negative.")

        if self.max_width < self.min_width:
            raise ValueError("Maximum width cannot be smaller than minimum width.")

        if self.max_height < self.min_height:
            raise ValueError(
                "Maximum height cannot be smaller than minimum height."
            )

    def constrain(self, size: Size) -> Size:
        """Clamp a size to these constraints."""

        return Size(
            width=min(
                max(size.width, self.min_width),
                self.max_width,
            ),
            height=min(
                max(size.height, self.min_height),
                self.max_height,
            ),
        )

    def loosen(self) -> LayoutConstraints:
        """Remove minimum dimensions while preserving maximums."""

        return LayoutConstraints(
            max_width=self.max_width,
            max_height=self.max_height,
        )

    def tighten(
        self,
        *,
        width: float | None = None,
        height: float | None = None,
    ) -> LayoutConstraints:
        """Create fixed constraints for supplied dimensions."""

        constrained_width = (
            self.constrain(Size(width, 0.0)).width
            if width is not None
            else None
        )
        constrained_height = (
            self.constrain(Size(0.0, height)).height
            if height is not None
            else None
        )

        return LayoutConstraints(
            min_width=(
                constrained_width
                if constrained_width is not None
                else self.min_width
            ),
            max_width=(
                constrained_width
                if constrained_width is not None
                else self.max_width
            ),
            min_height=(
                constrained_height
                if constrained_height is not None
                else self.min_height
            ),
            max_height=(
                constrained_height
                if constrained_height is not None
                else self.max_height
            ),
        )
