import pytest
from heos_ui.energy import (
    EnergyFlow,
    EnergyGraph,
    EnergyNode,
    EnergyNodeType,
)


def node(
    node_id: str,
    node_type: EnergyNodeType,
) -> EnergyNode:
    return EnergyNode(
        id=node_id,
        title=node_id.title(),
        node_type=node_type,
    )


def create_graph() -> EnergyGraph:
    graph = EnergyGraph()

    graph.add_node(
        node(
            "pv",
            EnergyNodeType.PRODUCER,
        )
    )
    graph.add_node(
        node(
            "house",
            EnergyNodeType.CONSUMER,
        )
    )
    graph.add_node(
        node(
            "battery",
            EnergyNodeType.STORAGE,
        )
    )
    graph.add_node(
        node(
            "grid",
            EnergyNodeType.GRID,
        )
    )

    return graph


def test_empty_graph() -> None:
    graph = EnergyGraph()

    assert graph.node_count == 0
    assert graph.flow_count == 0
    assert graph.total_active_power == 0.0


def test_add_node() -> None:
    graph = EnergyGraph()

    graph.add_node(
        node(
            "pv",
            EnergyNodeType.PRODUCER,
        )
    )

    assert graph.node_count == 1
    assert graph.node("pv") is not None


def test_duplicate_node_is_rejected() -> None:
    graph = EnergyGraph()
    pv = node(
        "pv",
        EnergyNodeType.PRODUCER,
    )

    graph.add_node(pv)

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        graph.add_node(pv)


def test_add_flow() -> None:
    graph = create_graph()

    graph.add_flow(
        EnergyFlow(
            source="pv",
            destination="house",
            power=4.5,
        )
    )

    assert graph.flow_count == 1
    assert graph.total_active_power == 4.5


def test_flow_requires_known_source() -> None:
    graph = create_graph()

    with pytest.raises(
        KeyError,
        match="missing",
    ):
        graph.add_flow(
            EnergyFlow(
                source="missing",
                destination="house",
                power=1.0,
            )
        )


def test_flow_requires_known_destination() -> None:
    graph = create_graph()

    with pytest.raises(
        KeyError,
        match="missing",
    ):
        graph.add_flow(
            EnergyFlow(
                source="pv",
                destination="missing",
                power=1.0,
            )
        )


def test_duplicate_flow_is_rejected() -> None:
    graph = create_graph()
    flow = EnergyFlow(
        source="pv",
        destination="house",
        power=3.0,
    )

    graph.add_flow(flow)

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        graph.add_flow(flow)


def test_incoming_and_outgoing_flows() -> None:
    graph = create_graph()

    graph.add_flow(
        EnergyFlow(
            source="pv",
            destination="house",
            power=3.0,
        )
    )
    graph.add_flow(
        EnergyFlow(
            source="pv",
            destination="battery",
            power=2.0,
        )
    )

    assert len(graph.outgoing("pv")) == 2
    assert len(graph.incoming("house")) == 1
    assert len(graph.incoming("battery")) == 1


def test_inactive_flows_are_ignored_by_default() -> None:
    graph = create_graph()

    graph.add_flow(
        EnergyFlow(
            source="grid",
            destination="house",
            power=5.0,
            active=False,
        )
    )

    assert graph.incoming("house") == ()
    assert len(
        graph.incoming(
            "house",
            active_only=False,
        )
    ) == 1


def test_node_power_balance() -> None:
    graph = create_graph()

    graph.add_flow(
        EnergyFlow(
            source="pv",
            destination="house",
            power=4.0,
        )
    )
    graph.add_flow(
        EnergyFlow(
            source="battery",
            destination="house",
            power=1.5,
        )
    )

    assert graph.incoming_power("house") == 5.5
    assert graph.outgoing_power("pv") == 4.0
    assert graph.balance("house") == 5.5
    assert graph.balance("pv") == -4.0


def test_clear_flows_preserves_nodes() -> None:
    graph = create_graph()

    graph.add_flow(
        EnergyFlow(
            source="pv",
            destination="house",
            power=3.0,
        )
    )

    graph.clear_flows()

    assert graph.flow_count == 0
    assert graph.node_count == 4


def test_invalid_flow_values_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="must differ",
    ):
        EnergyFlow(
            source="pv",
            destination="pv",
            power=1.0,
        )

    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        EnergyFlow(
            source="pv",
            destination="house",
            power=-1.0,
        )