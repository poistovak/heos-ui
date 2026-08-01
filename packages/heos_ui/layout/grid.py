from __future__ import annotations

from dataclasses import dataclass

from .arrange import Rect
from .constraints import Size


@dataclass(frozen=True, slots=True)
class GridLayout:
    """Arranges children in a fixed number of grid columns."""

    columns: int
    column_spacing: float = 0.0
    row_spacing: float = 0.0

    def __post_init__(self) -> None:
        if self.columns <= 0:
            raise ValueError("Grid columns must be greater than zero.")

        if self.column_spacing < 0.0:
            raise ValueError("Grid column spacing cannot be negative.")

        if self.row_spacing < 0.0:
            raise ValueError("Grid row spacing cannot be negative.")

    def measure(self, sizes: tuple[Size, ...]) -> Size:
        """Return the total size required by the grid."""

        if not sizes:
            return Size(0.0, 0.0)

        column_widths = self._column_widths(sizes)
        row_heights = self._row_heights(sizes)

        return Size(
            width=(
                sum(column_widths)
                + self.column_spacing * (len(column_widths) - 1)
            ),
            height=(
                sum(row_heights)
                + self.row_spacing * (len(row_heights) - 1)
            ),
        )

    def arrange(
        self,
        sizes: tuple[Size, ...],
        *,
        x: float = 0.0,
        y: float = 0.0,
    ) -> tuple[Rect, ...]:
        """Arrange children into grid cells."""

        if not sizes:
            return ()

        column_widths = self._column_widths(sizes)
        row_heights = self._row_heights(sizes)

        column_offsets: list[float] = []
        current_x = x

        for width in column_widths:
            column_offsets.append(current_x)
            current_x += width + self.column_spacing

        row_offsets: list[float] = []
        current_y = y

        for height in row_heights:
            row_offsets.append(current_y)
            current_y += height + self.row_spacing

        return tuple(
            Rect(
                x=column_offsets[index % self.columns],
                y=row_offsets[index // self.columns],
                width=size.width,
                height=size.height,
            )
            for index, size in enumerate(sizes)
        )

    def _column_widths(
        self,
        sizes: tuple[Size, ...],
    ) -> tuple[float, ...]:
        used_columns = min(self.columns, len(sizes))
        widths = [0.0] * used_columns

        for index, size in enumerate(sizes):
            column = index % self.columns
            widths[column] = max(widths[column], size.width)

        return tuple(widths)

    def _row_heights(
        self,
        sizes: tuple[Size, ...],
    ) -> tuple[float, ...]:
        row_count = (len(sizes) + self.columns - 1) // self.columns
        heights = [0.0] * row_count

        for index, size in enumerate(sizes):
            row = index // self.columns
            heights[row] = max(heights[row], size.height)

        return tuple(heights)
