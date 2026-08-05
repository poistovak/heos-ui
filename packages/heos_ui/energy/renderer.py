from __future__ import annotations

from dataclasses import dataclass

from .graph import EnergyGraph


@dataclass(slots=True, frozen=True)
class RenderNode:
    id: str
    title: str


@dataclass(slots=True, frozen=True)
class RenderEdge:
    source: str
    destination: str
    power: float
    active: bool


@dataclass(slots=True, frozen=True)
class RenderScene:
    nodes: tuple[RenderNode, ...]
    edges: tuple[RenderEdge, ...]


class EnergyRenderer:
    """Transforms an EnergyGraph into a renderable scene."""

    def render(
        self,
        graph: EnergyGraph,
    ) -> RenderScene:
        nodes = tuple(
            RenderNode(
                id=node.id,
                title=node.title,
            )
            for node in graph.nodes
        )

        edges = tuple(
            RenderEdge(
                source=flow.source,
                destination=flow.destination,
                power=flow.power,
                active=flow.active,
            )
            for flow in graph.flows
        )

        return RenderScene(
            nodes=nodes,
            edges=edges,
        )