from heos_ui.runtime import RenderRegistry
from heos_ui.widgets.base import Widget


class DummyWidget(Widget):
    pass


def widget(name: str) -> DummyWidget:
    return DummyWidget(
        id=name,
        title=name,
    )


def test_registry_starts_empty() -> None:
    registry = RenderRegistry()

    assert registry.count == 0


def test_register_widget() -> None:
    registry = RenderRegistry()
    w = widget("solar")

    registry.register(w)

    assert registry.count == 1
    assert registry.get("solar") is w


def test_register_overwrites_same_id() -> None:
    registry = RenderRegistry()

    first = widget("grid")
    second = widget("grid")

    registry.register(first)
    registry.register(second)

    assert registry.count == 1
    assert registry.get("grid") is second


def test_unregister_widget() -> None:
    registry = RenderRegistry()
    w = widget("battery")

    registry.register(w)
    registry.unregister("battery")

    assert registry.count == 0
    assert registry.get("battery") is None


def test_clear_registry() -> None:
    registry = RenderRegistry()

    registry.register(widget("a"))
    registry.register(widget("b"))
    registry.register(widget("c"))

    registry.clear()

    assert registry.count == 0


def test_iterates_widgets() -> None:
    registry = RenderRegistry()

    registry.register(widget("a"))
    registry.register(widget("b"))

    ids = {w.id for w in registry}

    assert ids == {"a", "b"}