from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from heos_ui.widgets.base import Widget


@dataclass(slots=True)
class LayoutNode:
    """Node in the layout tree."""

    widget: Widget
    children: list["LayoutNode"] = field(default_factory=list)

    def add(self, child: "LayoutNode") -> None:
        self.children.append(child)

    def remove(self, child: "LayoutNode") -> None:
        self.children.remove(child)

    def walk(self) -> Iterator["LayoutNode"]:
        yield self

        for child in self.children:
            yield from child.walk()

    @property
    def is_leaf(self) -> bool:
        return not self.children


@dataclass(slots=True)
class LayoutTree:
    """Hierarchy of layout nodes."""

    root: LayoutNode

    def walk(self) -> Iterator[LayoutNode]:
        yield from self.root.walk()

    @property
    def size(self) -> int:
        return sum(1 for _ in self.walk())