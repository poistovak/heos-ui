from heos_ui.runtime.render_queue import RenderQueue
from heos_ui.widgets.base import Widget


class RecordingWidget(Widget):
    def __init__(self, widget_id: str) -> None:
        super().__init__(
            id=widget_id,
            title=widget_id,
        )


def test_queue_starts_empty() -> None:
    queue = RenderQueue()

    assert queue.pending_count == 0
    assert queue.is_empty


def test_enqueue_widget() -> None:
    queue = RenderQueue()
    widget = RecordingWidget("pv")

    queue.enqueue(widget)

    assert queue.pending_count == 1


def test_duplicate_enqueue_is_ignored() -> None:
    queue = RenderQueue()
    widget = RecordingWidget("pv")

    queue.enqueue(widget)
    queue.enqueue(widget)
    queue.enqueue(widget)

    assert queue.pending_count == 1


def test_dequeue_preserves_order() -> None:
    queue = RenderQueue()

    pv = RecordingWidget("pv")
    battery = RecordingWidget("battery")
    grid = RecordingWidget("grid")

    queue.enqueue(pv)
    queue.enqueue(battery)
    queue.enqueue(grid)

    assert queue.dequeue_all() == (
        pv,
        battery,
        grid,
    )


def test_dequeue_clears_queue() -> None:
    queue = RenderQueue()

    queue.enqueue(RecordingWidget("pv"))

    queue.dequeue_all()

    assert queue.is_empty


def test_clear() -> None:
    queue = RenderQueue()

    queue.enqueue(RecordingWidget("pv"))
    queue.enqueue(RecordingWidget("battery"))

    queue.clear()

    assert queue.pending_count == 0
