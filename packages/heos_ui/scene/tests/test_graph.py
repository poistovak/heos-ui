from heos_ui.layout import Rect
from heos_ui.scene import SceneGraph, SceneNode


def rect() -> Rect:
    return Rect(
        0.0,
        0.0,
        100.0,
        100.0,
    )


def test_scene_graph_root() -> None:
    graph = SceneGraph(
        SceneNode(
            id="root",
            rect=rect(),
        )
    )

    assert graph.size == 1


def test_add_child() -> None:
    root = SceneNode(
        id="root",
        rect=rect(),
    )

    root.add(
        SceneNode(
            id="child",
            rect=rect(),
        )
    )

    assert len(root.children) == 1


def test_walk_graph() -> None:
    root = SceneNode(
        id="root",
        rect=rect(),
    )

    root.add(
        SceneNode(
            id="solar",
            rect=rect(),
        )
    )

    graph = SceneGraph(root)

    assert [
        node.id
        for node in graph.walk()
    ] == [
        "root",
        "solar",
    ]


def test_nested_scene() -> None:
    root = SceneNode("root", rect())

    a = SceneNode("a", rect())
    b = SceneNode("b", rect())

    root.add(a)
    a.add(b)

    graph = SceneGraph(root)

    assert graph.size == 3


def test_rect_preserved() -> None:
    r = Rect(
        10.0,
        20.0,
        300.0,
        150.0,
    )

    node = SceneNode(
        id="panel",
        rect=r,
    )

    assert node.rect == r