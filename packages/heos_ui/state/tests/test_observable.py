from heos_ui.state import ObservableState


def test_observable_state_notifies() -> None:
    state = ObservableState()

    events: list[tuple[str, object]] = []

    def observer(key: str, value: object) -> None:
        events.append((key, value))

    state.subscribe("pv_power", observer)

    state.set("pv_power", 8.4)

    assert events == [("pv_power", 8.4)]


def test_observable_state_get() -> None:
    state = ObservableState()

    state.set("battery_soc", 83)

    assert state.get("battery_soc") == 83


def test_observable_state_unsubscribe() -> None:
    state = ObservableState()

    events: list[tuple[str, object]] = []

    def observer(key: str, value: object) -> None:
        events.append((key, value))

    state.subscribe("pv_power", observer)
    state.unsubscribe("pv_power", observer)

    state.set("pv_power", 7.2)

    assert events == []


def test_only_matching_key_is_notified() -> None:
    state = ObservableState()

    events: list[tuple[str, object]] = []

    def observer(key: str, value: object) -> None:
        events.append((key, value))

    state.subscribe("pv_power", observer)

    state.set("battery_soc", 90)
    state.set("pv_power", 8.5)

    assert events == [("pv_power", 8.5)]

def test_same_value_does_not_notify() -> None:
    state = ObservableState()

    events: list[tuple[str, object]] = []

    def observer(key: str, value: object) -> None:
        events.append((key, value))

    state.subscribe("pv_power", observer)

    state.set("pv_power", 8.5)
    state.set("pv_power", 8.5)
    state.set("pv_power", 8.5)

    assert events == [("pv_power", 8.5)]

def test_update_notifies_changed_keys() -> None:
    state = ObservableState()

    pv_events: list[tuple[str, object]] = []
    battery_events: list[tuple[str, object]] = []

    def pv_observer(key: str, value: object) -> None:
        pv_events.append((key, value))

    def battery_observer(key: str, value: object) -> None:
        battery_events.append((key, value))

    state.subscribe("pv_power", pv_observer)
    state.subscribe("battery_soc", battery_observer)

    state.set("battery_soc", 80)

    battery_events.clear()

    state.update(
        {
            "pv_power": 8.4,
            "battery_soc": 80,
        }
    )

    assert pv_events == [("pv_power", 8.4)]
    assert battery_events == []