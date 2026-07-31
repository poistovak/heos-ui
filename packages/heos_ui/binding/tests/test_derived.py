from heos_ui.binding import DerivedBinding
from heos_ui.state import ComputedState, ObservableState


def test_derived_binding_returns_computed_value() -> None:
    state = ObservableState()

    state.set("pv", 8.0)
    state.set("house", 5.5)

    binding = DerivedBinding(
        ComputedState(
            state=state,
            computer=lambda s: s.get("pv") - s.get("house"),
        )
    )

    assert binding.value() == 2.5


def test_derived_binding_reflects_state_changes() -> None:
    state = ObservableState()

    state.set("pv", 10.0)
    state.set("house", 4.0)

    binding = DerivedBinding(
        ComputedState(
            state=state,
            computer=lambda s: s.get("pv") - s.get("house"),
        )
    )

    assert binding.value() == 6.0

    state.set("house", 8.5)

    assert binding.value() == 1.5