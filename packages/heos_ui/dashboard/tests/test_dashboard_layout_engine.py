from heos_ui.dashboard.layout import DashboardLayout
from heos_ui.layout import LayoutConstraints
from heos_ui.widgets.base import Widget


def widget(name: str) -> Widget:
    return Widget(
        id=name,
        title=name,
    )


def test_empty_dashboard() -> None:
    runtime = DashboardLayout().build(
        [],
        LayoutConstraints(
            max_width=800.0,
            max_height=600.0,
        ),
    )

    assert runtime.tree.size == 1


def test_dashboard_contains_all_widgets() -> None:
    runtime = DashboardLayout().build(
        [
            widget("solar"),
            widget("battery"),
            widget("house"),
        ],
        LayoutConstraints(
            max_width=800.0,
            max_height=600.0,
        ),
    )

    assert runtime.tree.size == 4


def test_dashboard_runtime_has_layout() -> None:
    runtime = DashboardLayout().build(
        [
            widget("solar"),
        ],
        LayoutConstraints(
            max_width=500.0,
            max_height=400.0,
        ),
    )

    assert runtime.rect_for("solar") is not None


def test_dashboard_root_exists() -> None:
    runtime = DashboardLayout().build(
        [],
        LayoutConstraints(
            max_width=100.0,
            max_height=100.0,
        ),
    )

    assert runtime.tree.root.widget.id == "dashboard"


def test_dashboard_layout_repeatable() -> None:
    layout = DashboardLayout()

    first = layout.build(
        [widget("a")],
        LayoutConstraints(
            max_width=200.0,
            max_height=100.0,
        ),
    )

    second = layout.build(
        [widget("a")],
        LayoutConstraints(
            max_width=200.0,
            max_height=100.0,
        ),
    )

    assert first.rect_for("a") == second.rect_for("a")