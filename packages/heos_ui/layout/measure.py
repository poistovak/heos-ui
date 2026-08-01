from __future__ import annotations

from dataclasses import dataclass

from .constraints import LayoutConstraints, Size


@dataclass(slots=True)
class MeasureEngine:
    """Computes widget sizes from layout constraints."""

    constraints: LayoutConstraints

    def measure(self, desired: Size) -> Size:
        """Return the constrained widget size."""

        return self.constraints.constrain(desired)