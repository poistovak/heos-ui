from heos_ui.layout import (
    LayoutConstraints,
    LayoutNode,
    LayoutPass,
    LayoutTree,
)
from heos_ui.widgets.base import Widget


def widget(name: str) -> Widget:
    return Widget(
        id=name,
        title=name,
    )


def test_layout_pass_single_node() -> None:
    tree = LayoutTree(
        LayoutNode(widget("root"))
    )

    result = LayoutPass().run(
        tree,
        LayoutConstraints(
            max_width=300.0,
            max_height=200.0,
        ),
    )

    assert result["root"].width == 300.0
    assert result["root"].height == 200.0


def test_layout_pass_multiple_nodes() -> None:
    root = LayoutNode(widget("root"))
    root.add(LayoutNode(widget("a")))
    root.add(LayoutNode(widget("b")))

    result = LayoutPass().run(
        LayoutTree(root),
        LayoutConstraints(
            max_width=500.0,
            max_height=400.0,
        ),
    )

    assert len(result) == 3


def test_every_node_receives_rect() -> None:
    root = LayoutNode(widget("root"))
    root.add(LayoutNode(widget("child")))

    result = LayoutPass().run(
        LayoutTree(root),
        LayoutConstraints(
            max_width=100.0,
            max_height=50.0,
        ),
    )

    assert set(result) == {
        "root",
        "child",
    }


def test_single_node_tree_has_one_result() -> None:
    tree = LayoutTree(
        LayoutNode(widget("only"))
    )

    result = LayoutPass().run(
        tree,
        LayoutConstraints(
            max_width=10.0,
            max_height=20.0,
        ),
    )

    assert len(result) == 1


def test_layout_pass_is_repeatable() -> None:
    tree = LayoutTree(
        LayoutNode(widget("root"))
    )
    layout_pass = LayoutPass()
    constraints = LayoutConstraints(
        max_width=320.0,
        max_height=240.0,
    )

    assert layout_pass.run(
        tree,
        constraints,
    ) == layout_pass.run(
        tree,
        constraints,
    )