from heos_ui.state import ComputedState, ObservableState


def test_computed_state_returns_value() -> None:
    state = ObservableState()

    state.set("pv_power", 8.4)
    state.set("house_power", 5.2)

    computed = ComputedState(
        state=state,
        computer=lambda s: s.get("pv_power") - s.get("house_power"),
    )

    assert computed.value() == 3.2


def test_computed_state_updates_after_change() -> None:
    state = ObservableState()

    state.set("pv_power", 6.0)
    state.set("house_power", 2.0)

    computed = ComputedState(
        state=state,
        computer=lambda s: s.get("pv_power") - s.get("house_power"),
    )

    assert computed.value() == 4.0

    state.set("house_power", 5.5)

    assert computed.value() == 0.5