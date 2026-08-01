from heos_ui.runtime import RenderCoordinator
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
    runtime = RenderCoordinator()

    assert runtime.widget_count == 0


def test_add_widget() -> None:
    runtime = RenderCoordinator()

    runtime.add(DummyWidget("solar"))

    assert runtime.widget_count == 1


def test_invalidate_registered_widget() -> None:
    runtime = RenderCoordinator()
    widget = DummyWidget("battery")

    runtime.add(widget)

    assert runtime.invalidate(widget) is True


def test_render_widget() -> None:
    runtime = RenderCoordinator()
    widget = DummyWidget("grid")

    runtime.add(widget)
    runtime.invalidate(widget)

    event = runtime.render()

    assert event.rendered == 1
    assert widget.calls == 1


def test_multiple_widgets() -> None:
    runtime = RenderCoordinator()

    for name in ("pv", "house", "ev"):
        widget = DummyWidget(name)
        runtime.add(widget)
        runtime.invalidate(widget)

    assert runtime.render().rendered == 3


def test_unknown_widget() -> None:
    runtime = RenderCoordinator()

    assert runtime.invalidate(DummyWidget("x")) is False