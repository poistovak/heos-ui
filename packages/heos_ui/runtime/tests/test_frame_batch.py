import pytest

from heos_ui.runtime import FrameBatch, RenderPipeline
from heos_ui.widgets.base import Widget


class RecordingWidget(Widget):
    def __init__(self, widget_id: str) -> None:
        super().__init__(id=widget_id, title=widget_id)
        self.render_calls = 0
        self.on_render = None

    def render(self) -> None:
        self.render_calls += 1

        if self.on_render is not None:
            self.on_render()


def test_batch_starts_empty() -> None:
    batch = FrameBatch()

    assert batch.frame_id == 0
    assert batch.active is False
    assert batch.pending_count == 0
    assert batch.current_widgets == ()


def test_enqueue_before_frame() -> None:
    batch = FrameBatch()
    widget = RecordingWidget("pv")

    batch.enqueue(widget)

    assert batch.pending_count == 1


def test_duplicate_widget_is_coalesced() -> None:
    batch = FrameBatch()
    widget = RecordingWidget("pv")

    batch.enqueue(widget)
    batch.enqueue(widget)
    batch.enqueue(widget)

    assert batch.pending_count == 1


def test_begin_freezes_current_frame() -> None:
    batch = FrameBatch()
    pv = RecordingWidget("pv")
    battery = RecordingWidget("battery")

    batch.enqueue(pv)
    batch.enqueue(battery)

    current = batch.begin()

    assert current == (pv, battery)
    assert batch.current_widgets == (pv, battery)
    assert batch.pending_count == 0
    assert batch.active is True
    assert batch.frame_id == 1

    batch.end()


def test_enqueue_during_frame_waits_for_next_frame() -> None:
    batch = FrameBatch()
    current = RecordingWidget("current")
    next_widget = RecordingWidget("next")

    batch.enqueue(current)
    batch.begin()
    batch.enqueue(next_widget)

    assert batch.current_widgets == (current,)
    assert batch.pending_count == 1

    batch.end()

    assert batch.begin() == (next_widget,)
    batch.end()


def test_invalid_nested_begin_is_rejected() -> None:
    batch = FrameBatch()

    batch.begin()

    with pytest.raises(
        RuntimeError,
        match="A render frame is already active.",
    ):
        batch.begin()

    batch.end()


def test_pipeline_defers_invalidation_during_render() -> None:
    pipeline = RenderPipeline()
    first = RecordingWidget("first")
    second = RecordingWidget("second")

    def invalidate_second() -> None:
        pipeline.invalidate(second)

    first.on_render = invalidate_second
    pipeline.invalidate(first)

    first_frame = pipeline.render_pending()

    assert first_frame == 1
    assert first.render_calls == 1
    assert second.render_calls == 0
    assert pipeline.pending_count == 1

    second_frame = pipeline.render_pending()

    assert second_frame == 1
    assert second.render_calls == 1
    assert pipeline.pending_count == 0


def test_clear_discards_only_future_work() -> None:
    batch = FrameBatch()
    current = RecordingWidget("current")
    future = RecordingWidget("future")

    batch.enqueue(current)
    batch.begin()
    batch.enqueue(future)
    batch.clear()

    assert batch.current_widgets == (current,)
    assert batch.pending_count == 0

    batch.end()
