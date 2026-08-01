from heos_ui.layout import (
    LayoutConstraints,
    LayoutNode,
    LayoutRuntime,
    LayoutTree,
)
from heos_ui.widgets.base import Widget


def widget(name: str) -> Widget:
    return Widget(
        id=name,
        title=name,
    )


def create_runtime() -> LayoutRuntime:
    root = LayoutNode(widget("root"))
    root.add(LayoutNode(widget("solar")))
    root.add(LayoutNode(widget("battery")))

    return LayoutRuntime(
        tree=LayoutTree(root),
        constraints=LayoutConstraints(
            max_width=800.0,
            max_height=600.0,
        ),
    )


def test_runtime_starts_without_layout() -> None:
    runtime = create_runtime()

    assert runtime.revision == 0
    assert runtime.rects == {}


def test_layout_processes_entire_tree() -> None:
    runtime = create_runtime()

    result = runtime.layout()

    assert set(result) == {
        "root",
        "solar",
        "battery",
    }
    assert runtime.revision == 1


def test_layout_uses_current_constraints() -> None:
    runtime = create_runtime()

    result = runtime.layout()

    assert result["root"].width == 800.0
    assert result["root"].height == 600.0


def test_updated_constraints_apply_to_next_pass() -> None:
    runtime = create_runtime()
    runtime.layout()

    runtime.update_constraints(
        LayoutConstraints(
            max_width=400.0,
            max_height=300.0,
        )
    )

    result = runtime.layout()

    assert result["root"].width == 400.0
    assert result["root"].height == 300.0
    assert runtime.revision == 2


def test_updated_tree_applies_to_next_pass() -> None:
    runtime = create_runtime()
    runtime.layout()

    new_root = LayoutNode(widget("dashboard"))
    new_root.add(LayoutNode(widget("grid")))

    runtime.update_tree(LayoutTree(new_root))

    result = runtime.layout()

    assert set(result) == {
        "dashboard",
        "grid",
    }


def test_rect_for_returns_latest_rectangle() -> None:
    runtime = create_runtime()
    runtime.layout()

    rect = runtime.rect_for("solar")

    assert rect is not None
    assert rect.width == 800.0
    assert runtime.rect_for("missing") is None


def test_rects_returns_copy() -> None:
    runtime = create_runtime()
    runtime.layout()

    result = runtime.rects
    result.clear()

    assert len(runtime.rects) == 3


def test_clear_removes_latest_layout() -> None:
    runtime = create_runtime()
    runtime.layout()

    runtime.clear()

    assert runtime.rects == {}
    assert runtime.revision == 1
