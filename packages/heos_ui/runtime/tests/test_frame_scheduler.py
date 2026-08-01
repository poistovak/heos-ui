from heos_ui.runtime import FrameResult, FrameScheduler
from heos_ui.widgets.base import Widget


class RecordingWidget(Widget):
    def __init__(self, widget_id: str = "widget") -> None:
        super().__init__(
            id=widget_id,
            title="Widget",
        )
        self.render_calls = 0

    def render(self) -> None:
        self.render_calls += 1


def test_frame_scheduler_starts_empty() -> None:
    scheduler = FrameScheduler()

    assert scheduler.frame_number == 0
    assert scheduler.pending_count == 0


def test_invalidate_marks_and_schedules_widget() -> None:
    scheduler = FrameScheduler()
    widget = RecordingWidget()

    changed = scheduler.invalidate(widget)

    assert changed is True
    assert widget.dirty is True
    assert scheduler.pending_count == 1


def test_repeated_invalidation_is_coalesced() -> None:
    scheduler = FrameScheduler()
    widget = RecordingWidget()

    first = scheduler.invalidate(widget)
    second = scheduler.invalidate(widget)
    third = scheduler.invalidate(widget)

    assert first is True
    assert second is False
    assert third is False
    assert scheduler.pending_count == 1


def test_render_frame_renders_pending_widget_once() -> None:
    scheduler = FrameScheduler()
    widget = RecordingWidget()

    scheduler.invalidate(widget)
    scheduler.invalidate(widget)

    result = scheduler.render_frame()

    assert result == FrameResult(
        frame_number=1,
        pending_widgets=1,
        rendered_widgets=1,
    )
    assert widget.render_calls == 1
    assert widget.dirty is False
    assert scheduler.pending_count == 0


def test_render_frame_batches_multiple_widgets() -> None:
    scheduler = FrameScheduler()
    solar = RecordingWidget("solar")
    battery = RecordingWidget("battery")
    grid = RecordingWidget("grid")

    scheduler.invalidate(solar)
    scheduler.invalidate(battery)
    scheduler.invalidate(grid)

    result = scheduler.render_frame()

    assert result.pending_widgets == 3
    assert result.rendered_widgets == 3
    assert solar.render_calls == 1
    assert battery.render_calls == 1
    assert grid.render_calls == 1


def test_empty_frame_is_recorded() -> None:
    scheduler = FrameScheduler()

    first = scheduler.render_frame()
    second = scheduler.render_frame()

    assert first == FrameResult(
        frame_number=1,
        pending_widgets=0,
        rendered_widgets=0,
    )
    assert second == FrameResult(
        frame_number=2,
        pending_widgets=0,
        rendered_widgets=0,
    )
    assert scheduler.frame_number == 2


def test_widget_can_render_in_later_frame() -> None:
    scheduler = FrameScheduler()
    widget = RecordingWidget()

    scheduler.invalidate(widget)
    first = scheduler.render_frame()

    scheduler.invalidate(widget)
    second = scheduler.render_frame()

    assert first.rendered_widgets == 1
    assert second.rendered_widgets == 1
    assert second.frame_number == 2
    assert widget.render_calls == 2
