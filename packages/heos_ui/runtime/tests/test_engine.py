from heos_ui.runtime import RenderEngine
from heos_ui.widgets.base import Widget


class RecordingWidget(Widget):
    def __init__(self, widget_id: str = "widget") -> None:
        super().__init__(
            id=widget_id,
            title=widget_id,
        )
        self.calls = 0

    def render(self) -> None:
        self.calls += 1


def test_engine_starts_empty() -> None:
    engine = RenderEngine()

    assert engine.render_count == 0


def test_render_dirty_widget() -> None:
    engine = RenderEngine()
    widget = RecordingWidget()

    widget.invalidate()

    assert engine.render(widget) is True
    assert widget.calls == 1
    assert engine.render_count == 1


def test_skip_clean_widget() -> None:
    engine = RenderEngine()
    widget = RecordingWidget()

    assert engine.render(widget) is False
    assert widget.calls == 0
    assert engine.render_count == 0


def test_render_all_widgets() -> None:
    engine = RenderEngine()

    solar = RecordingWidget("solar")
    battery = RecordingWidget("battery")
    grid = RecordingWidget("grid")

    solar.invalidate()
    battery.invalidate()
    grid.invalidate()

    rendered = engine.render_all(
        (
            solar,
            battery,
            grid,
        )
    )

    assert rendered == 3
    assert solar.calls == 1
    assert battery.calls == 1
    assert grid.calls == 1
    assert engine.render_count == 3


def test_duplicate_render_is_skipped() -> None:
    engine = RenderEngine()
    widget = RecordingWidget()

    widget.invalidate()

    assert engine.render(widget) is True
    assert engine.render(widget) is False
    assert widget.calls == 1
    assert engine.render_count == 1


def test_reset_statistics() -> None:
    engine = RenderEngine()
    widget = RecordingWidget()

    widget.invalidate()
    engine.render(widget)

    engine.reset_statistics()

    assert engine.render_count == 0