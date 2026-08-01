from heos_ui.runtime import RenderOrchestrator
from heos_ui.widgets.base import Widget


class DummyWidget(Widget):
    def __init__(self, widget_id: str) -> None:
        super().__init__(
            id=widget_id,
            title=widget_id,
        )
        self.calls = 0

    def render(self) -> None:
        self.calls += 1


def test_starts_empty() -> None:
    runtime = RenderOrchestrator()

    assert runtime.widget_count == 0


def test_register_widget() -> None:
    runtime = RenderOrchestrator()

    runtime.register(DummyWidget("solar"))

    assert runtime.widget_count == 1


def test_invalidate_unknown_widget() -> None:
    runtime = RenderOrchestrator()

    assert runtime.invalidate("missing") is False


def test_render_registered_widget() -> None:
    runtime = RenderOrchestrator()

    widget = DummyWidget("battery")

    runtime.register(widget)
    runtime.invalidate("battery")

    event = runtime.render()

    assert event.rendered == 1
    assert widget.calls == 1


def test_multiple_widgets() -> None:
    runtime = RenderOrchestrator()

    for name in ("pv", "grid", "house"):
        runtime.register(DummyWidget(name))
        runtime.invalidate(name)

    event = runtime.render()

    assert event.rendered == 3


def test_registry_keeps_widgets() -> None:
    runtime = RenderOrchestrator()

    runtime.register(DummyWidget("ev"))
    runtime.render()

    assert runtime.widget_count == 1