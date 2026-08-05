from heos_ui.energy import (
    EnergyFlow,
    EnergyGraph,
    EnergyNode,
    EnergyNodeType,
)
from heos_ui.energy.renderer import EnergyRenderer


def create_graph() -> EnergyGraph:
    graph = EnergyGraph()

    graph.add_node(
        EnergyNode(
            "pv",
            "PV",
            EnergyNodeType.PRODUCER,
        )
    )
    graph.add_node(
        EnergyNode(
            "house",
            "House",
            EnergyNodeType.CONSUMER,
        )
    )
    graph.add_flow(
        EnergyFlow(
            "pv",
            "house",
            5.2,
        )
    )

    return graph


def test_render_scene() -> None:
    scene = EnergyRenderer().render(
        create_graph()
    )

    assert len(scene.nodes) == 2
    assert len(scene.edges) == 1


def test_render_node() -> None:
    scene = EnergyRenderer().render(
        create_graph()
    )

    assert scene.nodes[0].id == "pv"
    assert scene.nodes[0].title == "PV"


def test_render_edge() -> None:
    scene = EnergyRenderer().render(
        create_graph()
    )

    edge = scene.edges[0]

    assert edge.source == "pv"
    assert edge.destination == "house"
    assert edge.power == 5.2
    assert edge.active


def test_empty_graph() -> None:
    scene = EnergyRenderer().render(
        EnergyGraph()
    )

    assert scene.nodes == ()
    assert scene.edges == ()


def test_inactive_flow() -> None:
    graph = EnergyGraph()

    graph.add_node(
        EnergyNode(
            "grid",
            "Grid",
            EnergyNodeType.GRID,
        )
    )
    graph.add_node(
        EnergyNode(
            "house",
            "House",
            EnergyNodeType.CONSUMER,
        )
    )
    graph.add_flow(
        EnergyFlow(
            "grid",
            "house",
            3.5,
            active=False,
        )
    )

    scene = EnergyRenderer().render(graph)

    assert not scene.edges[0].active