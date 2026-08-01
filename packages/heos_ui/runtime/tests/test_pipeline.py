from heos_ui.runtime import RenderPipeline
from heos_ui.widgets.base import Widget


class RecordingWidget(Widget):
    def __init__(self, widget_id: str = "widget") -> None:
        super().__init__(
            id=widget_id,
            title=widget_id,
        )
        self.render_calls = 0

    def render(self) -> None:
        self.render_calls += 1


def test_pipeline_starts_empty() -> None:
    pipeline = RenderPipeline()

    assert pipeline.pending_count == 0


def test_invalidate_marks_and_queues_widget() -> None:
    pipeline = RenderPipeline()
    widget = RecordingWidget()

    changed = pipeline.invalidate(widget)

    assert changed is True
    assert widget.dirty is True
    assert pipeline.pending_count == 1


def test_repeated_invalidation_is_coalesced() -> None:
    pipeline = RenderPipeline()
    widget = RecordingWidget()

    first = pipeline.invalidate(widget)
    second = pipeline.invalidate(widget)
    third = pipeline.invalidate(widget)

    assert first is True
    assert second is False
    assert third is False
    assert pipeline.pending_count == 1


def test_render_pending_renders_widget_once() -> None:
    pipeline = RenderPipeline()
    widget = RecordingWidget()

    pipeline.invalidate(widget)
    pipeline.invalidate(widget)

    rendered = pipeline.render_pending()

    assert rendered == 1
    assert widget.render_calls == 1
    assert widget.dirty is False
    assert pipeline.pending_count == 0


def test_render_pending_batches_multiple_widgets() -> None:
    pipeline = RenderPipeline()
    solar = RecordingWidget("solar")
    battery = RecordingWidget("battery")
    grid = RecordingWidget("grid")

    pipeline.invalidate(solar)
    pipeline.invalidate(battery)
    pipeline.invalidate(grid)

    assert pipeline.render_pending() == 3
    assert solar.render_calls == 1
    assert battery.render_calls == 1
    assert grid.render_calls == 1


def test_clear_discards_pending_widgets() -> None:
    pipeline = RenderPipeline()
    widget = RecordingWidget()

    pipeline.invalidate(widget)
    pipeline.clear()

    assert pipeline.pending_count == 0
    assert pipeline.render_pending() == 0
    assert widget.render_calls == 0
