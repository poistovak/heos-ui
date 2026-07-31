from heos_ui.state import ObservableState, StateChangeEvent


def test_state_event_observer_receives_changes() -> None:
    state = ObservableState()

    events: list[StateChangeEvent] = []

    state.subscribe_events(events.append)
    state.set("pv_power", 8.4)

    assert events == [
        StateChangeEvent(
            key="pv_power",
            value=8.4,
        )
    ]


def test_rollback_does_not_emit_state_event() -> None:
    state = ObservableState()

    events: list[StateChangeEvent] = []

    state.subscribe_events(events.append)

    state.begin()
    state.set("pv_power", 9.0)
    state.rollback()

    assert events == []