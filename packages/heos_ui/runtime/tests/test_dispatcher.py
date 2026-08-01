from heos_ui.runtime import (
    RenderDispatcher,
    RenderEvent,
    RenderEvents,
    RenderLoop,
)


def test_dispatch_empty_frame() -> None:
    dispatcher = RenderDispatcher(
        RenderLoop(),
        RenderEvents(),
    )

    event = dispatcher.dispatch()

    assert event == RenderEvent(
        frame=1,
        rendered=0,
    )


def test_dispatch_emits_event() -> None:
    events = RenderEvents()
    received = []

    events.subscribe(received.append)

    dispatcher = RenderDispatcher(
        RenderLoop(),
        events,
    )

    event = dispatcher.dispatch()

    assert received == [event]


def test_multiple_dispatches() -> None:
    dispatcher = RenderDispatcher(
        RenderLoop(),
        RenderEvents(),
    )

    dispatcher.dispatch()
    event = dispatcher.dispatch()

    assert event.frame == 2


def test_dispatch_updates_profiler() -> None:
    loop = RenderLoop()

    dispatcher = RenderDispatcher(
        loop,
        RenderEvents(),
    )

    dispatcher.dispatch()

    assert (
        loop.profiler.snapshot.frame_count
        == 1
    )