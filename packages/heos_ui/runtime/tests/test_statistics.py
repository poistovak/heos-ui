from heos_ui.runtime import RenderEngine, RenderStatistics
from heos_ui.widgets.base import Widget


class RecordingWidget(Widget):
    def __init__(self, widget_id: str = "widget") -> None:
        super().__init__(
            id=widget_id,
            title=widget_id,
        )

    def render(self) -> None:
        pass


def test_statistics_start_at_zero() -> None:
    engine = RenderEngine()

    assert engine.statistics == RenderStatistics(
        attempted=0,
        rendered=0,
        skipped=0,
        batches=0,
    )


def test_successful_render_is_recorded() -> None:
    engine = RenderEngine()
    widget = RecordingWidget()
    widget.invalidate()

    engine.render(widget)

    assert engine.statistics == RenderStatistics(
        attempted=1,
        rendered=1,
        skipped=0,
        batches=0,
    )


def test_skipped_render_is_recorded() -> None:
    engine = RenderEngine()
    widget = RecordingWidget()

    engine.render(widget)

    assert engine.statistics == RenderStatistics(
        attempted=1,
        rendered=0,
        skipped=1,
        batches=0,
    )


def test_render_all_records_one_batch() -> None:
    engine = RenderEngine()
    first = RecordingWidget("first")
    second = RecordingWidget("second")

    first.invalidate()
    second.invalidate()

    engine.render_all((first, second))

    assert engine.statistics == RenderStatistics(
        attempted=2,
        rendered=2,
        skipped=0,
        batches=1,
    )


def test_mixed_batch_records_rendered_and_skipped() -> None:
    engine = RenderEngine()
    dirty = RecordingWidget("dirty")
    clean = RecordingWidget("clean")

    dirty.invalidate()

    rendered = engine.render_all((dirty, clean))

    assert rendered == 1
    assert engine.statistics == RenderStatistics(
        attempted=2,
        rendered=1,
        skipped=1,
        batches=1,
    )


def test_empty_batch_is_recorded() -> None:
    engine = RenderEngine()

    rendered = engine.render_all(())

    assert rendered == 0
    assert engine.statistics.batches == 1
    assert engine.statistics.attempted == 0


def test_statistics_snapshot_is_immutable() -> None:
    engine = RenderEngine()

    first_snapshot = engine.statistics

    widget = RecordingWidget()
    widget.invalidate()
    engine.render(widget)

    assert first_snapshot.rendered == 0
    assert engine.statistics.rendered == 1


def test_reset_clears_all_statistics() -> None:
    engine = RenderEngine()
    widget = RecordingWidget()
    widget.invalidate()

    engine.render_all((widget,))
    engine.reset_statistics()

    assert engine.statistics == RenderStatistics(
        attempted=0,
        rendered=0,
        skipped=0,
        batches=0,
    )
