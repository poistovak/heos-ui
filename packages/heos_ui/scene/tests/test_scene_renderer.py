from heos_ui.layout import Rect
from heos_ui.scene import SceneGraph, SceneNode
from heos_ui.scene.renderer import (
    RenderResult,
    SceneRenderer,
)


def node(name: str) -> SceneNode:
    return SceneNode(
        id=name,
        rect=Rect(
            0.0,
            0.0,
            100.0,
            100.0,
        ),
    )


def test_render_empty_scene() -> None:
    renderer = SceneRenderer()

    graph = SceneGraph(
        node("root"),
    )

    result = renderer.render(graph)

    assert isinstance(result, RenderResult)
    assert result.rendered_nodes == 1


def test_render_multiple_nodes() -> None:
    root = node("root")

    root.add(node("solar"))
    root.add(node("battery"))

    renderer = SceneRenderer()

    result = renderer.render(
        SceneGraph(root),
    )

    assert result.rendered_nodes == 3


def test_render_nested_scene() -> None:
    root = node("root")

    solar = node("solar")
    inverter = node("inverter")

    solar.add(inverter)

    root.add(solar)

    renderer = SceneRenderer()

    result = renderer.render(
        SceneGraph(root),
    )

    assert result.rendered_nodes == 3


def test_renderer_repeatable() -> None:
    graph = SceneGraph(
        node("root"),
    )

    renderer = SceneRenderer()

    first = renderer.render(graph)
    second = renderer.render(graph)

    assert first == second


def test_render_node() -> None:
    renderer = SceneRenderer()

    renderer.render_node(
        node("widget"),
    )