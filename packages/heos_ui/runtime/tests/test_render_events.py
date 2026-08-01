from heos_ui.runtime import RenderEvent, RenderEvents


def test_event_dispatch() -> None:
    events = RenderEvents()

    received = []

    events.subscribe(received.append)

    events.emit(
        RenderEvent(
            frame=7,
            rendered=3,
        )
    )

    assert len(received) == 1
    assert received[0].frame == 7
    assert received[0].rendered == 3


def test_multiple_subscribers() -> None:
    events = RenderEvents()

    a = []
    b = []

    events.subscribe(a.append)
    events.subscribe(b.append)

    event = RenderEvent(1, 2)

    events.emit(event)

    assert a == [event]
    assert b == [event]


def test_no_subscribers() -> None:
    events = RenderEvents()

    events.emit(RenderEvent(1, 0))