from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class EnergyNodeType(StrEnum):
    """Supported energy node types."""

    PRODUCER = "producer"
    CONSUMER = "consumer"
    STORAGE = "storage"
    GRID = "grid"


@dataclass(frozen=True, slots=True)
class EnergyNode:
    """One device or system inside the energy graph."""

    id: str
    title: str
    node_type: EnergyNodeType


@dataclass(frozen=True, slots=True)
class EnergyFlow:
    """Directed power flow between two energy nodes."""

    source: str
    destination: str
    power: float
    active: bool = True

    def __post_init__(self) -> None:
        if self.source == self.destination:
            raise ValueError(
                "Energy flow source and destination must differ."
            )

        if self.power < 0.0:
            raise ValueError(
                "Energy flow power cannot be negative."
            )


@dataclass(slots=True)
class EnergyGraph:
    """Domain model describing energy nodes and power flows."""

    _nodes: dict[str, EnergyNode] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )
    _flows: list[EnergyFlow] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    @property
    def nodes(self) -> tuple[EnergyNode, ...]:
        return tuple(self._nodes.values())

    @property
    def flows(self) -> tuple[EnergyFlow, ...]:
        return tuple(self._flows)

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def flow_count(self) -> int:
        return len(self._flows)

    def add_node(self, node: EnergyNode) -> None:
        if node.id in self._nodes:
            raise ValueError(
                f"Energy node '{node.id}' is already registered."
            )

        self._nodes[node.id] = node

    def add_flow(self, flow: EnergyFlow) -> None:
        self._require_node(flow.source)
        self._require_node(flow.destination)

        if flow in self._flows:
            raise ValueError(
                "Energy flow is already registered."
            )

        self._flows.append(flow)

    def node(self, node_id: str) -> EnergyNode | None:
        return self._nodes.get(node_id)

    def incoming(
        self,
        node_id: str,
        *,
        active_only: bool = True,
    ) -> tuple[EnergyFlow, ...]:
        self._require_node(node_id)

        return tuple(
            flow
            for flow in self._flows
            if flow.destination == node_id
            and (flow.active or not active_only)
        )

    def outgoing(
        self,
        node_id: str,
        *,
        active_only: bool = True,
    ) -> tuple[EnergyFlow, ...]:
        self._require_node(node_id)

        return tuple(
            flow
            for flow in self._flows
            if flow.source == node_id
            and (flow.active or not active_only)
        )

    def incoming_power(self, node_id: str) -> float:
        return sum(
            flow.power
            for flow in self.incoming(node_id)
        )

    def outgoing_power(self, node_id: str) -> float:
        return sum(
            flow.power
            for flow in self.outgoing(node_id)
        )

    def balance(self, node_id: str) -> float:
        """Return incoming power minus outgoing power."""

        return (
            self.incoming_power(node_id)
            - self.outgoing_power(node_id)
        )

    @property
    def active_flows(self) -> tuple[EnergyFlow, ...]:
        return tuple(
            flow
            for flow in self._flows
            if flow.active
        )

    @property
    def total_active_power(self) -> float:
        return sum(
            flow.power
            for flow in self.active_flows
        )

    def clear_flows(self) -> None:
        self._flows.clear()

    def _require_node(self, node_id: str) -> None:
        if node_id not in self._nodes:
            raise KeyError(
                f"Unknown energy node '{node_id}'."
            )