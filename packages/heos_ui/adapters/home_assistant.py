from __future__ import annotations

from dataclasses import dataclass

from heos_ui.energy import (
    EnergyFlow,
    EnergyGraph,
    EnergyNode,
    EnergyNodeType,
)


@dataclass(frozen=True, slots=True)
class HomeAssistantSnapshot:
    """Normalized energy snapshot received from Home Assistant."""

    pv_power: float = 0.0
    house_power: float = 0.0
    grid_power: float = 0.0
    battery_power: float = 0.0
    ev_power: float = 0.0
    heat_pump_power: float = 0.0

    battery_online: bool = False
    ev_online: bool = False
    heat_pump_online: bool = False


class HomeAssistantAdapter:
    """Transforms Home Assistant energy data into an EnergyGraph."""

    def build_graph(
        self,
        snapshot: HomeAssistantSnapshot,
    ) -> EnergyGraph:
        graph = EnergyGraph()

        self._add_core_nodes(graph)

        if snapshot.battery_online:
            graph.add_node(
                EnergyNode(
                    id="battery",
                    title="Battery",
                    node_type=EnergyNodeType.STORAGE,
                )
            )

        if snapshot.ev_online:
            graph.add_node(
                EnergyNode(
                    id="ev",
                    title="EV Charger",
                    node_type=EnergyNodeType.CONSUMER,
                )
            )

        if snapshot.heat_pump_online:
            graph.add_node(
                EnergyNode(
                    id="heat_pump",
                    title="Heat Pump",
                    node_type=EnergyNodeType.CONSUMER,
                )
            )

        self._add_flows(
            graph,
            snapshot,
        )

        return graph

    def _add_core_nodes(
        self,
        graph: EnergyGraph,
    ) -> None:
        graph.add_node(
            EnergyNode(
                id="pv",
                title="Photovoltaics",
                node_type=EnergyNodeType.PRODUCER,
            )
        )
        graph.add_node(
            EnergyNode(
                id="house",
                title="House",
                node_type=EnergyNodeType.CONSUMER,
            )
        )
        graph.add_node(
            EnergyNode(
                id="grid",
                title="Grid",
                node_type=EnergyNodeType.GRID,
            )
        )

    def _add_flows(
        self,
        graph: EnergyGraph,
        snapshot: HomeAssistantSnapshot,
    ) -> None:
        pv_remaining = max(0.0, snapshot.pv_power)

        house_base = max(
            0.0,
            snapshot.house_power
            - snapshot.ev_power
            - snapshot.heat_pump_power,
        )

        pv_to_house = min(
            pv_remaining,
            house_base,
        )
        self._add_flow(
            graph,
            "pv",
            "house",
            pv_to_house,
        )
        pv_remaining -= pv_to_house

        if snapshot.heat_pump_online:
            pv_to_heat_pump = min(
                pv_remaining,
                max(0.0, snapshot.heat_pump_power),
            )
            self._add_flow(
                graph,
                "pv",
                "heat_pump",
                pv_to_heat_pump,
            )
            pv_remaining -= pv_to_heat_pump

        if snapshot.ev_online:
            pv_to_ev = min(
                pv_remaining,
                max(0.0, snapshot.ev_power),
            )
            self._add_flow(
                graph,
                "pv",
                "ev",
                pv_to_ev,
            )
            pv_remaining -= pv_to_ev

        if (
            snapshot.battery_online
            and snapshot.battery_power > 0.0
        ):
            pv_to_battery = min(
                pv_remaining,
                snapshot.battery_power,
            )
            self._add_flow(
                graph,
                "pv",
                "battery",
                pv_to_battery,
            )
            pv_remaining -= pv_to_battery

        if pv_remaining > 0.0:
            self._add_flow(
                graph,
                "pv",
                "grid",
                pv_remaining,
            )

        if snapshot.grid_power > 0.0:
            self._add_flow(
                graph,
                "grid",
                "house",
                snapshot.grid_power,
            )

        if (
            snapshot.battery_online
            and snapshot.battery_power < 0.0
        ):
            self._add_flow(
                graph,
                "battery",
                "house",
                abs(snapshot.battery_power),
            )

    def _add_flow(
        self,
        graph: EnergyGraph,
        source: str,
        destination: str,
        power: float,
    ) -> None:
        if power <= 0.0:
            return

        graph.add_flow(
            EnergyFlow(
                source=source,
                destination=destination,
                power=power,
            )
        )