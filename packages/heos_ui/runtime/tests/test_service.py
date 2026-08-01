from heos_ui.runtime import RenderEvent, RenderRuntime
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


def test_runtime_starts_empty() -> None:
    runtime = RenderRuntime()

    assert runtime.frame == 0
    assert runtime.pending_count == 0


def test_invalidate_schedules_widget() -> None:
    runtime = RenderRuntime()
    widget = RecordingWidget()

    changed = runtime.invalidate(widget)

    assert changed is True
    assert runtime.pending_count == 1
    assert widget.dirty is True


def test_repeated_invalidation_is_coalesced() -> None:
    runtime = RenderRuntime()
    widget = RecordingWidget()

    first = runtime.invalidate(widget)
    second = runtime.invalidate(widget)
    third = runtime.invalidate(widget)

    assert first is True
    assert second is False
    assert third is False
    assert runtime.pending_count == 1


def test_tick_renders_pending_widgets() -> None:
    runtime = RenderRuntime()
    widget = RecordingWidget()

    runtime.invalidate(widget)

    event = runtime.tick()

    assert event == RenderEvent(
        frame=1,
        rendered=1,
    )
    assert widget.render_calls == 1
    assert runtime.pending_count == 0


def test_tick_emits_render_event() -> None:
    runtime = RenderRuntime()
    widget = RecordingWidget()
    received: list[RenderEvent] = []

    runtime.events.subscribe(received.append)
    runtime.invalidate(widget)

    event = runtime.tick()

    assert received == [event]


def test_runtime_batches_multiple_widgets() -> None:
    runtime = RenderRuntime()
    solar = RecordingWidget("solar")
    battery = RecordingWidget("battery")
    grid = RecordingWidget("grid")

    runtime.invalidate(solar)
    runtime.invalidate(battery)
    runtime.invalidate(grid)

    event = runtime.tick()

    assert event.rendered == 3
    assert event.frame == 1
    assert solar.render_calls == 1
    assert battery.render_calls == 1
    assert grid.render_calls == 1


def test_empty_tick_records_frame() -> None:
    runtime = RenderRuntime()

    event = runtime.tick()

    assert event == RenderEvent(
        frame=1,
        rendered=0,
    )
    assert runtime.profiler.snapshot.frame_count == 1


def test_multiple_ticks_advance_runtime() -> None:
    runtime = RenderRuntime()
    widget = RecordingWidget()

    runtime.invalidate(widget)
    first = runtime.tick()

    runtime.invalidate(widget)
    second = runtime.tick()

    assert first.frame == 1
    assert second.frame == 2
    assert widget.render_calls == 2
    assert runtime.profiler.snapshot.frame_count == 2
