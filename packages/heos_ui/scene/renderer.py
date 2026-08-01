from __future__ import annotations

from dataclasses import dataclass

from .graph import SceneGraph, SceneNode
from .render_queue import RenderQueue


@dataclass(slots=True)
class RenderResult:
    """Result of one render pass."""

    rendered_nodes: int


class SceneRenderer:
    """Traverses a scene graph and builds a render pass."""

    def render(
        self,
        graph: SceneGraph,
    ) -> RenderResult:
        queue = RenderQueue()

        queue.extend(
            list(graph.walk())
        )

        rendered = 0

        while not queue.empty:
            node = queue.pop()

            self.render_node(node)

            rendered += 1

        return RenderResult(
            rendered_nodes=rendered,
        )

    def render_node(
        self,
        node: SceneNode,
    ) -> None:
        """Render one scene node.

        Future milestones will translate this node into
        paint commands.
        """
        _ = node