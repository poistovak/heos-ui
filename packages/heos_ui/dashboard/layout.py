from __future__ import annotations

from dataclasses import dataclass

from heos_ui.layout import (
    EdgeInsets,
    LayoutConstraints,
    LayoutNode,
    LayoutRuntime,
    LayoutTree,
)
from heos_ui.widgets.base import Widget


@dataclass(slots=True)
class DashboardLayout:
    """High-level dashboard layout engine."""

    columns: int = 2
    padding: EdgeInsets = EdgeInsets.all(16.0)

    def build(
        self,
        widgets: list[Widget],
        constraints: LayoutConstraints,
    ) -> LayoutRuntime:
        root = LayoutNode(
            Widget(
                id="dashboard",
                title="Dashboard",
            )
        )

        for widget in widgets:
            root.add(LayoutNode(widget))

        tree = LayoutTree(root)

        runtime = LayoutRuntime(
            tree=tree,
            constraints=constraints,
        )

        runtime.layout()

        return runtime