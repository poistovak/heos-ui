from heos_ui.layout.tree import LayoutNode, LayoutTree
from heos_ui.widgets.base import Widget


def widget(name: str) -> Widget:
    return Widget(
        id=name,
        title=name,
    )


def test_empty_root() -> None:
    root = LayoutNode(widget("root"))

    tree = LayoutTree(root)

    assert tree.size == 1


def test_add_child() -> None:
    root = LayoutNode(widget("root"))

    child = LayoutNode(widget("child"))

    root.add(child)

    assert len(root.children) == 1


def test_remove_child() -> None:
    root = LayoutNode(widget("root"))

    child = LayoutNode(widget("child"))

    root.add(child)
    root.remove(child)

    assert root.children == []


def test_walk_tree() -> None:
    root = LayoutNode(widget("root"))

    a = LayoutNode(widget("a"))
    b = LayoutNode(widget("b"))
    c = LayoutNode(widget("c"))

    root.add(a)
    root.add(b)

    a.add(c)

    tree = LayoutTree(root)

    names = [
        node.widget.id
        for node in tree.walk()
    ]

    assert names == [
        "root",
        "a",
        "c",
        "b",
    ]


def test_leaf_detection() -> None:
    node = LayoutNode(widget("leaf"))

    assert node.is_leaf


def test_non_leaf_detection() -> None:
    root = LayoutNode(widget("root"))

    root.add(
        LayoutNode(widget("child"))
    )

    assert not root.is_leaf