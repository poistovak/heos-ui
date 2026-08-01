from heos_ui.runtime import RenderScheduler
from heos_ui.widgets.base import Widget


class RecordingWidget(Widget):
    def __init__(self) -> None:
        super().__init__(
            id="widget",
            title="Widget",
        )

    def render(self) -> None:
        pass


def test_scheduler_starts_empty() -> None:
    scheduler = RenderScheduler()

    assert scheduler.pending_count == 0


def test_invalidate_adds_widget_once() -> None:
    scheduler = RenderScheduler()
    widget = RecordingWidget()

    scheduler.invalidate(widget)
    scheduler.invalidate(widget)

    assert scheduler.pending_count == 1


def test_flush_renders_dirty_widget() -> None:
    scheduler = RenderScheduler()
    widget = RecordingWidget()

    widget.invalidate()
    scheduler.invalidate(widget)

    assert scheduler.flush() == 1
    assert widget.render_count == 1
    assert scheduler.pending_count == 0


def test_flush_empty_scheduler() -> None:
    scheduler = RenderScheduler()

    assert scheduler.flush() == 0