from heos_ui.widgets.energy_flow import (
    EnergyFlow,
    EnergyFlowWidget,
    EnergyNode,
)


def test_empty_widget() -> None:
    widget = EnergyFlowWidget()

    assert widget.node_count == 0
    assert widget.flow_count == 0
    assert widget.total_power == 0.0


def test_add_node() -> None:
    widget = EnergyFlowWidget()

    widget.add_node(
        EnergyNode(
            "pv",
            "PV",
        )
    )

    assert widget.node_count == 1


def test_add_flow() -> None:
    widget = EnergyFlowWidget()

    widget.add_flow(
        EnergyFlow(
            "pv",
            "house",
            4.5,
        )
    )

    assert widget.flow_count == 1
    assert widget.total_power == 4.5


def test_active_flow() -> None:
    widget = EnergyFlowWidget()

    widget.add_flow(
        EnergyFlow(
            "pv",
            "battery",
            2.0,
        )
    )

    widget.add_flow(
        EnergyFlow(
            "grid",
            "house",
            5.0,
            active=False,
        )
    )

    assert len(widget.active_flows) == 1


def test_multiple_nodes() -> None:
    widget = EnergyFlowWidget()

    for node in (
        EnergyNode("pv", "PV"),
        EnergyNode("battery", "Battery"),
        EnergyNode("house", "House"),
        EnergyNode("grid", "Grid"),
    ):
        widget.add_node(node)

    assert widget.node_count == 4


def test_total_power_multiple_flows() -> None:
    widget = EnergyFlowWidget()

    widget.add_flow(EnergyFlow("pv", "house", 3.5))
    widget.add_flow(EnergyFlow("battery", "house", 1.5))

    assert widget.total_power == 5.0