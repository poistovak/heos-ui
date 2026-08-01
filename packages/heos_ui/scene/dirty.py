from __future__ import annotations

from dataclasses import dataclass, field

from heos_ui.layout import Rect


@dataclass(slots=True)
class DirtyRegionEngine:
    """Tracks regions that require repaint."""

    _regions: list[Rect] = field(default_factory=list)

    def mark(self, rect: Rect) -> None:
        """Mark a rectangle as dirty."""

        self._regions.append(rect)

    def clear(self) -> None:
        """Clear all dirty regions."""

        self._regions.clear()

    @property
    def regions(self) -> tuple[Rect, ...]:
        """Return immutable dirty regions."""

        return tuple(self._regions)

    @property
    def count(self) -> int:
        return len(self._regions)

    @property
    def empty(self) -> bool:
        return not self._regions

    def union(self) -> Rect | None:
        """Return bounding rectangle of all dirty regions."""

        if not self._regions:
            return None

        left = min(r.x for r in self._regions)
        top = min(r.y for r in self._regions)

        right = max(r.x + r.width for r in self._regions)
        bottom = max(r.y + r.height for r in self._regions)

        return Rect(
            x=left,
            y=top,
            width=right - left,
            height=bottom - top,
        )