from __future__ import annotations

from dataclasses import dataclass, field

from .arrange import ArrangeEngine, Rect
from .constraints import LayoutConstraints, Size
from .measure import MeasureEngine
from .tree import LayoutTree


@dataclass(slots=True)
class LayoutPass:
    """Runs a complete measure and arrange pass."""

    arrange: ArrangeEngine = field(default_factory=ArrangeEngine)

    def run(
        self,
        tree: LayoutTree,
        constraints: LayoutConstraints,
    ) -> dict[str, Rect]:
        measure = MeasureEngine(constraints)

        available = measure.measure(
            Size(
                width=constraints.max_width,
                height=constraints.max_height,
            )
        )

        return {
            node.widget.id: self.arrange.arrange(
                0.0,
                0.0,
                available,
            )
            for node in tree.walk()
        }