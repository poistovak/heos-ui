from __future__ import annotations

from .arrange import Rect
from .constraints import LayoutConstraints
from .layout_pass import LayoutPass
from .tree import LayoutTree


class LayoutRuntime:
    """Coordinates repeated layout passes for a layout tree."""

    def __init__(
        self,
        tree: LayoutTree,
        constraints: LayoutConstraints,
        layout_pass: LayoutPass | None = None,
    ) -> None:
        self._tree = tree
        self._constraints = constraints
        self._layout_pass = layout_pass or LayoutPass()
        self._rects: dict[str, Rect] = {}
        self._revision = 0

    @property
    def tree(self) -> LayoutTree:
        """Return the active layout tree."""

        return self._tree

    @property
    def constraints(self) -> LayoutConstraints:
        """Return the active layout constraints."""

        return self._constraints

    @property
    def revision(self) -> int:
        """Return the number of completed layout passes."""

        return self._revision

    @property
    def rects(self) -> dict[str, Rect]:
        """Return a copy of the latest layout result."""

        return dict(self._rects)

    def layout(self) -> dict[str, Rect]:
        """Run one complete layout pass."""

        self._rects = self._layout_pass.run(
            self._tree,
            self._constraints,
        )
        self._revision += 1

        return self.rects

    def update_constraints(
        self,
        constraints: LayoutConstraints,
    ) -> None:
        """Replace the active layout constraints."""

        self._constraints = constraints

    def update_tree(self, tree: LayoutTree) -> None:
        """Replace the active layout tree."""

        self._tree = tree

    def rect_for(self, widget_id: str) -> Rect | None:
        """Return the latest rectangle for a widget."""

        return self._rects.get(widget_id)

    def clear(self) -> None:
        """Clear the latest calculated layout."""

        self._rects.clear()
