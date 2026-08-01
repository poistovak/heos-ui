from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass, field

from .graph import SceneNode


@dataclass(slots=True)
class RenderQueue:
    """FIFO queue for scene rendering."""

    _queue: deque[SceneNode] = field(
        default_factory=deque,
        init=False,
        repr=False,
    )

    def push(self, node: SceneNode) -> None:
        self._queue.append(node)

    def pop(self) -> SceneNode:
        return self._queue.popleft()

    def extend(self, nodes: list[SceneNode]) -> None:
        self._queue.extend(nodes)

    def clear(self) -> None:
        self._queue.clear()

    @property
    def empty(self) -> bool:
        return not self._queue

    @property
    def size(self) -> int:
        return len(self._queue)

    def __iter__(self) -> Iterator[SceneNode]:
        return iter(self._queue)
