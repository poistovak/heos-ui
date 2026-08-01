from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from heos_ui.layout import Rect


@dataclass(slots=True)
class SceneNode:
    """Visual node inside the scene graph."""

    id: str
    rect: Rect
    children: list["SceneNode"] = field(default_factory=list)

    def add(self, child: "SceneNode") -> None:
        self.children.append(child)

    def walk(self) -> Iterator["SceneNode"]:
        yield self

        for child in self.children:
            yield from child.walk()


@dataclass(slots=True)
class SceneGraph:
    """Hierarchy of visual nodes."""

    root: SceneNode

    def walk(self) -> Iterator[SceneNode]:
        yield from self.root.walk()

    @property
    def size(self) -> int:
        return sum(1 for _ in self.walk())