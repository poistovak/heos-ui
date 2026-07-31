from heos_ui.events import EventBus


def test_event_bus_publish() -> None:
    bus = EventBus()

    received: list[float] = []

    def handler(value: float) -> None:
        received.append(value)

    bus.subscribe("pv_power", handler)

    bus.publish("pv_power", 8.4)

    assert received == [8.4]


def test_event_bus_multiple_handlers() -> None:
    bus = EventBus()

    first: list[int] = []
    second: list[int] = []

    bus.subscribe("value", first.append)
    bus.subscribe("value", second.append)

    bus.publish("value", 5)

    assert first == [5]
    assert second == [5]