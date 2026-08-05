from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class EnergyNode:
    """Energy graph node."""

    id: str
    title: str


@dataclass(slots=True, frozen=True)
class EnergyFlow:
    """Directed energy flow."""

    source: str
    destination: str
    power: float
    active: bool = True


@dataclass(slots=True)
class EnergyFlowWidget:
    """Visualizes energy flow graph."""

    _nodes: dict[str, EnergyNode] = field(
        default_factory=dict,
        init=False,
    )

    _flows: list[EnergyFlow] = field(
        default_factory=list,
        init=False,
    )

    def add_node(
        self,
        node: EnergyNode,
    ) -> None:
        self._nodes[node.id] = node

    def add_flow(
        self,
        flow: EnergyFlow,
    ) -> None:
        self._flows.append(flow)

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def flow_count(self) -> int:
        return len(self._flows)

    @property
    def active_flows(self) -> tuple[EnergyFlow, ...]:
        return tuple(
            flow
            for flow in self._flows
            if flow.active
        )

    @property
    def total_power(self) -> float:
        return sum(
            flow.power
            for flow in self._flows
            if flow.active
        )